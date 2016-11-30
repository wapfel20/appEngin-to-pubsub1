import csv
import time
import logging
import os


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

    print(payload)
    time.sleep(1)
print(MESSAGES)

# [END app]