"""message kafka generator"""
from __future__ import print_function

import datetime
import os
import sys
import json
import random
import time

try:
    import kafka
except ImportError:
    print("Couldn't import kafka library")
    print("Install it with 'pip install kafka-python' and try again")
    sys.exit(-1)

from kafka import KafkaProducer

def main():
    """main program entry point"""

    ktopic = "users"
    kservers = "0.0.0.0:39092"

    try:
        producer = KafkaProducer(bootstrap_servers=kservers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        while True:
            date = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 60 * 60 * 1))
            ts = time.mktime(date.timetuple()) * 1000
            obj = {
                    'username': random.choice(['javier', 'mariano', 'andre', 'sandra', 'franco', 'laura']),
                    'val': random.randint(0, 100),
                    'ts': ts
            }
            future = producer.send(ktopic, obj)
            result = future.get(timeout=5)
            print (obj)
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    except Exception as error:
        print("Error connection to server", kservers, str(error))
        return

if __name__ == "__main__":
    main()
