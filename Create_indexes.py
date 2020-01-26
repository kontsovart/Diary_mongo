from config import mydb
import pymongo

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

mytt = mydb['tmp_student']
mytt.create_index([('id', pymongo.ASCENDING)], unique=False)

mytt = mydb['tmp_teacher']
mytt.create_index([('id', pymongo.ASCENDING)], unique=False)

