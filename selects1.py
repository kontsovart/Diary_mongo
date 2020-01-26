import psycopg2
import pymongo
import datetime
import pprint
from itertools import groupby

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']

def avg_mark_region(chart_type,region,district=None,school_id=None,class_id=None,subject_id=None,topic=None,
                    mark_type=None,date1=None,date2=None, title = "Region Башкортостан"):
    # cur.execute("select district from settlement where region LIKE %s",(region,))
    myreg = mydb['region']
    mas = myreg.find({}, {'areas': 1})
    areas = {}
    for area in mas:
        areas = area.get("areas")
    #mark_avg = {subject:{data:[mark,count]}}
    date_mas = get_date_topic(subject_id,topic,date1,date2)
    mark_avg = {}
    avg_mark_district(areas,district,school_id,class_id,subject_id,mark_type,date_mas[0],date_mas[1],mark_avg,title,chart_type)
    mas_avg1 = None
    if chart_type == 'line':
        mas_avg1 = prepare_data_week(mark_avg,title=title,oxName="Date",oyName="Mark")
    elif chart_type == 'pie':
        mas_avg1 = prepare_data_pie(mark_avg, title=title, oxName="Date", oyName="Mark")
    return mas_avg1

def avg_mark_district(mas,district,school_id,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type):
    for area in mas:
        if district != None:
            if area == district:
                title += "Area " + district + " "
                avg_mark_school(mas.get(area).values(),school_id,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type)
        else:
            avg_mark_school(mas.get(area).values(), school_id, class_id, subject_id, mark_type, date1, date2,mark_avg,title,chart_type)

def avg_mark_school(mas,school_id,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type):
    for school in mas:
        if school_id != None:
            if school == school_id:
                title += "School " + str(school_id) + " "
                avg_mark_school_student(school,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type)
        else:
            avg_mark_school_student(school,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type)

def avg_mark_school_student(school,class_id,subject_id,mark_type,date1,date2,mark_avg,title,chart_type):
    # cur.execute("select students from school where id=(%s)", (school,))
    # mas_stud = cur.fetchone()[0]
    mas_stud = []
    for item in mydb['school'].find({'idSchool': school}, {'_id': 1,'students': 1}):
        mas_stud = item["students"]
    for student in mas_stud:
        try:
            # cur.execute("select class from student where id=(%s)", (student,))
            # stud_class = cur.fetchone()[0]
            stud_class = None
            for item in mydb['student'].find({'idStudent': student}, {'_id': 1, 'class': 1, 'subjects': 1}):
                stud_class = item
            if class_id:
                if class_id == stud_class["class"]:
                    title += "Class " + str(class_id) + " "
                    # cur.execute("select marks from student where id=(%s)", (student,))
                    # mas_subject = cur.fetchone()[0]
                    avg_mark_subject(stud_class["subjects"],subject_id,mark_type,date1,date2,mark_avg,title,chart_type)
            else:
                # cur.execute("select marks from student where id=(%s)", (student,))
                # mas_subject = cur.fetchone()[0]
                avg_mark_subject(stud_class["subjects"], subject_id, mark_type, date1, date2, mark_avg,title,chart_type)
        except Exception as e:
            pass

def avg_mark_subject(mas,subject_id,mark_type,date1,date2,mark_avg,title,chart_type):
    for subject in mas:
        if subject_id != None:
            if subject["subject"] == subject_id:
                title += "Subject " + str(subject_id) + " "
                avg_mark_date(subject,mark_type,date1,date2,mark_avg,title,chart_type)
        else:
            avg_mark_date(subject,mark_type,date1,date2,mark_avg,title,chart_type)

def avg_mark_date(subject,mark_type,date1,date2, mark_avg,title,chart_type):
    if subject["subject"] not in mark_avg:
        mark_avg.update({subject["subject"]: {}})
    for mark in subject["marks"]:
        if mark["mark"]:
            if date1 and date2:
                if mark["date"] >= date1 and mark["date"] <= date2:
                    title += "Date of begin " + date1 + "Date of end" + date2 + " "
                    avg_mark_type(mark, subject, mark_type, mark_avg,title,chart_type)
            elif date1 and not date2:
                if mark["date"] >= date1:
                    title += "Date of begin " + date1 + " "
                    avg_mark_type(mark, subject, mark_type, mark_avg,title,chart_type)
            elif date2 and not date1:
                if mark["date"] <= date2:
                    title += "Date of end" + date2 + " "
                    avg_mark_type(mark, subject, mark_type, mark_avg,title,chart_type)
            else:
                avg_mark_type(mark, subject, mark_type, mark_avg,title,chart_type)


def avg_mark_type(mark,subject,mark_type,mark_avg,title,chart_type):
    if mark_type != None:
        if mark["mark_type"] == mark_type:
            title += "Mark type " + mark_type + " "
            if chart_type == 'line':
                avg_mark_mark_line(mark,subject,mark_avg)
            elif chart_type == 'pie':
                avg_mark_mark_circle(mark, subject, mark_avg)
    else:
        if chart_type == 'line':
            avg_mark_mark_line(mark, subject, mark_avg)
        elif chart_type == 'pie':
            avg_mark_mark_circle(mark, subject, mark_avg)



def avg_mark_mark_line(mark,subject,mark_avg):
    if mark["date"] not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({mark["date"]: [0, 0]})
    mark_avg[subject["subject"]][mark["date"]][0] += mark["mark"]
    mark_avg[subject["subject"]][mark["date"]][1] += 1

def avg_mark_mark_circle(mark,subject,mark_avg):
    if mark["mark"] not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({mark["mark"]: 0})
    mark_avg[subject["subject"]][mark["mark"]] += 1





def avg_mark_student(chart_type,student_id,subject_id=None,topic=None,mark_type=None,date1=None,date2=None):
    # conn = psycopg2.connect("dbname=diary user=postgres password=123")
    # cur = conn.cursor()
    # cur.execute("select marks from student where id=(%s)", (student_id,))
    # mark_avg = {subject:{data:[mark,count]}}
    mas_subject = None
    for item in mydb['student'].find({'idStudent': student_id}, {'_id': 1, 'subjects': 1}):
        mas_subject = item
    mark_avg = {}
    title = "Student "+str(student_id) + " "
    # mas_subject = cur.fetchone()[0]
    date_mas = get_date_topic(subject_id, topic, date1, date2)
    avg_mark_subject(mas_subject["subjects"], subject_id,mark_type, date_mas[0], date_mas[1], mark_avg,title,chart_type)
    # cur.close()
    # conn.close()
    mas_avg1 = prepare_data_week(mark_avg, title=title, oxName="Date", oyName="Mark")
    return mas_avg1






def avg_mark_teacher(chart_type,region,teacher_id,class_id=None,subject_id=None,topic=None,mark_type=None,date1=None,date2=None):
    # conn = psycopg2.connect("dbname=diary user=postgres password=123")
    # cur = conn.cursor()
    # cur.execute("select district from settlement where region LIKE %s", (region,))
    # mas = cur.fetchone()[0]
    # mark_avg = {subject:{data:[mark,count]}}
    myreg = mydb['region']
    mas = myreg.find({}, {'areas': 1})
    areas = {}
    for area in mas:
        areas = area.get("areas")
    mark_avg = {}
    title = "Region "+region+" Teacher "+ str(teacher_id) + " "
    # cur.execute("select subject from teacher where id=(%s)", (teacher_id,))
    # subject_teach = cur.fetchone()[0]
    subject_teach = None
    for item in mydb['teacher'].find({'idTeacher': teacher_id}, {'_id': 1, 'subjects': 1}):
        subject_teach = item
    date_mas = get_date_topic(subject_id,topic,date1,date2)
    for area in areas:
        for school in areas.get(area).values():
            # cur.execute("select subject_and_teacher from school where id=(%s)", (school,))
            # subjects = cur.fetchone()[0]
            subjects = None
            for item in mydb['school'].find({'idSchool': school}, {'_id': 1, 'subject': 1}):
                subjects = item
            avg_mark_teacher_subject(school,subjects["subject"],subject_teach["subjects"],class_id,subject_id,teacher_id,mark_type,mark_avg,date_mas[0],date_mas[1],title,chart_type)
    # cur.close()
    # conn.close()
    mas_avg1 = prepare_data_week(mark_avg, title=title, oxName="Date", oyName="Mark")
    return mas_avg1

def avg_mark_teacher_subject(school,subjects,subject_teach,class_id,subject_id,teacher_id,mark_type,mark_avg,date1,date2,title,chart_type):
    for subject in subjects:
        if subject_id != None:
            if (subject["idSubject"] == subject_id) and (subject["idSubject"] in subject_teach):
                title += "Subject " + str(subject_id) + " "
                avg_mark_teacher_class(school,subject,class_id,teacher_id,mark_type,mark_avg,date1,date2,title,chart_type)
        elif subject["idSubject"] in subject_teach:
            avg_mark_teacher_class(school,subject,class_id,teacher_id,mark_type,mark_avg,date1,date2,title,chart_type)


def avg_mark_teacher_class(school,subject,class_id,teacher_id,mark_type,mark_avg,date1,date2,title,chart_type):
    for teacher in subject["teachers"]:
        if teacher_id == teacher["teacher"]:
            if class_id != None:
                if teacher["class"] == class_id:
                    title += "Class " + str(class_id) + " "
                    avg_mark_teacher_date(teacher,school,subject,mark_type,mark_avg,date1,date2,title,chart_type)
            else:
                avg_mark_teacher_date(teacher,school,subject,mark_type,mark_avg,date1,date2,title,chart_type)

def avg_mark_teacher_date(teacher,school,subject,mark_type,mark_avg,date1,date2,title,chart_type):
    date_of_start = teacher["date_of_start"]
    date_of_end = teacher["date_of_end"]
    date_mas = compare_date(date_of_start,date_of_end,date1,date2)
    avg_mark_school_student(school, teacher["class"], subject["idSubject"], mark_type, date_mas[0], date_mas[1], mark_avg,title,chart_type)


def get_date_topic(subject_id,topic,date1,date2):
    if subject_id != None:
        # cur.execute("select topics from Subject_and_Topic where id=(%s)", (subject_id,))
        # themes = cur.fetchone()[0]
        themes = []
        for item in mydb['subject'].find({'idSubject': subject_id}, {'_id': 1, 'themes': 1}):
            themes = item["themes"]
        if topic != None:
            for theme in themes:
                if theme["theme"] == topic:
                    date_of_begin = theme["date_of_begin"]
                    date_of_end = theme["date_of_end"]
                    return compare_date(date_of_begin,date_of_end,date1,date2)
                    # if date1 and date2:
                    #     if date_of_begin >= date1 and date_of_end <= date2:
                    #         return [date_of_begin, date_of_end]
                    #     elif date_of_begin >= date1 and date_of_end >= date2:
                    #         return [date_of_begin, date2]
                    #     elif date_of_begin <= date1 and date_of_end <= date2:
                    #         return [date1, date_of_end]
                    #     elif date_of_begin <= date1 and date_of_end >= date2:
                    #         return [date1, date2]
                    # elif date1 and not date2:
                    #     if date_of_begin >= date1:
                    #         return [date_of_begin, date2]
                    # elif date2 and not date1:
                    #     if date_of_end <= date2:
                    #         return [date_of_begin, date_of_end]
                    # else:
                    #     return [date1, date2]
    return [date1,date2]

def compare_date(date1,date2,date3,date4):
    if date1 == None:
        date1 = date3
    if date2 == None:
        date2 = date4
    if date3 != None and date4 != None:
        if date1 >= date3 and date2 <= date4:
            return [date1, date2]
        elif date1 >= date3 and date2 >= date4:
            return [date1, date4]
        elif date1 <= date3 and date2 <= date4:
            return [date3, date2]
        elif date1 <= date3 and date2 >= date4:
            return [date3, date4]
    elif date3 != None and date4 == None:
        if date1 >= date3:
            return [date1, date2]
        else:
            return [date3, date2]
    elif date4 != None and date3 == None:
        if date2 <= date4:
            return [date1, date2]
        else:
            return [date1, date4]
    return [date1, date2]

def prepare_data_day(mas_avg,title=None,oxName=None,oyName=None):
    print(mas_avg)
    mas_avg1 = []
    for count,item in enumerate(mas_avg):
        info = None
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
        mas_avg1.append({"data":[],"id":count,"lineTitle":info})
        for item1 in sorted(mas_avg[item]):
            mas_avg1[count]["data"].append({"date":item1,"value":float('{:.2f}'.format(mas_avg[item][item1][0]/mas_avg[item][item1][1]))})
    # print(mas_avg1)
    return {"title":title,"oxName":oxName,"oyName":oyName,"series":mas_avg1}


# def prepare_data_month(mas_avg1):
#     # mas_avg2 = []
#     # print(mas_avg1[0]["data"][0]["date"][:7])
#     count = 0
#     mas_mon_week = []
#     for key, group in groupby(mas_avg1[0]["data"], lambda x: x["date"][:7]):
#         mas_mon_week.append([[],[],[],[],[]])
#         for item in group:
#             d = datetime.datetime(int(item["date"][:4]),int(item["date"][5:7]),int(item["date"][8:]))
#             if (d.day-1)//7+1 == 1:
#                 mas_mon_week[count][0].append(item)
#             if (d.day-1)//7+1 == 2:
#                 mas_mon_week[count][1].append(item)
#             if (d.day-1)//7+1 == 3:
#                 mas_mon_week[count][2].append(item)
#             if (d.day-1)//7+1 == 4:
#                 mas_mon_week[count][3].append(item)
#             if (d.day-1)//7+1 == 5:
#                 mas_mon_week[count][4].append(item)
#         count +=1
#         # mas_avg2.append(list(group)) #month
#     pprint.pprint(mas_mon_week)

# def prepare_data_month(mas_avg1):
#     mas_avg2 = []
#     for item in mas_avg1:
#         week_data = datetime.datetime(int(item["data"][0]["date"][:4]),int(item["data"]["date"][0][5:7]),int(item["data"]["date"][0][8:])) + datetime.timedelta(7)
#         mas_data = []
#         mas_week = []
#         for item1 in item["data"]:
#             d = datetime.datetime(int(item1["date"][:4]),int(item1["date"][5:7]),int(item1["date"][8:]))
#             if d < week_data:
#                 mas_week.append(item1["value"])
#             else:
#                 cnt = 0
#                 value = 0
#                 for cnt_cur,elem in mas_week:
#                     value += elem
#                     cnt = cnt_cur + 1
#                 mas_data.append({week_data.__str__():value/cnt})
#                 mas_week = []
#                 while d > week_data:
#                     week_data += datetime.timedelta(7)
#                 mas_week.append(item1["value"])
#

def prepare_data_week(mas_avg,title=None,oxName=None,oyName=None):
    mas_avg1 = []
    # pprint.pprint(mas_avg)
    for count,item in enumerate(mas_avg):
        info = None
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
        mas_avg1.append({"data":[],"id":count,"lineTitle":info})
        sorted_mas = sorted(mas_avg[item].keys())
        week_date = datetime.datetime(int(sorted_mas[0][:4]), int(sorted_mas[0][5:7]),int(sorted_mas[0][8:])) + datetime.timedelta(6)
        mas_week = [0,0]
        for cnt,item1 in enumerate(sorted_mas):
            d = datetime.datetime(int(item1[:4]),int(item1[5:7]),int(item1[8:]))
            if d <= week_date and cnt + 1 != len(sorted_mas):
                mas_week[0] += mas_avg[item][item1][0]
                mas_week[1] += mas_avg[item][item1][1]
            elif d <= week_date and cnt + 1 == len(sorted_mas):
                mas_week[0] += mas_avg[item][item1][0]
                mas_week[1] += mas_avg[item][item1][1]
                mas_avg1[count]["data"].append(
                    {"date": week_date.__str__(), "value": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
            elif d> week_date and cnt + 1 != len(sorted_mas):
                mas_avg1[count]["data"].append(
                    {"date": week_date.__str__(), "value": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
                mas_week = [0,0]
                while d > week_date:
                    week_date += datetime.timedelta(7)
                mas_week[0] += mas_avg[item][item1][0]
                mas_week[1] += mas_avg[item][item1][1]
            elif d> week_date and cnt + 1 == len(sorted_mas):
                mas_avg1[count]["data"].append(
                    {"date": week_date.__str__(), "value": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
                mas_week = [0, 0]
                while d > week_date:
                    week_date += datetime.timedelta(7)
                mas_week[0] += mas_avg[item][item1][0]
                mas_week[1] += mas_avg[item][item1][1]
                mas_avg1[count]["data"].append(
                    {"date": week_date.__str__(), "value": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
            else:
                print("ERROOR HAPPANED")

    return {"title":title,"oxName":oxName,"oyName":oyName,"series":mas_avg1}

def prepare_data_pie(mas_avg,title=None,oxName=None,oyName=None):
    mas_avg1 = []
    pprint.pprint(mas_avg)
    for count,item in enumerate(mas_avg):
        info = None
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
        sum = 0
        series = []
        for item3 in mas_avg[item]:
            sum += mas_avg[item][item3]
        for item4 in mas_avg[item]:
            series.append({"sector":str(item4), "size":float('{:.3f}'.format(mas_avg[item][item4] / sum))*100})
        mas_avg1.append({"info": info, "series": series})
    return mas_avg1



#Dobavit temu and type ocenki and grafik posesheniy

if __name__== "__main__":
    # mas = {subject:{data:[mark_sum,count]}}

    # start_time = time.time()
    # mas = avg_mark_region("Башкортостан")
    # print("TIME:%s",(time.time()-start_time))
    # print(mas)
    # start_time = time.time()
    # mas = avg_mark_student(0,subject_id=0, date1='2018-11-15', date2='2018-12-23')
    # print("TIME:%s", (time.time() - start_time))
    # print(mas)
    # start_time = time.time()
    # mas = avg_mark_teacher("Башкортостан", 50, subject_id=3, class_id=8)
    # print("TIME:%s", (time.time() - start_time))
    # print(mas)
    #
    # conn = psycopg2.connect("dbname=diary user=postgres password=123")
    # cur = conn.cursor()
    # sum = 0
    # start_time = datetime.datetime.now()
    # for num in range(290000):
    #     cur.execute("select * from student where id=%s",(num,))
    #     mas = cur.fetchone()[0]
    # print("TIME:%s", (datetime.datetime.now() - start_time))
    # cur.close()
    # conn.close()


    # myreg = mydb['region']
    # mas = myreg.find({}, {'areas': 1})
    # for area in mas:
    #     mas1 = area.get("areas")
    #     print(mas1)
    #     for area1 in mas1:
    #         print(mas1.get(area1).values())
    #
    # for item in mydb['school'].find({'idSchool': 300}, {'students': 1}):
    #     print('Oppa')
    #     pprint.pprint(item["students"])

    # mas = avg_mark_region("Башкортостан")
    # pprint.pprint(mas)

    # mas = avg_mark_region("Башкортостан",district="Area0",school_id=11,class_id=10, subject_id=5, date1='2017-10-17',date2='2018-12-31')
    mas = avg_mark_region("pie","Башкортостан", district="Area0")
    pprint.pprint(mas)

    # def avg_mark_student(student_id,subject_id=None,topic=None,mark_type=None,date1=None,date2=None):

    # mas = avg_mark_student(student_id=100,mark_type='Обычная',subject_id=5,topic="He looked inquisitively at his keyboard and wrote another sentence.",date1='2017-11-21',date2='2018-12-25')
    # pprint.pprint(mas)

    # def avg_mark_teacher(region,teacher_id,class_id=None,subject_id=None,topic=None,mark_type=None,date1=None,date2=None):

    # mas = avg_mark_teacher("Башкортостан",teacher_id=0,subject_id=1,topic="Where are my pants?")
    # pprint.pprint(mas)

