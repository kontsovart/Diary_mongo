import pprint
import json
from config import mydb

for item in mydb['tmp_teacher'].find({}, {'data': 1, '_id': 1}):
    print(1)
    tmp = []
    for it in item['data']:
        it.update({'type': 'column-line-mix'})
        tmp.append(it)
    mydb['tmp_teacher'].update({'_id': item['_id']}, {'$set': { 'data': tmp}})
