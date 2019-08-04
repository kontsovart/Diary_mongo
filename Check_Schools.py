import pprint
import json


with open('/home/kamidae/PycharmProjects/analitics/School/School0.txt', 'r') as f:
    pprint.pprint(json.loads(f.read()))
