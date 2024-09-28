from datetime import datetime
from datetime import timedelta
import pytz

import heapq
from collections import deque
from itertools import combinations
import json
import logging
from flask import request
from routes import app

logger = logging.getLogger(__name__)

TEST_CASE = {
  "emails": [
    {
      "subject": "subject",
      "sender": "Alice",
      "receiver": "Bob",
      "timeSent": "2024-04-12T15:00:00+02:00"
    },
    {
      "subject": "RE: subject",
      "sender": "Bob",
      "receiver": "Alice",
      "timeSent": "2024-04-15T09:00:00+08:00"
    },
    {
      "subject": "RE: RE: subject",
      "sender": "Alice",
      "receiver": "Bob",
      "timeSent": "2024-04-16T09:05:00+02:00"
    }
  ],
  "users": [
    {
      "name": "Alice",
      "officeHours": {
        "timeZone": "Europe/Paris",
        "start": 9,
        "end": 18
      }
    },
    {
      "name": "Bob",
      "officeHours": {
        "timeZone": "Asia/Singapore",
        "start": 8,
        "end": 17
      }
    }
  ]
}

@app.route('/mailtime', methods=['POST'])
def mailtime():
    input = request.get_json()
    logging.info("data sent for evaluation {}".format(input))

    emails, users = input["emails"], input["users"]

    ori_send_receiver = {}
    classified_emails = {}

    users_time_count = {user["name"]: (timedelta(0), 0) for user in users}

    for email in emails:
        RE_occurence = email["subject"].count("RE: ")
        actual_subject = email["subject"].replace("RE: ", "")
        if actual_subject not in ori_send_receiver:
            ori_send_receiver[actual_subject] = (email["sender"], email["receiver"]) if RE_occurence % 2 == 0 else (email["receiver"], email["sender"])
        
        if actual_subject not in classified_emails:
            classified_emails[actual_subject] = [datetime.fromisoformat(email["timeSent"])]
        else:
            classified_emails[actual_subject].append(datetime.fromisoformat(email["timeSent"]))
    
    for subject in classified_emails.keys():
        sender, receiver = ori_send_receiver[subject]
        timing = classified_emails[subject]
        timing.sort()
        for i in range(1, len(classified_emails[subject])):
            if i % 2 == 0:
                users_time_count[sender] = (users_time_count[sender][0] + timing[i] - timing[i-1], 
                                            users_time_count[sender][1] + 1)
            else:
                users_time_count[receiver] = (users_time_count[receiver][0] + timing[i] - timing[i-1], 
                                              users_time_count[receiver][1] + 1)
    
    return_dict = {}
    for user, time_data in users_time_count.items():
        return_dict[user] = 0 if time_data[1] == 0 else int(time_data[0].total_seconds() / time_data[1])

    logging.info("My result :{}".format(return_dict))
    return json.dumps({"response": return_dict})

def mailtime_2():
    input = request.get_json()
    logging.info("data sent for evaluation {}".format(input))
    emails, users = input["emails"], input["users"]

    ori_send_receiver = {}
    classified_emails = {}

    users_time_count = {user["name"]: (0, 0) for user in users}
    users_working_hours = {user["name"]: (user["officeHours"]["timeZone"], 
                                          user["officeHours"]["start"], 
                                          user["officeHours"]["end"]) for user in users}

    for email in emails:
        RE_occurence = email["subject"].count("RE: ")
        actual_subject = email["subject"].replace("RE: ", "")
        if actual_subject not in ori_send_receiver:
            ori_send_receiver[actual_subject] = (email["sender"], email["receiver"]) if RE_occurence % 2 == 0 else (email["receiver"], email["sender"])
        
        if actual_subject not in classified_emails:
            classified_emails[actual_subject] = [datetime.fromisoformat(email["timeSent"])]
        else:
            classified_emails[actual_subject].append(datetime.fromisoformat(email["timeSent"]))
    
    for subject in classified_emails.keys():
        sender, receiver = ori_send_receiver[subject]
        timing = classified_emails[subject]
        timing.sort()
        for i in range(1, len(classified_emails[subject])):
            if i % 2 == 0:
                users_time_count[sender] = (users_time_count[sender][0] + working_hours(timing[i-1], 
                                                                                        timing[i], 
                                                                                        users_working_hours[sender][0],
                                                                                        (users_working_hours[sender][1], 
                                                                                         users_working_hours[sender][2])), 
                                            users_time_count[sender][1] + 1)
            else:
                users_time_count[receiver] = (users_time_count[receiver][0] + working_hours(timing[i-1], 
                                                                                        timing[i], 
                                                                                        users_working_hours[receiver][0],
                                                                                        (users_working_hours[receiver][1], 
                                                                                         users_working_hours[receiver][2])), 
                                              users_time_count[receiver][1] + 1)
    
    return_dict = {}
    for user, time_data in users_time_count.items():
        return_dict[user] = int(time_data[0] / time_data[1])

    logging.info("My result :{}".format(return_dict))
    return json.dumps({"response": return_dict})

def working_hours(start, end, timezone, workhours):
    tz = pytz.timezone(timezone)
    
    start_time = start.astimezone(tz)
    end_time = end.astimezone(tz)
    
    working_start_hour, working_end_hour = workhours
    total_working_seconds = 0
    
    current_day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    
    while current_day <= end_time:
        if current_day.weekday() < 5: 
            work_start = current_day.replace(hour=working_start_hour, minute=0, second=0, microsecond=0)
            work_end = current_day.replace(hour=working_end_hour, minute=0, second=0, microsecond=0)
            
            interval_start = max(work_start, start_time)
            interval_end = min(work_end, end_time)
            
            if interval_start < interval_end:
                total_working_seconds += (interval_end - interval_start).total_seconds()
        
        current_day += timedelta(days=1)
    
    return total_working_seconds

if __name__ == "__main__":
    print(mailtime_2(TEST_CASE))
