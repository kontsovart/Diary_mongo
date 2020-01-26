import pprint
import json
from config import mydb

for item in mydb['tmp_teacher'].find({'id': '6_0_20'}, {'_id': 0, 'data': 1}):
    pprint.pprint(item)
