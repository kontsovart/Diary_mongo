import pprint
import json


with open('/home/kamidae/PycharmProjects/analitics/Student/Student10000.txt', 'r') as f:
    pprint.pprint(json.loads(f.read()))
