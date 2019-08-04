import pymongo
import json
import pprint
import os
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']


mytt = mydb['teacher']
mytt.create_index([('idTeacher', pymongo.ASCENDING)], unique=True)

mytt = mydb['school']
mytt.create_index([('idSchool', pymongo.ASCENDING)], unique=True)

mytt = mydb['student']
mytt.create_index([('idStudent', pymongo.ASCENDING)], unique=True)

mytt = mydb['subject']
mytt.create_index([('idSubject', pymongo.ASCENDING)], unique=True)

mytt = mydb['tmp']
mytt.create_index([('id', pymongo.ASCENDING)], unique=False)

mytt = mydb['tmp_pie']
mytt.create_index([('id', pymongo.ASCENDING), ('id_child', pymongo.ASCENDING)], unique=True)
#
# mytt = mydb['tmp_pie']
# mytt.drop_index([('id', pymongo.ASCENDING)])
