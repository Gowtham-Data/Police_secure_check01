import mysql.connector as db
import pandas as pd 

#Connect sql and create police_secure_check table:

connection = db.connect(
    host ='localhost',
    user ='gowtham',
    password ='Gautisql',
    database ='police_secure_check'
)
curr = connection.cursor()

#Create table:
#Create = """ create table Police_traffic_details1(
#   stop_date date,
#    stop_time time,
#	country_name varchar(20),
#	driver_gender varchar(10),
#	driver_age_raw int,
#	driver_age int,
#	driver_race varchar(20),
#	violation_raw varchar(20),
#	violation varchar(20),
#	search_conducted varchar(20),
#	search_type varchar(20),
#	stop_outcome varchar(20),
#	is_arrested varchar(20),
#	stop_duration varchar(30),
#	drugs_related_stop varchar(20),
#    vehicle_number varchar(20)    
#)
#"""
#curr.execute(Create)
#df = pd.read_excel("traffic_stops - orginal.xlsx")
#data = [tuple(None if pd.isna(x) else x for x in row) for row in df.itertuples(index=False, name=None)]

df = pd.read_excel("traffic_stops - orginal.xlsx")

# 2️⃣ Convert DataFrame rows to tuples and replace NaN with None
data = [tuple(None if pd.isna(x) else x for x in row) for row in df.itertuples(index=False, name=None)]

# 3️⃣ Insert query (make sure column names match the table)
#sql = """  
#  insert into Police_traffic_details1(
#      stop_date, stop_time, country_name, driver_gender, driver_age_raw, driver_age, 
#      driver_race, violation_raw, violation, search_conducted, search_type, 
#      stop_outcome, is_arrested, stop_duration, drugs_related_stop, vehicle_number
#   )
#   Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#"""

# 4️⃣ Bulk insert
#curr.executemany(sql, data)
#connection.commit()

#print(curr.rowcount, "rows inserted.")

#Query run:
qury = """
      Select * from Police_traffic_details1;
"""
curr = connection.cursor()
curr.execute(qury)

#Fetch the query:

d = curr.fetchall()

#Change to df and add column into data frame:

column= [desc[0] for desc in curr.description]
data = pd.DataFrame(d,columns=column)

data['drugs_related_stop'] = data['drugs_related_stop'].map({
    '0': 'Not Drug-Related',
    '1': 'Drug-Related'
})

#Change time format in stop time column:

data['stop_time'] = pd.to_timedelta(data['stop_time'])

data['stop_time'] = (pd.to_datetime(data['stop_time'].dt.total_seconds(), unit='s')
                     .dt.strftime('%I:%M %p'))

#change search_conducted

data['search_conducted'] = data['search_conducted'].map({
    '0': 'No Search was conducted',
    '1': 'Search was conducted'
})

#Gender col value change:
data['driver_gender'] = data['driver_gender'].map({
    'F': 'Female',
    'M': 'Male'
})

#pronounce he/she :

def pronounce(x):
    if x == 'Male':
        return'He'
    else:
        return 'She'


def Traffic_details():
    """Return cleaned police traffic data as DataFrame."""
    return data
