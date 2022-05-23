# Jira Metrics

Jira Metrics extracts the most common team metrics from your Jira project.

# What you get
The script will generate two csv files with your sprint data.

### Details.csv
Contains information on each card completed and includes:

- **Ticket number**
- **Ticket type:** story, bug, task
- **Cycle time**
- **Lead time**
- **Moved left:** whether the ticket moved left on the board
- **_State entrance:_** showing when the ticket entered each board column
- **_Days per state_** 

<img width="594" alt="Screenshot 2022-05-23 at 16 04 04" src="https://user-images.githubusercontent.com/76520153/169840793-08114787-2316-43fe-9139-5f5bc89c799f.png">

### Summary.csv
Gives you a "birds-eye-view of each sprint. You get:

- **Throughput** (number of tickets done)
- **Bugs** (number o bugs done)
- **Spikes** (ditto)
- **Tasks**
- **Average cycle time**
- **Average lead time**

<img width="527" alt="Screenshot 2022-05-23 at 16 07 48" src="https://user-images.githubusercontent.com/76520153/169840851-00caf71f-2ccc-4453-9138-ce4542e5eb4a.png">

# Installing

The easiest way to install is just to download _jira_metrics.py_ and _jira_metrics.cfg_ to your computer.  

You will also need to install two dependencies. 

On MacOS:

```% pip3 install jira ```

```% pip3 install numpy ```

# Usage

### Get your API token

Before your first run you will need to generate an API Token from your Jira instance. It's pretty easy:

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
	"jql_done": "project = %s AND issuetype in (Bug, Story) AND status = Done  AND resolutionDate >= '%s' AND resolutionDate <= '%s' order by resolutiondate asc"
}
```
- **start_date:** report starting date (weekends are automtically ignored)
- **end-date:** report end date (weekends are automtically ignored)
- **sprint_names:** are just nicknames to your sprints to show on the reports
- **jira:** your jira credentials
- **teams:** 
	- _name:_ the name of your team
	- _jira_name:_ the name of the project in Jira
	- _jira_columns:_ are the column names on your board (warning: do NOT add the "To Do" and "Done" columns here)
	- _details_filename:_ it's the output filename
	- _summary_filename:_ it's the other output filename
- **holidays:** dates to exclude
- **jql_done:** is the jira query that will retrieve your tickets

## Execution

On MacOS:

```% python3 jira_extractor.py ```


