import httplib2
from apiclient import discovery
from oauth2client.contrib import appengine
import csv
import time

_SCOPE = 'https://www.googleapis.com/auth/bigquery'

# Change the following 3 values:
PROJECT_ID = 'your_project'
DATASET_ID = 'your_dataset'
TABLE_ID = 'TestTable'

#read CSV file
f = open('LoanStats.csv')
csv_f = csv.reader(f)

for row in csv_f:
    body = {"LoanStats":[
        {"loan_amnt": row[0], "int_rate": row[1], "annual_inc": row[2], "emp_length": row[3], "loan_status": row[4]}
    ]}
    time.sleep(1)
    print (body)

credentials = appengine.AppAssertionCredentials(scope=_SCOPE)
http = credentials.authorize(httplib2.Http())

bigquery = discovery.build('bigquery', 'v2', http=http)
response = bigquery.tabledata().insertAll(
   projectId=PROJECT_ID,
   datasetId=DATASET_ID,
   tableId=TABLE_ID,
   body=body).execute()

print response