import csv
import time
from google.cloud import pubsub


def publish_message(topic_name, data):
    """Publishes a message to a Pub/Sub topic with the given data."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    # Data must be a bytestring
    data = data.encode('utf-8')

    message_id = topic.publish(data)


#read CSV file
f = open('LoanStats.csv')
csv_f = csv.reader(f)

for row in csv_f:
    body = {"LoanStats":[
        {"loan_amnt": row[0], "int_rate": row[1], "annual_inc": row[2], "emp_length": row[3], "loan_status": row[4]}
    ]}

    print(body)
    publish_message('testtopic1',body)
    time.sleep(1)
# [END app]
