# README
# -------------------------------------------------------------------
# Prep work: install the following packages using PIP
#   pip3 install jira (https://pypi.org/project/jira)
#   pip3 install numpy
# Follow further instructions searching for ConfigMe in this script

from jira import JIRA
import numpy as np
from datetime import datetime
import json

with open("jira_metrics.cfg") as config_file:
    config = json.load(config_file)

cfg_jirauser = config["jira"]["user"]
cfg_jirakey = config["jira"]["apikey"]
cfg_jiraserver = config["jira"]["server"]

cfg_start = config["start_date"]
cfg_end = config["end_date"]

cfg_global_sprints = config["sprints"]
cfg_teams = config["teams"]
cfg_hols = config["holidays"]

# Jira sucks and the Done column needs to be referenced by its ID on next-gen projects
# https://community.atlassian.com/t5/Jira-Software-questions/How-to-retrieve-all-items-in-a-given-state-between-two-dates/qaq-p/1623283
# Done column IDs: PDN (10115), PA(10142), PES(10124), PD(10139)
cfg_jql_done = config["jql_done"]


# Returns the name of the sprint for a given date (format: %Y-%m-%d)
def get_sprint_name(date, sprints) -> str:
    for key, value in sprints.items():
        sprint_name = key
        sprint_start = value[0]
        sprint_end = value[1]

        if sprint_start <= date <= sprint_end:
            return sprint_name

    return "unknown"


# Returns the number of working days between two dates
def workdays_between(begin_date, end_date) -> str:
    if begin_date != "" and end_date != "":
        begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        number_of_days = np.busday_count(begin_date.date(), end_date.date(), holidays=cfg_hols)
        return number_of_days

    return ""


def has_moved_left(a_state, b_state, board_columns):
    if a_state in board_columns and b_state in board_columns:
        a_position = board_columns.index(a_state)
        b_position = board_columns.index(b_state)
        if a_position > b_position:
            return True
    return False


# Returns a Dictionary: key(sprintName), value=[cards] where each card is a {} dictionary
def get_tickets(board_columns, query, sprints) -> dict:
    # Prepares the return of this function (as stated above)
    sprint_data = {}
    for key in sprints.keys():
        sprint_data.update({key: []})

    jira = JIRA({"server": cfg_jiraserver}, basic_auth=(cfg_jirauser, cfg_jirakey))

    #pagination (maxResults is hard-capped at 100 in the backend)
    start_at = 0
    increment = 100

    #tickets = jira.search_issues(query, maxResults=increment, startAt=start_at, fields='resolutiondate, issuetype, created')
    print(query)
    tickets = jira.search_issues(query, maxResults=increment, startAt=start_at)
    total_tickets = len(tickets)

    while total_tickets != 0:

        for ticket in tickets:
            moved_left = "False"
            cross_layers = False
            start_date = ""

            board_transitions = {}

            changelog = jira.issue(ticket.key, expand='changelog').changelog

            prev_state = ""
            prev_date = ""

            first_entry = True

            # history items are in reverse chronological order, so the last item is the first state
            for history in changelog.histories:

                for item in history.items:

                    # Bespoke field in Jira where we capture which layers are also involved in this card
                    if item.field == 'Cross-layers':
                        cross_layers = True

                    # A change in 'status' means a change in columns on the board
                    if item.field == 'status':

                        curr_state = item.toString
                        curr_date = history.created[0:10]

                        # Jira allows history state transitions to itself (e.g., from To Do > To Do)
                        void_transition = item.toString == item.fromString

                        if not void_transition:

                            if curr_state not in board_transitions:
                                board_transitions[curr_state] = {"date_in": curr_date, "days_in": 0}

                            if first_entry:
                                prev_state = curr_state
                                prev_date = curr_date
                                first_entry = False

                            else:
                                date_diff = workdays_between(curr_date, prev_date)

                                if prev_state not in board_transitions:
                                    board_transitions[prev_state] = {"date_in": prev_date, "days_in": date_diff}

                                else:
                                    moved_left = has_moved_left(curr_state, prev_state, board_columns)
                                    days_in = board_transitions[curr_state]["days_in"]
                                    new_days_in = days_in + date_diff
                                    value = {"date_in": curr_date, "days_in": new_days_in}
                                    board_transitions.update({curr_state: value})

                                prev_state = curr_state
                                prev_date = curr_date

                                start_date = prev_date

            resolution_date = ticket.fields.resolutiondate[0:10]

            # Some cards jump from 'To Do' into 'Done', so cycle time needs to be 0
            cycle_time = workdays_between(start_date, resolution_date)
            if cycle_time == "":
                cycle_time = 0

            card = {
                "id": ticket.key,
                "type": ticket.fields.issuetype.name,
                "sprint": get_sprint_name((ticket.fields.resolutiondate[0:10]), sprints),
                "creator": "NA",  # ticket.fields.creator # Commenting out due to GDPR
                "created_date": ticket.fields.created[0:10],  # string obj, remove time
                "start_date": start_date,
                "done_date": ticket.fields.resolutiondate[0:10],
                "cycle_time": cycle_time,
                "lead_time": workdays_between(ticket.fields.created[0:10], ticket.fields.resolutiondate[0:10]),
                "moved_left": moved_left,
                "cross_layers": cross_layers,
                "columns_data": board_transitions  # contains dictionary (key = column_name, values: date_in, time_in)
                # "summary": ticket.fields.summary,
                # "raw_fields": ticket.raw['fields']
            }

            sprint_data[card["sprint"]].append(card)

        #pagination snippet
        start_at = start_at + increment
        tickets = jira.search_issues(query, maxResults=increment, startAt=start_at, fields='resolutiondate, issuetype, created')
        total_tickets = len(tickets)

    return sprint_data


# Outputs a DETAILED CSV with cards details
def create_sprint_details_csv(sprint_data, board_columns, filename):
    with open(filename, "w") as file:
        print_header = True

        for sprint, cards in sprint_data.items():

            for card in cards:

                # Prints the header before the first entry
                if print_header:
                    print_header = False
                    header = "Sprint,Ticket,Creator,Type,CycleTime,LeadTime,MovedLeft,CrossLayers"

                    for column in board_columns:
                        header += "," + column + " Date"
                    for column in board_columns:
                        header += "," + column + " Days"
                    file.write(header + "\n")

                line = "%s,%s,%s,%s,%s,%s,%s,%s" % (
                    card["sprint"], card["id"], card["creator"], card["type"], card["cycle_time"], card["lead_time"],
                    card["moved_left"], card["cross_layers"])

                for column in board_columns:
                    if column in card["columns_data"]:
                        date = card["columns_data"][column]["date_in"]
                        line += "," + date
                    else:
                        line += ","

                for column in board_columns:
                    if column in card["columns_data"]:
                        days_in = card["columns_data"][column]["days_in"]
                        line += "," + str(days_in)
                    else:
                        line += ","

                file.write(line + "\n")


# Outputs a SUMMARY CSV with Sprint metrics
def create_sprint_summary_csv(sprint_data, ref_columns, filename):
    header = "Sprint,Throughput,Stories,Bugs,Spikes,Tasks,AvgCycleTime,AvgLeadTime"

    for column in ref_columns:
        header = header + ',' + column

    with open(filename, "w") as file:
        file.write(header + "\n")

        for sprint, cards in sprint_data.items():
            total_cycletime = 0
            total_leadtime = 0
            total_stories = 0
            total_bugs = 0
            total_spikes = 0
            total_tasks = 0
            avg_cycletime = 0
            avg_leadtime = 0
            total_cards = len(cards)

            # Data structure to manipulate total and average days per column
            days_in_columns = {}
            for column in ref_columns:
                days_in_columns[column] = {'total': 0, 'average': 0}

            for card in cards:
                total_cycletime += card["cycle_time"]
                total_leadtime += card["lead_time"]
                if card["type"] == "Story":
                    total_stories += 1
                if card["type"] == "Bug":
                    total_bugs += 1
                if card["type"] == "Spike":
                    total_spikes += 1
                if card["type"] == "Task":
                    total_tasks += 1

                # Card did NOT move left? Add its time on each column to create averages
                if not card['moved_left']:
                    for column in card['columns_data']:
                        days_in = 0
                        if card['columns_data'][column]['days_in'] != '':
                            days_in = int(card['columns_data'][column]['days_in'])
                        days_in_columns[column]['total'] += days_in

            if total_cards != 0:
                avg_cycletime = round(total_cycletime / total_cards, 1)
                avg_leadtime = round(total_leadtime / total_cards, 1)
                for column in days_in_columns:
                    days_in_columns[column]['average'] = round(days_in_columns[column]['total'] / total_cards, 1)

            line = "%s,%s,%s,%s,%s,%s,%s,%s" % (
                sprint, total_cards, total_stories, total_bugs, total_spikes, total_tasks, avg_cycletime, avg_leadtime)

            for column in days_in_columns:
                line = line + ',' + str(days_in_columns[column]['average'])

            file.write(line + "\n")


# Manages exceptions when extracting keys from a dictionary
def get_value_from_dictionary(key, dictionary):
    try:
        value = dictionary[key]
        if len(value) == 0:
            value = None
    except KeyError:
        value = None
    return value


# Function that kicks off the creating of all reports"
def generate_reports():
    for team in cfg_teams:
        board_columns = team['jira_columns']
        jira_name = team['jira_name']

        csv_details = get_value_from_dictionary("details_filename", team)
        csv_bugs = get_value_from_dictionary("bugs_filename", team)
        csv_summary = get_value_from_dictionary("summary_filename", team)
        sprints = get_value_from_dictionary("sprints", team)

        if not sprints:
            sprints = cfg_global_sprints

        if csv_details or csv_bugs or csv_summary:
            print('Processing {0}'.format(team['name']))
            query = cfg_jql_done % (jira_name, cfg_start, cfg_end)
            #query = cfg_jql_done.format(p1=jira_name, p2=cfg_start, p3=cfg_end)


            sprint_data = get_tickets(board_columns, query, sprints)

            if csv_details:
                print(sprint_data)
                create_sprint_details_csv(sprint_data, board_columns, csv_details)

            if csv_summary:
                create_sprint_summary_csv(sprint_data, jira_name, csv_summary)

        else:
            print('%s - not processing ' % team['name'])


def main():
    generate_reports()


main()
