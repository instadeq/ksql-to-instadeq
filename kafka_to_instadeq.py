"""example using instadeq api client library to send kafka topics msg to instadeq"""
from __future__ import print_function

import os
import sys
import requests
import json

try:
    import requests
except ImportError:
    print("Couldn't import requests library")
    print("Install it with 'pip install requests' and try again")
    sys.exit(-1)

try:
    import kafka
except ImportError:
    print("Couldn't import kafka library")
    print("Install it with 'pip install kafka-python' and try again")
    sys.exit(-1)

from kafka import KafkaConsumer

def login_instadeq(instadeq_base, username, password):
    headers = {'content-type': 'application/json'}
    credentials = {'username': username, 'password': password}
    url = instadeq_base + "/sessions"
    response = requests.post(url, verify = False, data=json.dumps(credentials), headers=headers)
    status_ok = response.status_code in (200, 201)
    if not status_ok:
        print("Instadeq authentication failed")
        sys.exit(-1)
    return response.json().get("token")

def send_event_to_instadeq(instadeq_base, token, bucket, channel, event):
    headers = {'content-type': 'application/json','x-session': token}
    url = instadeq_base + "/streams/" + bucket + "/" + channel + "/"
    print(url)
    response = requests.post(url, verify = False, data=json.dumps(event), headers=headers)
    status_ok = response.status_code in (200, 201)
    return status_ok, response

def main(username, password, ktopic, instadeq_channel):
    """main program entry point"""

    print (username, password, ktopic, instadeq_channel)

    kservers = "0.0.0.0:39092"
    instadeq_bucket = "@" + username
    instadeq_base = "https://dev.instadeq.com"

    try:
        token = login_instadeq(instadeq_base, username, password)
        if not token:
            print("Error authenticating")
            return

        #subscribe to kafka
        consumer = KafkaConsumer(ktopic, bootstrap_servers=kservers)
        try:
            for msg in consumer:
                print (msg)
                if msg.value:
                    event = json.loads(msg.value)
                    send_ok, send_response = send_event_to_instadeq(instadeq_base, token, instadeq_bucket, instadeq_channel, event)
                    if not send_ok:
                        print("Error sending event to Instadeq", send_response)
                        return

        except IOError as error:
            print("Error consuming from kafka", ktopic, kservers, str(error))
            return

    except requests.exceptions.ConnectionError as conn_error:
        print("Error connection to server", args.url, str(conn_error))
        return

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    topic = sys.argv[3]
    instadeq_channel = sys.argv[4]
    main(username, password, topic, instadeq_channel)
