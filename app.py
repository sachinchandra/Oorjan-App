from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import or_
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/example'
db = SQLAlchemy(app)


class ReferenceData(db.Model):
    __tablename__ = "referencedata"
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    systemcapacity = db.Column(db.String(120))
    cityname = db.Column(db.String(120))
    cityid = db.Column(db.Integer, unique = True, primary_key = True)

    def __init__(self, latitude,longitude,systemcapacity,cityname,cityid):
        self.latitude = latitude
        self.longitude = longitude
        self.systemcapacity = systemcapacity
        self.cityname = cityname
        self.cityid = cityid

    def __repr__(self):
        return ""

class DcInfo(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.Integer, nullable = False)
    city = db.Column(db.String(40))
    solarid = db.Column(db.Integer)
    dc = db.Column(db.Numeric,primary_key = True)
    timestamp = db.Column(db.DateTime)

    def __init__(self, location,city,solarid,dc,timestamp):
        self.location = location
        self.city = city
        self.solarid = solarid
        self.dc = dc
        self.timestamp = timestamp

    def __repr__(self):
        return ""

class EmailInfo(db.Model):
    __tablename__ = "emailid"
    id = db.Column(db.Integer, primary_key = True)
    solarid = db.Column(db.Integer,primary_key = True, unique = True)
    emailid = db.Column(db.String(40))


    def __init__(self, solarid,emailid):
        self.solarid = solarid
        self.emailid = emailId

    def __repr__(self):
        return ""

# find list of all underperforming hours of a panel
@app.route('/<int:solar_id>/')
def lowPerformance(solar_id):
    date = request.args.get('date')
    finalList =lowPerformanceList(date,solar_id)
    
    return "underperforming hours \n" +  '\n'.join(finalList)

#finding list of all underperforming hours

def lowPerformanceList(date, solarid):


    print(date)


    sql = text('select dc from data where solarid ' + '=' + str(solarid) + ' and cast(timestamp as date) =\'' + str(datetime.datetime.strptime(date, '%d-%m-%Y')).split(" ")[0]+'\'')
    
    result = db.engine.execute(sql)
    dc = []
    for row in result:
        dc.append(row[0])

    sql1 = text('select location from data where solarid = ' + str(solarid))
    result1 = db.engine.execute(sql1)

    for val1 in result1:
        location = val1[0]

    sql2 = text('select systemcapacity from referencedata where cityid =' + str(location) )
    result2 = db.engine.execute(sql2)

    for val2 in result2:
        referenceValue = val2[0]

    lowPerformanceHours =[]
    i=0
    for val in dc :
    
        if val <= 0.8*float(referenceValue):

            lowPerformanceHours.append(str(i) + ":00 - " + str(i+1) + ":00")
        i =i+1
    

    return lowPerformanceHours


#Add reference data for a city

@app.route("/addReference", methods =['POST'])
def addReference():
    latitude = request.form['latitude']
    longitude = request.form ['longitude']
    systemCapacity = request.form ['systemcapacity']
    cityName = request.form['cityname']
    cityId = request.form['cityid']
    referenceData = ReferenceData(latitude,longitude,systemCapacity,cityName,cityId)
    db.session.add(referenceData)
    db.session.commit()

    return "reference data added"

#Add hourly data 

@app.route("/addData" , methods = ['POST'])
def addData():
    location = request.form['location']
    city = request.form['city']
    solarId = request.form['solarid']
    dc = request.form['dc']
    timeStamp = request.form['timestamp']
    dcInfo = DcInfo(location,city,solarId,dc,timeStamp)
    db.session.add(dcInfo)
    db.session.commit()


    return "hourly data added"

#Add email linked to a solar panel



@app.route("/addEmail" , methods = ['POST'])
def addEmail():
    solarId = request.form['solarid']
    emailId = request.form['emailid']
    emailInfo = EmailInfo(solarid,emailId)
    db.session.add(emailInfo)
    db.session.commit()

    return "email data added"



if __name__ == '__main__':
    app.debug = False
    app.run()
