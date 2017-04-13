import psycopg2

conn = psycopg2.connect(database="example", host="127.0.0.1", port="5432")
print "Opened database successfully"

cur = conn.cursor()
cur.execute('create table referencedata(latitude decimal, longitude decimal, systemcapacity decimal, cityname varchar(30),cityid integer, primary key (cityid));')
cur.execute('create table data(location Integer not null, city varchar(30) , solarid Integer not null, dc decimal , timestamp timestamp );')
cur.execute('create table  emailid( solarid Integer not null, emailid varchar(30) , primary key (solarid));')
print "Table created successfully"

conn.commit()
conn.close()