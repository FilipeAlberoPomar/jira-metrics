# jira-metrics

Jira Metrics extracts the most common team metrics from your project.

<img src="https://user-images.githubusercontent.com/76520153/169852552-0eb9ab05-aff2-4d6c-ad09-3adcd1c1f541.png" width="100" /><img src="https://user-images.githubusercontent.com/76520153/169852578-4d4aacfd-dbab-4985-b46d-544c9d128762.png" width="100" />


# What you get
The script will generate two csv files with your sprint data.

### Details.csv
Contains information on each ticket **Done** and includes:

- **Ticket number:** the unique id of the ticket
- **Ticket type:** story, bug, task
- **Cycle time:** number of days "in progress"
- **Lead time:** number of days between creation and Done
- **Moved left:** whether the ticket moved left on the board
- **_"State entrance:"_** shows the date of entrance on each board column
- **_"Days per state:"_** shows the number of days the ticket was on each board column 


<img width="600" alt="Screenshot 2022-05-27 at 09 57 37" src="https://user-images.githubusercontent.com/76520153/170656777-6e75f710-21a8-4035-9f80-eaa823152d67.png">


### Summary.csv
Gives you a "birds-eye-view" of each sprint (for tickets **Done**). It includes:

- **Throughput:** number of tickets 
- **Bugs:** number of bugs
- **Spikes:** number of spikes
- **Tasks:** number of tasks
- **Average cycle time:** average number of days "in progress"
- **Average lead time:** average number of days between creation to Done
- **85th percentile cycle time:** 85% of all cycle times fall below this 
- **85th percentile lead time:** 85% of all lead times fall below this 

<img width="600" alt="Screenshot 2022-06-15 at 10 35 57" src="https://user-images.githubusercontent.com/76520153/173782445-626ccd59-4de3-461b-890e-7f0d08016716.png">


# Installation

First you install [Python 3](https://www.python.org/) (obviously). Then install two project dependencies. 

On MacOS:

```% pip3 install jira ```

```% pip3 install numpy ```

Now all you need to do is to download _jira_metrics.py_ and _jira_metrics.cfg_.  

# Configuration

### Get an API token

Before your first run you will need to generate an API Token from your Jira instance.

1. Click on your profile picture (top right)
2. Account Settings
3. Security
4. API Token > Create

### Add your project details

Now you need to add your project information to your _jira_metrics.cfg_ file. It's actually more simple than it looks.

```json
{
	"start_date": "YYYY-MM-DD",
	"end_date": "YYYY-MM-DD",
	"sprint_names": {
	    "sprint 1": ["YYYY-MM-DD", "YYYY-MM-DD"],
	    "sprint 2": ["YYYY-MM-DD", "YYYY-MM-DD"],
	    "sprint 3": ["YYYY-MM-DD", "YYYY-MM-DD"],
	    "sprint 4": ["YYYY-MM-DD", "YYYY-MM-DD"]
	},
	"jira":{
		"user": "<your jira user name>",
		"apitoken": "<API from jira>",
		"server": "<URL to your instance>"
	},
	"teams": [
		{
	        "name": "<team name>",
	        "jira_name": "<jira project name>",
	        "jira_columns": ["Column name", "Another column", "Yet another column"],
	        "details_filename": "details.csv",
		"summary_filename": "summary.csv",
		"sprint_names": {  }
		}
	],
	"holidays": ["YYYY-MM-DD", "YYYY-MM-DD"],
	"jql_done": "project = %s AND status = Done AND resolutionDate >= '%s' AND resolutionDate <= '%s'"
}
```
- **start_date:** report start date
- **end-date:** report end date
- **sprint_names:** are just nicknames to your sprints for reporting (add new ones at your heart's content)
- **jira:** your jira credentials
	- _user:_ is your username (likely an e-mail address)
	- _apitoken:_ the string you generated in the first step
	- _server:_ is the link to your Jira installation 
- **teams:** 
	- _name:_ the name of your team
	- _jira_name:_ the name of the project in Jira
	- _jira_columns:_ are the column names on your board (warning: do NOT add the "To Do" and "Done" columns here)
	- _details_filename:_ it's the output filename
	- _summary_filename:_ it's the other output filename
- **holidays:** dates to exclude
- **jql_done:** is the Jira query that will retrieve your tickets

_Bonus: this file can be used to generate metrics for multiple teams. In the "teams" element, you can copy and paste the {...} snippet having one per team. And separate each block of {} with a comma._

# Execution

Now you have to execute the script. 

On MacOS:

```% python3 jira_metrics.py ```

Jira Metrics will then read the configuration file and do its magic.

