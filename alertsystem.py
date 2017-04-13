import json
import datetime
import requests
import psycopg2
from collections import OrderedDict
import smtplib
from email.mime.text import MIMEText
import sys
sys.path.insert(0, '/var/www/html/flaskapp')

conn = psycopg2.connect(database="example", user='oorjan', password='oorjan', host="127.0.0.1", port="5432")

cur = conn.cursor()

cur.execute('select solarid,emailid from emailid')

result = cur.fetchall()
conn.commit()
conn.close()

solaremailids = [val for val in result]


now = datetime.datetime.now().date()
newformat = now.strftime('%d-%m-%Y')
params = OrderedDict([('date',newformat)])

# Make request and get statuses for mailing
finalEmails = []
for solarid in solaremailids:
	r = requests.get("http://localhost/{}".format(solarid[0]), params=params)
	finalEmails.append({'Subject': "underperforming hours of your solar panel",
					   'Message': r.text,
					   'To' : solarid[1]})


# Send mails
s = smtplib.SMTP('localhost')
me = 'mailer@oorjan.com'
for mail in finalEmails:
	msg = MIMEText(mail['Message'])
	msg['Subject'] = mail['Subject'] 
	msg['From'] = me
	msg['To'] = mail['To']

	s.sendmail(me, [msg['To']], msg.as_string())
