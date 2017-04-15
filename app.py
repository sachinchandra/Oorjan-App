from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import or_
from sqlalchemy import text
from sqlalchemy.exc import DataError, IntegrityError, ProgrammingError
from conf import db_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)


class CityInfo(db.Model):
    __tablename__ = "cityinfo"
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    systemcapacity = db.Column(db.String(120))
    cityname = db.Column(db.String(120))
    cityid = db.Column(db.Integer, unique=True, primary_key=True)

    def __init__(self, latitude, longitude, systemcapacity, cityname, cityid):
        self.latitude = latitude
        self.longitude = longitude
        self.systemcapacity = systemcapacity
        self.cityname = cityname
        self.cityid = cityid

    def __repr__(self):
        return ""


class DcReferenceInfo(db.Model):
    __tablename__ = "referencedata"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(40))
    dc = db.Column(db.Numeric, primary_key=True)
    timestamp = db.Column(db.DateTime)

    def __init__(self, location, city, dc, timestamp):
        self.location = location
        self.city = city
        self.dc = dc
        self.timestamp = timestamp

    def __repr__(self):
        return ""


class DcInfo(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(40))
    solarid = db.Column(db.Integer)
    dc = db.Column(db.Numeric, primary_key=True)
    timestamp = db.Column(db.DateTime)

    def __init__(self, location, city, solarid, dc, timestamp):
        self.location = location
        self.city = city
        self.solarid = solarid
        self.dc = dc
        self.timestamp = timestamp

    def __repr__(self):
        return ""


class EmailInfo(db.Model):
    __tablename__ = "emailid"
    id = db.Column(db.Integer, primary_key=True)
    solarid = db.Column(db.Integer, primary_key=True, unique=True)
    emailid = db.Column(db.String(40))

    def __init__(self, solarid, emailid):
        self.solarid = solarid
        self.emailid = emailid

    def __repr__(self):
        return ""

# find list of all underperforming hours of a panel


@app.route('/<int:solar_id>/')
def low_performance(solar_id):
    date = request.args.get('date')

    try:
        final_list = low_performance_list(date, solar_id)
        return "underperforming hours \n" + '\n'.join(final_list)
    except ValueError as e:
        return str(e), 404
    except (DataError, TypeError):
        return 'Invalid input params', 400


# finding list of all underperforming hours


def low_performance_list(date, solar_id):

    sql_data = text('select dc from data where solarid ' + '=' + str(solar_id) + ' and cast(timestamp as date) =\'' +
                    str(datetime.datetime.strptime(date, '%d-%m-%Y')).split(" ")[0] + '\'')

    result_data = db.engine.execute(sql_data)
    dc = []
    for row in result_data:
        dc.append(row[0])

    sql_location = text(
        'select location from data where solarid ' + '=' + str(solar_id))

    result_location = db.engine.execute(sql_location)

    location = 0
    for row in result_location:
        location = row[0]

    sql_reference_data = text('select dc from referencedata where location ' + '=' + str(location) + ' and cast(timestamp as date) =\'' +
                              str(datetime.datetime.strptime(date, '%d-%m-%Y')).split(" ")[0] + '\'')

    result_reference_data = db.engine.execute(sql_reference_data)
    dc_reference = []
    for row in result_reference_data:
        dc_reference.append(row[0])

    low_performance_hours = []
    for index in range(len(dc_reference)):
        if (dc_reference[index] != 0 and dc[index] <= 0.8 * float(dc_reference[index])):
            low_performance_hours.append(str(index) + ":00 - " + str(index + 1) + ":00" +
                                         "  referencedc=" + str(dc_reference[index]) + "     originaldc=" + str(dc[index]))

    return low_performance_hours


# Add reference data for a city

@app.route("/addcityinfo", methods=['POST'])
def add_reference():
    try:
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        system_capacity = request.form['systemcapacity']
        city_name = request.form['cityname']
        city_id = request.form['cityid']
        city_info = CityInfo(
            latitude, longitude, system_capacity, city_name, city_id)
        db.session.add(city_info)
        db.session.commit()

        return "cityInfo data added"
    except DataError:
        return 'Invalid input params', 400

# Add hourly data


@app.route("/adddata", methods=['POST'])
def add_data():
    try:
        location = request.form['location']
        city = request.form['city']
        solar_id = request.form['solarid']
        dc = request.form['dc']
        timestamp = request.form['timestamp']
        is_reference_data = request.form['isreferencedata']

        if is_reference_data.lower() in ['yes', 'true', 't', 'y']:
            dc_reference_info = DcReferenceInfo(location, city, dc, timestamp)
            db.session.add(dc_reference_info)
            db.session.commit()
        else:
            dc_info = DcInfo(location, city, solar_id, dc, timestamp)
            db.session.add(dc_info)
            db.session.commit()

        return "hourly data added"
    except DataError as e:
        return 'Invalid input params', 400


# Add email linked to a solar panel


@app.route("/addemail", methods=['POST'])
def add_email():
    try:
        solar_id = request.form['solarid']
        email_id = request.form['emailid']
        email_info = EmailInfo(solar_id, email_id)
        db.session.add(email_info)
        db.session.commit()

        return "email data added"
    except DataError as e:
        return 'Invalid input params', 400


@app.route("/test")
def hello():
    return "app working!"


if __name__ == '__main__':
    app.debug = False
    app.run()
