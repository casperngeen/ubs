import json
from datetime import datetime, time, timedelta
import pytz
import re

import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    emails = data['emails']
    users_data = data['users']

    # Build user information dictionary
    users = {}
    for user in users_data:
        name = user['name']
        tz = pytz.timezone(user['officeHours']['timeZone'])
        start_hour = user['officeHours']['start']
        end_hour = user['officeHours']['end']
        users[name] = {
            'timeZone': tz,
            'startHour': start_hour,
            'endHour': end_hour,
            'responseTimes': []
        }

    # Function to parse datetime with timezone

    def parse_datetime(dt_str):
        return datetime.fromisoformat(dt_str)

    # Function to calculate working seconds between two datetimes for a user

    def calculate_working_seconds(start_dt, end_dt, user):
        total_seconds = 0
        current_dt = start_dt

        def end_of_day(dt): return dt.replace(
            hour=user['endHour'], minute=0, second=0, microsecond=0)

        def start_of_day(dt): return dt.replace(
            hour=user['startHour'], minute=0, second=0, microsecond=0)

        while current_dt < end_dt:
            # Skip weekends
            if current_dt.weekday() >= 5:
                current_dt += timedelta(days=1)
                current_dt = start_of_day(current_dt)
                continue

            work_end = end_of_day(current_dt)
            if current_dt >= work_end:
                # Move to next day's start
                current_dt += timedelta(days=1)
                current_dt = start_of_day(current_dt)
                continue

            work_start = max(current_dt, start_of_day(current_dt))
            work_end = min(work_end, end_dt)
            if work_start < work_end:
                total_seconds += (work_end - work_start).total_seconds()
            current_dt = work_end
        return total_seconds

    # Organize emails by thread using the subject
    threads = {}
    for email in emails:
        # Remove 'RE: ' prefixes to get the base subject
        base_subject = re.sub(r'^(RE:\s)+', '', email['subject'])
        if base_subject not in threads:
            threads[base_subject] = []
        threads[base_subject].append(email)

    # Process each thread
    for thread_emails in threads.values():
        # Sort emails by timeSent
        sorted_emails = sorted(
            thread_emails, key=lambda x: parse_datetime(x['timeSent']))
        # Map email index to sender
        email_index = {}
        for idx, email in enumerate(sorted_emails):
            email_index[idx] = email['sender']

        # For replies, calculate response time
        for idx in range(1, len(sorted_emails)):
            email = sorted_emails[idx]
            sender = email['sender']
            recipient = email['receiver']

            # Previous email time (when sender received the email)
            prev_email = sorted_emails[idx - 1]
            prev_sender = prev_email['sender']
            if sender == prev_sender:
                continue  # Skip if the sender hasn't changed

            # Parse datetimes
            prev_time = parse_datetime(prev_email['timeSent']).astimezone(
                users[sender]['timeZone'])
            reply_time = parse_datetime(email['timeSent']).astimezone(
                users[sender]['timeZone'])

            # Adjust times to user's timezone
            start_dt = prev_time
            end_dt = reply_time

            # Calculate working seconds
            working_seconds = calculate_working_seconds(
                start_dt, end_dt, users[sender])
            users[sender]['responseTimes'].append(working_seconds)

    # Calculate average response times
    output = {}
    for user_name, user_info in users.items():
        response_times = user_info['responseTimes']
        if response_times:
            average_response = sum(response_times) / len(response_times)
            output[user_name] = int(round(average_response))
        else:
            output[user_name] = 0

    logging.info("My result :{}".format(output))
    return json.dumps(output)
