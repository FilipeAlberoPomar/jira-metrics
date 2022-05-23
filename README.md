# Jira Metrics

Jira Metrics extracts the most common metrics from your Jira project.

# What you get
The script will generate two csv files with your data.

### Details.csv
Contains information on each card completed in the sprint and includes:

- **Ticket number**
- **Ticket type** (story, bug, task)
- **Cycle time**
- **Lead time**
- **Moved left** whether the ticket moved left on the board
- **"state entrance"** showing when the ticket entered each board column
- **"days per state"** 

### Summary.csv
Gives you a "birds-eye-view of each sprint. You get:

- **Throughput** (number of tickets done)
- **Bugs** (number o bugs done)
- **Spikes** (ditto)
- **Tasks**
- **Average cycle time**
- **Average lead time**

# Installing

The easiest way to install is just to download jira_metrics.py and jira_metrics.cfg to your computer. You will also need to install two dependencies. 

On MacOS

```pip3 install jira ```

``` pip3 install numpy ```

# Usage

Before your first run you will need to generate an api key from your Jira instance. It's pretty easy:

1. Click on your profile picture (top right)
2. Account Settings
3. Security
4. API token > Create
