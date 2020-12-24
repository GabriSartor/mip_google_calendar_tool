# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:34:23 2020

@author: Gabry
"""

import pandas as pd
import datetime
import numpy as np

class Event:
    
    def __init__(self, summary, startDate, endDate, location = None, course = None, teacher = None):
        self.body['summary'] = summary
        self.body['start']['dateTime'] = str(startDate)
        self.body['end']['dateTime'] = str(endDate)
        
        if location:
            self.body['location'] = location
        description = []
        if course:
            description.append("COURSE: {}".format(course))
        if teacher:
            description.append("TEACHER: {}".format(teacher))
        if description:
            self.body['description'] = description
        
    
    body = {
      'summary': None,
      'location': 'MIP - Politecnico di Milano (Bovisa)',
      'description': 'COURSE: None \nTEACHER: None',
      'start': {
        'dateTime': None,
        'timeZone':'Europe/Rome'
      },
      'end': {
        'dateTime': None,
        'timeZone':'Europe/Rome'
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 15},
        ],
      },
    }
    
    @classmethod
    def createFromSeries(cls, serie):
        start_time_str = serie.Date+' '+serie.Start
        end_time_str = serie.Date+' '+serie.End
        summary = serie.Summary
        startDate = datetime.datetime.strptime(start_time_str, '%A, %d %B %Y %I:%M %p').isoformat()
        endDate = datetime.datetime.strptime(end_time_str, '%A, %d %B %Y %I:%M %p').isoformat()
        course = None
        if not serie.isna().Course:
            course = serie.Course
        teacher = None
        if not serie.isna().Teacher:
            teacher = serie.Teacher
        location = 'MIP'
        if summary.find("ONLINE") != -1:
            location = "ONLINE"
            summary = summary.replace(" - ONLINE", "")
        return cls(summary, startDate, endDate, location, course, teacher)
