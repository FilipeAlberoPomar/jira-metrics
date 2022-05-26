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

<img width="594" alt="Screenshot 2022-05-23 at 16 04 04" src="https://user-images.githubusercontent.com/76520153/169840793-08114787-2316-43fe-9139-5f5bc89c799f.png">

### Summary.csv
Gives you a "birds-eye-view" of each sprint (for tickets **Done**). It includes:

- **Throughput:** number of tickets 
- **Bugs:** number of bugs
- **Spikes:** number of spikes
- **Tasks:** number of tasks
- **Average cycle time:** average number of days "in progress"
- **Average lead time:** average number of days between creation to Done

<img width="527" alt="Screenshot 2022-05-23 at 16 07 48" src="https://user-images.githubusercontent.com/76520153/169840851-00caf71f-2ccc-4453-9138-ce4542e5eb4a.png">

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

### Configure your project details

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

# Execution

Now you have to execute the script. 

On MacOS:

```% python3 jira_metrics.py ```

Jira Metrics will then read the configuration file and do its magic.

