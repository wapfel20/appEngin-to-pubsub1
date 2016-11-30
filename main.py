import csv
import time
import logging
import os

from flask import current_app, Flask, render_template, request
from google.cloud import pubsub


app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to veirfy that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']

#read CSV file
f = open('LoanStats.csv')
csv_f = csv.reader(f)

# Global list to storage messages received by this instance.
MESSAGES = []

for row in csv_f:
    body = {"LoanStats":[
        {"loan_amnt": row[0], "int_rate": row[1], "annual_inc": row[2], "emp_length": row[3], "loan_status": row[4]}
    ]}
    payload = body
    MESSAGES.append(payload)

    # [START push]
    @app.route('/', methods=['GET', 'POST'])
    def index():
        ps = pubsub.Client()
        topic = ps.topic(current_app.config['PUBSUB_TOPIC'])

        topic.publish(payload)
    # [END push]
    time.sleep(1)
print(MESSAGES)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]



