import mysql.connector
import sys

sys.path.append('fingerprint.py')
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import csv

### Connect to / Create Craigslist DB
connection = mysql.connector.connect(host="localhost", port=3306, user="semdemo", passwd="demo", db="semdemo",
                                     use_pure=True)
# use_pure: see https://stackoverflow.com/questions/50535192/i-get-notimplementederror-when-trying-to-do-a-prepared-statement-with-mysql-pyth
db = connection.cursor(prepared=True)

db.execute("""
        CREATE TABLE IF NOT EXISTS US_LISTINGS
        (
            Title VARCHAR(512) NOT NULL,
            Price VARCHAR(512) NOT NULL,
            Make VARCHAR(512) NOT NULL,
            Model VARCHAR(512) NOT NULL,
            MakeKey VARCHAR(512) NOT NULL,
            ModelKey VARCHAR(512) NOT NULL,
            Year VARCHAR(512) NOT NULL,
            Odo VARCHAR(512) NOT NULL DEFAULT "",
            Added VARCHAR(512) NOT NULL,
            URL VARCHAR(512) NOT NULL,
            TitleKey VARCHAR(512) NOT NULL,
            Area VARCHAR(512) NOT NULL,
            INDEX(MakeKey(512)),
            INDEX(ModelKey(512))
        )""")
connection.commit()
print('connected')
query = ('select * from US_LISTINGS;')
db.execute(query)

current_saved_listings = []
with open('output.csv', 'w') as f:
    print('file open')
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Make', 'Model', 'MakeKey', 'ModelKey', 'Year', 'Odo', 'Added', 'URL', 'TitleKey', 'Area'])
    for (Data) in db:
        print(Data)
        writer.writerow(Data)

print('Done')
