import mimesis
from mimesis import locales
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
import random
import pprint
import json
import datetime
from config import mydb
import Mongo


first_name = ''
last_name = ''
patronomik = ''
clas = {'gb': [], 'bb': [], 'norm': []}
classes = {}
for i in range(11):
    classes.update({i+1: clas})
gb = []
bb = []
norm = []

a = mimesis.Person(locales.RU)
ru = RussiaSpecProvider()
cl = mimesis.Numbers()
d = mimesis.Datetime()
t = mimesis.Text()

# пофиксить номера школ, районы, datetime в date, вынести subject в Учениках в оценках

mark_typ = ['Контрольная', 'Обычная']
visition = ['Был', 'Уважительная причина', 'Не уважительная причина']
subject_names = ['Математика', 'Химия', 'Физика', 'Астрономия', 'Информатика', 'Биология']


# def classify_students():
#     for i in range(20000):
#         if i % 5 == 0:
#             gb.append(i)
#         elif i % 5 == 1:
#             bb.append(i)
#         else:
#             norm.append(i)
#     return


def correct_marks_by_subject(students, subject, min_mark):
    mytt = mydb['student']
    pprint.pprint(students)
    for student in students:
        # print('student  ', student)
        for item in mytt.find({'idStudent': student}, {'_id': 0, 'subjects': 1}):
            # print('item  ', item)
            new_subjects = item['subjects']
            for subj in new_subjects:
                if subj['subject'] == subject:
                    new_marks = subj['marks']
                    for it in new_marks:
                        it['mark'] = random.choice([min_mark, min_mark + 1, min_mark + 1])
                    subj.update({'marks': new_marks})
            # pprint.pprint(item)
            # pprint.pprint(new_subjects)
            mytt.update_one({'idStudent': student}, {'$set': {'subjects': new_subjects}})



def Student():
    Students = []
    # good_guys = []
    # bad_boys = []
    # st_type = None
    for i in range(20000): # 300 000
        if i % 1000 == 0:
            print(i)
            if i % 10000 == 0 and i:
                with open(f'Student/Student{i}.txt', 'w') as f:
                    f.write(json.dumps(Students, default=myconverter))
                    print('written txt')
                Students = []
            # if i % 5000 == 0: # 50000
            #     with open(f'Bad_boys{i}.txt', 'w') as f:
            #         f.write(json.dumps(bad_boys, default=myconverter))
            #     with open(f'Good_guys{i}.txt', 'w') as f:
            #         f.write(json.dumps(good_guys, default=myconverter))
            #     good_guys = []
            #     bad_boys = []
            if i == 1000:
                with open('Data_PP/PP_Student.txt', 'w') as f:
                    pprint.pprint(Students, f)
                    print('written PP')
                # with open(f'PP_Bad_boys.txt', 'w') as f:
                #     pprint.pprint(bad_boys, f)
                # with open(f'PP_Good_guys.txt', 'w') as f:
                #     pprint.pprint(good_guys, f)
        idStudent = i
        gend = Gender.FEMALE
        clas = i % 11 + 1
        if i % 5 == 0:
            st_type = 'otl'
            min_mark = 4
            max_mark = 5
            # gb.append(i)
            classes[clas]['gb'].append(i)
        elif i % 5 == 1:
            st_type = 'udvl'
            min_mark = 2
            max_mark = 4
            # bb.append(i)
            classes[clas]['bb'].append(i)
        else:
            st_type = 'hor'
            min_mark = 3
            max_mark = 5
            # norm.append(i)
            classes[clas]['norm'].append(i)
        if i % 2 == 1:
            gend = Gender.MALE
        first_name = a.name(gender=gend)
        last_name = a.last_name(gender=gend)
        patronymic = ru.patronymic(gender=gend)
        subject = []
        for j in range(6):
            marks = []
            dates_kr = []
            for t in range(20):
                dates_kr.append(mimesis.Datetime.date(d, 2017, 2018))
            for k in range(80):
                if k % 4 == 3:
                    date = dates_kr.pop(0)
                    if st_type == 'udvl':
                        mark = random.choice([min_mark, (min_mark + max_mark) // 2, max_mark,
                                              (min_mark + max_mark) // 2, (min_mark + max_mark) // 2])
                    elif st_type == 'hor':
                        mark = random.choice([min_mark, max_mark, max_mark])
                    else:
                        mark = random.choice([min_mark, (min_mark + max_mark) // 2, max_mark])
                    mark_type = 'Контрольная'
                    visit = 'Был'
                else:
                    date = mimesis.Datetime.date(d, 2017, 2018)
                    mark = random.choice([random.choice([min_mark, (min_mark + max_mark) // 2, max_mark]), None, None])
                    mark_type = 'Обычная'
                    visit = random.choice(visition)
                marks.append({
                        'date': date,
                        'mark': mark,
                        'mark_type': mark_type,
                        'visit': visit
                    })
            subject.append({'subject': j, 'marks': marks})
        # if st_type == 'hor':
        Students.append({'idStudent': idStudent, 'first_name': first_name, 'last_name': last_name,
                     'patronymic': patronymic, 'class': clas, 'subjects': subject})
        # elif st_type == 'otl':
        #     good_guys.append({'idStudent': idStudent, 'first_name': first_name, 'last_name': last_name,
        #                  'patronymic': patronymic, 'class': clas, 'subjects': subject})
        # else:
        #     bad_boys.append({'idStudent': idStudent, 'first_name': first_name, 'last_name': last_name,
        #                  'patronymic': patronymic, 'class': clas, 'subjects': subject})
    with open(f'Student/Student_last.txt', 'w') as f:
        f.write(json.dumps(Students, default=myconverter))
        print('written txt')
    return Students


def Subject():
    Subjects = []
    for i, name in enumerate(subject_names):
        themes = []
        dates = []
        for j in range(60):
            dates.append(mimesis.Datetime.date(d, 2017, 2018))
        dates.sort()
        for k in range(30):
            date_beg = dates[k*2]
            date_end = dates[k*2 + 1]
            theme = mimesis.Text.title(t)
            themes.append({'date_of_begin': date_beg, 'date_of_end': date_end, 'theme': theme})
        Subjects.append({'idSubject': i, 'info': name, 'themes': themes})
    return Subjects


def Teacher():
    Teachers = []
    for i in range(15000):
        idTeacher = i
        gend = Gender.FEMALE
        if i % 3 == 1:
            gend = Gender.MALE
        first_name = a.name(gender=gend)
        last_name = a.last_name(gender=gend)
        patronymic = ru.patronymic(gender=gend)
        subjects = []
        rg = range(mimesis.Numbers.between(cl, 1, 3))
        for j in rg:
            while len(subjects) < j+1:
                idSubject = mimesis.Numbers.between(cl, 0, 5)
                if idSubject not in subjects:
                    subjects.append(idSubject)
        subjects.sort()
        Teachers.append({'idTeacher': idTeacher, 'first_name': first_name, 'last_name': last_name,
                         'patronymic': patronymic, 'subjects': subjects})
    return Teachers


def School():
    # with open('School.txt', 'w') as f:
    Schools = []
    # sch_status = None
    counter = 0
    for i in range(60): # 1500
        print(i)
        subjects = []
        if i % 10 == 0:
            sch_status = 'good'
        elif i % 10 == 1:
            sch_status = 'bad'
        else:
            sch_status = 'norm'
        for j in range(len(subject_names)):
            teachers = []
            cp = 1
            for count, tt in enumerate(Teachers):
                if j in tt.get('subjects'):
                    teachers.append({'teacher': tt.get('idTeacher'), 'class': cp,
                                     'date_of_start': mimesis.Datetime.date(d, 2016, 2016), 'date_of_end': None})
                    cp += 1
                    if cp == 12:
                        break
                    # tt = random.choice(Teachers)
                # break
            subjects.append({'idSubject': j, 'teachers': teachers})
        students = []
        pprint.pprint(subjects)
        idst = counter
        for k in range(99): # 200
            print(idst)
            if sch_status == 'good':
                if k % 2 == 0:
                    # idst = gb.pop(0)
                    idst = classes[k % 11 + 1]['gb'].pop(0)
                    students.append(idst)
                else:
                    # idst = norm.pop(0)
                    idst = classes[k % 11 + 1]['bb'].pop(0)
                    students.append(idst)
            elif sch_status == 'bad':
                if k % 2 == 0:
                    # idst = norm.pop(0)
                    idst = classes[k % 11 + 1]['norm'].pop(0)
                    students.append(idst)
                else:
                    # idst = bb.pop(0)
                    idst = classes[k % 11 + 1]['bb'].pop(0)
                    students.append(idst)
            else:
                if k % 10 == 0:
                    # idst = gb.pop(0)
                    idst = classes[k % 11 + 1]['gb'].pop(0)
                    students.append(idst)
                elif k % 2 == 0:
                    # idst = norm.pop(0)
                    idst = classes[k % 11 + 1]['norm'].pop(0)
                    students.append(idst)
                else:
                    # idst = bb.pop(0)
                    idst = classes[k % 11 + 1]['bb'].pop(0)
                    students.append(idst)
            # idst += 1
            # print(len(classes[k % 11 + 1]['bb']), len(classes[k % 11 + 1]['gb']), len(classes[k % 11 + 1]['norm']))
        Schools.append({'idSchool': i, 'subject': subjects, 'students': students})
        # print('OPAAAA')
        r_sub = random.randint(1, 5)
        # print(r_sub)
        if sch_status == 'good' or sch_status == 'bad':
            correct_marks_by_subject(students, r_sub, 4 if sch_status == 'good' else 2)
        # pprint.pprint(Schools)
        counter += idst
        if i % 300 == 0:
            with open(f'School/School{i}.txt','w') as f:
                f.write(json.dumps(Schools, default=myconverter))
                Schools = []
        # f.write(json.dumps(Schools, default=myconverter))
    with open(f'School/School_last.txt', 'w') as f:
        f.write(json.dumps(Schools, default=myconverter))
    return Schools


def Region():
    Reqion = {'region': 'Башкортостан'}
    areas = {}
    for i in range(3): # 10
        st = 'Area' + str(i)
        schools = {}
        for j in range(20): # 150
            qq = 'School#' + str(j + i*20)  # 100
            schools.update({qq: j + i*20})  # 100
        areas.update({st: schools})
    Reqion.update({'areas': areas})
    return Reqion


def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()


# def get_student_by_status(sch_status, idst):
#     if sch_status == 'good':
#         while idst % 5 != 0:
#             idst += 1
#     elif sch_status == 'bad':
#         while idst % 5 != 1:
#             idst += 1
#     else:
#         if idst % 5 == 0:
#             idst += 2
#         elif idst % 5 == 1:
#             idst += 1
#     return idst

Teachers = Teacher()
with open('Data/Teacher.txt', 'w') as f:
    f.write(json.dumps(Teachers, default=myconverter))
Mongo.create_table_and_insert_data('teacher', 'Data/Teacher.txt')
print('Done Teachers')


Region = Region()
with open('Data/Region.txt', 'w') as f:
    f.write(json.dumps(Region, default=myconverter))
Mongo.create_table_and_insert_data('region', 'Data/Region.txt')
print('Done Region')


Subject = Subject()
with open('Data/Subject.txt', 'w') as f:
    f.write(json.dumps(Subject, default=myconverter))
Mongo.create_table_and_insert_data('subject', 'Data/Subject.txt')
print('Done Subject')


# classify_students()

Student()
Mongo.fcking_students()
print('Done Student')


School = School()
Mongo.some_schools()
print('Done School')
#
#
# with open('Data/Region.txt', 'w') as f:
#     f.write(json.dumps(Region, default=myconverter))
# #
# with open('Data/Teacher.txt', 'w') as f:
#     f.write(json.dumps(Teachers, default=myconverter))
#
# with open('Data/Subject.txt', 'w') as f:
#     f.write(json.dumps(Subject, default=myconverter))
#
# with open('PP_Region.txt', 'w') as f:
#     pprint.pprint(Region, f)
#
# with open('PP_Subject.txt', 'w') as f:
#     pprint.pprint(Subject, f)
#
# with open('PP_Teacher.txt', 'w') as f:
#     pprint.pprint(Teachers, f)
#
# with open('PP_School.txt', 'w') as f:
#     pprint.pprint(School, f)

#Student = Student()
#print('Done Students')