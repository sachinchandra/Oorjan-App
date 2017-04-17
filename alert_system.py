import json
import datetime
import requests
import psycopg2
from collections import OrderedDict
import smtplib
from email.mime.text import MIMEText
from conf import db_name, db_port, db_host, db_user, db_password,api_host, api_port

import sys

sys.path.insert(0, '/var/www/html/flaskapp')

conn = psycopg2.connect(database=db_name, host=db_host,
                        port=db_port, user=db_user, password=db_password)

cur = conn.cursor()

cur.execute('select solarid,emailid from emailid')

result = cur.fetchall()
conn.commit()
conn.close()

solaremailids = [val for val in result]


now = datetime.datetime.now().date()
newformat = now.strftime('%d-%m-%Y')
params = OrderedDict([('date', newformat)])

# Make request and get statuses for mailing
finalEmails = []
for solarid in solaremailids:
    r = requests.get("http://{host}:{port}/{path}".format(host=api_host, port=api_port,path = solarid[0]), params=params)
    finalEmails.append({'Subject': "underperforming hours of your solar panel",
                        'Message': r.text,
                        'To': solarid[1]})


# Send mails
s = smtplib.SMTP('localhost')
me = 'mailer@oorjan.com'
for mail in finalEmails:
    msg = MIMEText(mail['Message'])
    msg['Subject'] = mail['Subject']
    msg['From'] = me
    msg['To'] = mail['To']

    s.sendmail(me, [msg['To']], msg.as_string())
