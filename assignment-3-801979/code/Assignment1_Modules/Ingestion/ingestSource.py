# main application

# read the input data

import sys, os
import csv
import pymongo
from sourceIngestion import sourceIngestion

client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client.get_database('test')
records = db.documents

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    next(reader) # skip header
    data = [r for r in reader]
insert = []
for i in data:
    line = sourceIngestion(*i)
    insert.append(line.map())

records.insert_many(insert)
