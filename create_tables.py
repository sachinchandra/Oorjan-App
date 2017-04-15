import psycopg2
from conf import db_name, db_port, db_host, db_user, db_password

conn = psycopg2.connect(database=db_name, host=db_host,
                        port=db_port, user=db_user, password=db_password)


cur = conn.cursor()
cur.execute('create table if not exists referencedata(location Integer not null, city varchar(30) , dc decimal , timestamp timestamp);')
cur.execute('create table if not exists data(location Integer not null, city varchar(30) , solarid Integer not null, dc decimal , timestamp timestamp );')
cur.execute('create table if not exists emailid( solarid Integer not null, emailid varchar(30) , primary key (solarid));')
cur.execute('create table if not exists cityinfo( latitude decimal, longitude decimal, systemcapacity decimal, cityname varchar(30),cityid integer, primary key (cityid));')


conn.commit()
conn.close()
