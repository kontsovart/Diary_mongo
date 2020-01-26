import json
import pprint
import os
from config import mydb


def some_schools():
    ltt = os.listdir('/home/albatros/PycharmProjects/Diary_mongo/School')
    for txt in ltt:
        if txt.endswith('.txt'):
            create_table_and_insert_data('school', 'School/' + txt)
            print(txt)


def fcking_students():
    ltt = os.listdir('/home/albatros/PycharmProjects/Diary_mongo/Student')
    ltt.sort()
    for txt in ltt:
        if txt.endswith('.txt'):
            create_table_and_insert_data('student', 'Student/' + txt)
            print(txt)


def create_table_and_insert_data(dbname, file_name):
    mytt = mydb[dbname]
    with open(file_name) as content_file:
        content = json.loads(content_file.read())
        dic = {}
    if isinstance(content, list):
        keys = [i[0].lower() + i[1:] for i in list(content[0].keys())]
        data = []
        for it in content:
            for count in range(len(keys)):
                dic.update({keys[count]: it.get(keys[count])})
            data.append(dic)
            dic = {}
        mytt.insert_many(data)
    else:
        keys = [i[0].lower() + i[1:] for i in list(content.keys())]
        dic.update({})
        for count, item in enumerate(content.values()):
            # if isinstance(item, str):
            #     dic.update({keys[count]: item})
            #     content.pop(keys[count], None)
            # if isinstance(item, dict):
            dic.update({keys[count]: item})
        mytt.insert_one(dic)


for item in mydb['student'].find({'idStudent': 1}, {'_id': 1, 'students': 1, 'idSchool': 1, 'subjects': 1}):
    pprint.pprint(item)
    break

