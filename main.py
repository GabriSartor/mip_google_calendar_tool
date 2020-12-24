from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from os import listdir
import pandas as pd

from Event import Event

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar.events']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    #Get the calendar list
    page_token = None
    count = 0
    calendars = []
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token, minAccessRole='writer').execute()
      for calendar_list_entry in calendar_list['items']:
          count +=1
          print("{}. {}".format(count, calendar_list_entry['summary']))
          calendars.append(calendar_list_entry)
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
          break
    
    print("Select the calendar (input number):")
    x = int(input())
    print("You selected this calendar: {}".format(calendars[x-1]))
    cal = calendars[x-1]
    
    event_list = []
    ## Leggere il csv, creare gli eventi e inseririrli
    for file in listdir('data'):
        df = pd.read_csv('data/{}'.format(file))
        df = df.dropna(subset=['Subject/Activity'])
        df = df.rename(columns={"Subject/Activity": "Summary", "Macro subject": "Course"})
        for i in range(len(df.index)):
            e = Event.createFromSeries(df.iloc[i])
            try:
                request = service.events().insert(calendarId=cal['id'], body=e.body)
                response = request.execute()
            except HttpError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.resp.status, e.error_details))
    print("... Events created")
#


if __name__ == '__main__':
    main()