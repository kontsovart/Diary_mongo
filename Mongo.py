import pymongo
import json
import pprint
import os
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']

# Russia language
# mark_typ = ['Контрольная', 'Обычная']
# visition = ['Был', 'Уважительная причина', 'Не уважительная причина']
# subject_names = ['Математика', 'Химия', 'Физика', 'Астрономия', 'Информатика', 'Биология']
# with open('Data/Subject.txt') as content_file:
#     content = json.loads(content_file.read())
#
# print(content)
# result = mytt.insert_many([{'info': item.get('info'), 'themes': item.get('themes')} for item in content])

# print(result)


# for item in mytt.find({'info': 'Физика'}, {'_id': 0, 'info': 1, 'themes': 1}):
#     print(item.get('themes'))
#     for it in item.get('themes'):
#         if it.get('date_of_begin') is not None and it.get('date_of_begin') > '2017-05-28':
#             print(it)
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
            print(txt)
            create_table_and_insert_data('student', 'Student/' + txt)


def create_table_and_insert_data(dbname, file_name):
    mytt = mydb[dbname]
    with open(file_name) as content_file:
        content = json.loads(content_file.read())
        dic = {}
    if isinstance(content, list):
        # print(list(content))
        keys = [i[0].lower() + i[1:] for i in list(content[0].keys())]
        data = []
        for item in content:
            for count in range(len(keys)):
                dic.update({keys[count]: item.get(keys[count])})
            data.append(dic)
            dic = {}
        mytt.insert_many(data)
    else:
        keys = [i[0].lower() + i[1:] for i in list(content.keys())]
        dic.update({})
        for count, item in enumerate(content.values()):
            if isinstance(item, str):
                dic.update({keys[count]: item})
                content.pop(keys[count], None)
            if isinstance(item, dict):
                dic.update({keys[count]: item})
        mytt.insert_one(dic)


# create_table_and_insert_data('subject', 'Data/Subject.txt')
# create_table_and_insert_data('teacher', 'Data/Teacher.txt')
# create_table_and_insert_data('region', 'Data/Region.txt')
# some_schools()
# fcking_students()

# print(1)
# a = datetime.datetime.now()
# qq = 0
# for item in mydb['region'].find({}, {'_id': 1, 'areas': 1}):
#     # print('Oppa')
#     pprint.pprint(item)


# sts = []
for item in mydb['student'].find({'idStudent': 1}, {'_id': 1, 'students': 1, 'idSchool': 1, 'subjects': 1}):
    # print('Oppa')
    pprint.pprint(item)
    break
    # 4
for item in mydb['student'].find({'idStudent': 0}, {'_id': 1, 'first_name': 1, 'last_name': 1, 'subjects': 1}):
    # print('Oppa')
    pprint.pprint(item)
    break
    # 3
# for item in mydb['tmp_pie'].find({}, {'_id': 1, 'type': 1}):
#     # print('Oppa')
#     pprint.pprint(item)
#     break
# for item in mydb['school'].find({}, {'_id': 1, 'students': 1, 'idSchool': 1, 'subject': 1}):
#     # print('Oppa')
#     pprint.pprint(item)
#     break
# print(2)
# #
# for item in mydb['student'].find({'idStudent': sts[0]}, {'_id': 1, 'class': 1,
#   'first_name': 1,
#   'idStudent': 1,
#   'last_name': 1,
#   'patronymic': 1,
#   'subjects' : 1}):
#     # pass
#     # print(datetime.datetime.now() - a)
#     pprint.pprint(item)
#
# print(datetime.datetime.now() - a)
# print(qq)

# fcking_students()
# print(2)
# for item in mydb['student'].find({'idStudent': 300}, {'_id': 1, 'class': 1,
#   'first_name': 1,
#   'idStudent': 1,
#   'last_name': 1,
#   'patronymic': 1}):
#     print('Oppa')
#     pprint.pprint(item)

# fcking_students()
# print(3)
# for item in mydb['student'].find({'idStudent': 300}, {'_id': 1, 'class': 1,
#   'first_name': 1,
#   'idStudent': 1,
#   'last_name': 1,
#   'patronymic': 1}):
#     print('Oppa')
#     pprint.pprint(item)
