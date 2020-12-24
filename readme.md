# MIP - Google Calendar Tool: 
 This is a simple tool to convert csv tables (from MIP pdf calendar format) in Google Calendar events
 
## Requirements
 - Python 3.8
 - Pip or another packet manager
 - Pandas
 - A Google account 
 
## Quick start
 - Convert .pdf in .csv (there are a lot free online tools to do this) or use the ones provided in 'data/'
 - Run `pip install -r requirements.txt` in the root folder to install python modules
 - Go to this [site](https://developers.google.com/calendar/quickstart/python) , enable Google Calendar API and download credentials (or use the Google console page to create a project and OAuth2 credentials)
 - Save them as 'credential.json' in root folder
 - Run `python main.py`, authorize the application, choose the calendar and enjoy!

