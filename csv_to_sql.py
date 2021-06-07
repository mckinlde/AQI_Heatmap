import mysql.connector
import sys
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import csv

### Connect to / Create Craigslist DB
connection = mysql.connector.connect(host="localhost", port=3306, user="semdemo", passwd="demo", db="semdemo",
                                     use_pure=True)
# use_pure: see https://stackoverflow.com/questions/50535192/i-get-notimplementederror-when-trying-to-do-a-prepared-statement-with-mysql-pyth
db = connection.cursor(prepared=True)
connection.commit()
print('connected')

db.execute("""CREATE TABLE IF NOT EXISTS AQI_INDEX
        (
            County VARCHAR(64) NOT NULL,
            FIPS VARCHAR(64) NOT NULL,
            Date VARCHAR(64) NOT NULL,
            AQI VARCHAR(64) NOT NULL,
            Pollutant VARCHAR(64) NOT NULL,
            AveragingTime VARCHAR(64) NOT NULL,
            AQICategory VARCHAR(64) NOT NULL
        ) """)
connection.commit()
print('table AQI_INDEX exists')

count = 0
with open('AQI_by_County_1970_2021.csv', newline='') as csvfile:
    airreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in airreader:
        if count == 0:
            print(row)
            print('Data:')
        if count > 10:
            query = '''INSERT INTO AQI_INDEX
            (County, FIPS, Date, AQI, Pollutant, AveragingTime, AQICategory)
            VALUES
            (\''''+row[0]+'\', \''+row[1]+'\', \''+row[2]+'\', \''+row[3]+'\', \''+row[4]+'\', \''+row[5]+'\', \''+row[6]+'\');'
            print(query)
            db.execute(query)
            connection.commit()
        count += 1


'''
with open('output.csv', 'w') as f:
    print('file open')
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Make', 'Model', 'MakeKey', 'ModelKey', 'Year', 'Odo', 'Added', 'URL', 'TitleKey', 'Area'])
    for (Data) in db:
        print(Data)
        writer.writerow(Data)
'''
print('Done')
