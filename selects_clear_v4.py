import time
import datetime

import pprint

from config import mydb


def avg_mark_region(chart_type, region,
                    district=None, school_id=None,
                    class_id=None, subject_id=None,
                    topic=None, mark_type=None,
                    date1=None, date2=None, title=None):
    myreg = mydb['region']
    mas_ = myreg.find({}, {'areas': 1})

    areas = {}
    for area in mas_:
        areas = area.get("areas")
    date_mas = get_date_topic(subject_id, topic, date1, date2)
    mark_avg = {}

    avg_mark_district(areas, district,
                      school_id, class_id,
                      subject_id, mark_type,
                      date_mas[0], date_mas[1],
                      mark_avg, title,
                      chart_type)
    if chart_type == 'line':
        mas_avg1 = prepare_data_week(mark_avg, title=title,
                                     oxname="Date", oyname="Mark")
    elif chart_type == 'pie_mark':
        mas_avg1 = prepare_data_pie_mark(mark_avg)
    elif chart_type == "pie_student":
        mas_avg1 = prepare_data_pie_student(mark_avg)
    elif chart_type == "column_student":
        mas_avg1 = prepare_data_column_student(mark_avg, title=title,
                                               oxname="Subject", oyname="Quantity")
    elif chart_type == "pie_visit":
        mas_avg1 = prepare_data_pie_visit(mark_avg)
    elif chart_type == "column_visit":
        mas_avg1 = prepare_data_column_visit(mark_avg, title=title,
                                             oxname="Date", oyname="Mark")
    elif chart_type == "radial_visit":
        mas_avg1 = prepare_data_radial_visit(mark_avg)
    elif chart_type == "column_line_mix":
        mas_avg1 = prepare_data_column_line_mix(mark_avg)
    else:
        mas_avg1 = None
    return mas_avg1


def avg_mark_district(mas_, district,
                      school_id, class_id,
                      subject_id, mark_type,
                      date1, date2,
                      mark_avg,
                      title, chart_type):
    for area in mas_:
        if district is not None:
            if area == district:
                title += "Area " + district + " "
                avg_mark_school(mas_.get(area).values(), school_id,
                                class_id, subject_id,
                                mark_type,
                                date1, date2,
                                mark_avg,
                                title, chart_type)
        else:
            avg_mark_school(mas_.get(area).values(), school_id,
                            class_id, subject_id,
                            mark_type,
                            date1, date2,
                            mark_avg,
                            title, chart_type)


def avg_mark_school(mas_, school_id,
                    class_id, subject_id,
                    mark_type,
                    date1, date2,
                    mark_avg,
                    title, chart_type):
    for school in mas_:
        if school_id is not None:
            if school == school_id:
                title += "School " + str(school_id) + " "
                avg_mark_school_student(school, class_id,
                                        subject_id, mark_type,
                                        date1, date2,
                                        mark_avg,
                                        title, chart_type)
        else:
            avg_mark_school_student(school, class_id,
                                    subject_id, mark_type,
                                    date1, date2,
                                    mark_avg,
                                    title, chart_type)


def avg_mark_school_student(school, class_id,
                            subject_id, mark_type,
                            date1, date2,
                            mark_avg,
                            title, chart_type):
    mas_stud = []
    for item in mydb['school'].find({'idSchool': school}, {'_id': 1, 'students': 1}):
        mas_stud = item["students"]
    for student in mas_stud:
        stud_class = None
        for item in mydb['student'].find({'idStudent': student}, {'_id': 1, 'class': 1, 'subjects': 1}):
            stud_class = item
        if class_id:
            if class_id == stud_class["class"]:
                # title += "Class " + str(class_id) + " "
                if chart_type in ["line", "pie_mark", "pie_visit", "column_visit", "radial_visit", "column_line_mix"]:
                    avg_mark_subject(stud_class["subjects"], subject_id,
                                     mark_type,
                                     date1, date2,
                                     mark_avg,
                                     title, chart_type)
                elif chart_type == "pie_student" or chart_type == "column_student":
                    avg_mark_pie_column_student(stud_class["subjects"], subject_id,
                                                mark_type,
                                                date1, date2,
                                                mark_avg,
                                                title, chart_type)
        else:
            if chart_type in ["line", "pie_mark", "pie_visit", "column_visit", "radial_visit", "column_line_mix"]:
                avg_mark_subject(stud_class["subjects"], subject_id,
                                 mark_type,
                                 date1, date2,
                                 mark_avg,
                                 title, chart_type)
            elif chart_type == "pie_student" or chart_type == "column_student":
                avg_mark_pie_column_student(stud_class["subjects"], subject_id,
                                            mark_type,
                                            date1, date2,
                                            mark_avg,
                                            title, chart_type)


def avg_mark_pie_column_student(mas_, subject_id,
                                mark_type,
                                date1, date2,
                                mark_avg,
                                title, chart_type):
    mark_avg1 = {}
    avg_mark_subject(mas_, subject_id,
                     mark_type,
                     date1, date2,
                     mark_avg1,
                     title, chart_type)
    sum_mark = 0
    count_mark = 0
    if chart_type == "pie_student":
        for item in mark_avg1:
            sum_mark += mark_avg1[item]["sum_mark"]
            count_mark += mark_avg1[item]["count_mark"]
        avg_mark = sum_mark / count_mark
        if avg_mark < 3.5:
            if 3 not in mark_avg:
                mark_avg.update({3: 0})
            mark_avg[3] += 1
        if 3.5 <= avg_mark < 4.5:
            if 4 not in mark_avg:
                mark_avg.update({4: 0})
            mark_avg[4] += 1
        if avg_mark >= 4.5:
            if 5 not in mark_avg:
                mark_avg.update({5: 0})
            mark_avg[5] += 1
    elif chart_type == "column_student":
        for item in mark_avg1:
            sum_mark += mark_avg1[item]["sum_mark"]
            count_mark += mark_avg1[item]["count_mark"]
            avg_mark = sum_mark / count_mark
            if avg_mark < 3.5:
                if item not in mark_avg:
                    mark_avg.update({item: {}})
                if 3 not in mark_avg[item]:
                    mark_avg[item].update({3: 0})
                mark_avg[item][3] += 1
            if 3.5 <= avg_mark < 4.5:
                if item not in mark_avg:
                    mark_avg.update({item: {}})
                if 4 not in mark_avg[item]:
                    mark_avg[item].update({4: 0})
                mark_avg[item][4] += 1
            if avg_mark >= 4.5:
                if item not in mark_avg:
                    mark_avg.update({item: {}})
                if 5 not in mark_avg[item]:
                    mark_avg[item].update({5: 0})
                mark_avg[item][5] += 1


def avg_mark_subject(mas_, subject_id,
                     mark_type,
                     date1, date2,
                     mark_avg,
                     title, chart_type):
    for subject in mas_:
        if subject_id is not None:
            if subject["subject"] == subject_id:
                title += "Subject " + str(subject_id) + " "
                avg_mark_date(subject, mark_type,
                              date1, date2,
                              mark_avg,
                              title, chart_type)
        else:
            avg_mark_date(subject, mark_type,
                          date1, date2,
                          mark_avg,
                          title, chart_type)


def avg_mark_date(subject, mark_type,
                  date1, date2,
                  mark_avg,
                  title, chart_type):
    if subject["subject"] not in mark_avg:
        mark_avg.update({subject["subject"]: {}})
    student_visits = {}
    for mark in subject["marks"]:
        if chart_type in ["line", "pie_mark", "pie_student", "column_student"]:
            if mark["mark"]:
                if date1 and date2:
                    if date1 <= mark["date"] <= date2:
                        title += "Date of begin " + date1 + "Date of end" + date2 + " "
                        avg_mark_type(mark, subject,
                                      mark_type, mark_avg,
                                      title, chart_type)
                elif date1 and not date2:
                    if mark["date"] >= date1:
                        title += "Date of begin " + date1 + " "
                        avg_mark_type(mark, subject,
                                      mark_type, mark_avg,
                                      title, chart_type)
                elif date2 and not date1:
                    if mark["date"] <= date2:
                        title += "Date of end" + date2 + " "
                        avg_mark_type(mark, subject,
                                      mark_type, mark_avg,
                                      title, chart_type)
                else:
                    avg_mark_type(mark, subject,
                                  mark_type, mark_avg,
                                  title, chart_type)
        elif chart_type in ["pie_visit", "column_visit"]:
            if date1 and date2:
                if date1 <= mark["date"] <= date2:
                    title += "Date of begin " + date1 + "Date of end" + date2 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            elif date1 and not date2:
                if mark["date"] >= date1:
                    title += "Date of begin " + date1 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            elif date2 and not date1:
                if mark["date"] <= date2:
                    title += "Date of end" + date2 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            else:
                avg_mark_mark_pie_column_radial_visit(mark, student_visits)
        elif chart_type == "radial_visit":
            if date1 and date2:
                if date1 <= mark["date"] <= date2:
                    title += "Date of begin " + date1 + "Date of end" + date2 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            elif date1 and not date2:
                if mark["date"] >= date1:
                    title += "Date of begin " + date1 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            elif date2 and not date1:
                if mark["date"] <= date2:
                    title += "Date of end" + date2 + " "
                    avg_mark_mark_pie_column_radial_visit(mark, student_visits)
            else:
                avg_mark_mark_pie_column_radial_visit(mark, student_visits)
        elif chart_type == "column_line_mix":
            if date1 and date2:
                if date1 <= mark["date"] <= date2:
                    title += "Date of begin " + date1 + "Date of end" + date2 + " "
                    avg_mark_type(mark, subject,
                                  mark_type, mark_avg,
                                  title, chart_type)
            elif date1 and not date2:
                if mark["date"] >= date1:
                    title += "Date of begin " + date1 + " "
                    avg_mark_type(mark, subject,
                                  mark_type, mark_avg,
                                  title, chart_type)
            elif date2 and not date1:
                if mark["date"] <= date2:
                    title += "Date of end" + date2 + " "
                    avg_mark_type(mark, subject,
                                  mark_type, mark_avg,
                                  title, chart_type)
            else:
                avg_mark_type(mark, subject,
                              mark_type, mark_avg,
                              title, chart_type)
    if chart_type in ["pie_visit", "column_visit"]:
        for item in student_visits:
            for item1 in student_visits[item]:
                if item1 not in mark_avg[subject["subject"]]:
                    mark_avg[subject["subject"]].update({item1: 0})
                mark_avg[subject["subject"]][item1] += student_visits[item][item1]
    elif chart_type == "radial_visit":
        for item in student_visits:
            if item not in mark_avg[subject["subject"]]:
                mark_avg[subject["subject"]].update({item: {}})
            for item1 in student_visits[item]:
                if item1 not in mark_avg[subject["subject"]][item]:
                    mark_avg[subject["subject"]][item].update({item1: 0})
                mark_avg[subject["subject"]][item][item1] += student_visits[item][item1]


def avg_mark_type(mark, subject,
                  mark_type, mark_avg,
                  title, chart_type):
    if mark_type is not None:
        if mark["mark_type"] == mark_type:
            title += "Mark type " + mark_type + " "
            if chart_type == 'line':
                avg_mark_mark_line(mark, subject, mark_avg)
            elif chart_type == 'pie_mark':
                avg_mark_mark_circle_mark(mark, subject, mark_avg)
            elif chart_type == 'pie_student' or chart_type == "column_student":
                avg_mark_mark_circle_student(mark, subject, mark_avg)
            elif chart_type == 'column_line_mix':
                avg_mark_mark_column_line_mix(mark, subject, mark_avg)
    else:
        if chart_type == 'line':
            avg_mark_mark_line(mark, subject, mark_avg)
        elif chart_type == 'pie_mark':
            avg_mark_mark_circle_mark(mark, subject, mark_avg)
        elif chart_type == 'pie_student' or chart_type == "column_student":
            avg_mark_mark_circle_student(mark, subject, mark_avg)
        elif chart_type == 'column_line_mix':
            avg_mark_mark_column_line_mix(mark, subject, mark_avg)


def avg_mark_mark_line(mark, subject, mark_avg):
    if mark["date"] not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({mark["date"]: [0, 0]})
    mark_avg[subject["subject"]][mark["date"]][0] += mark["mark"]
    mark_avg[subject["subject"]][mark["date"]][1] += 1


def avg_mark_mark_circle_mark(mark, subject, mark_avg):
    if mark["mark"] not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({mark["mark"]: 0})
    mark_avg[subject["subject"]][mark["mark"]] += 1


def avg_mark_mark_circle_student(mark, subject, mark_avg):
    if "sum_mark" not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({"sum_mark": 0, "count_mark": 0})
    mark_avg[subject["subject"]]["sum_mark"] += mark["mark"]
    mark_avg[subject["subject"]]["count_mark"] += 1


def avg_mark_mark_pie_column_radial_visit(mark, mark_avg):
    if mark["date"] not in mark_avg:
        mark_avg.update({mark["date"]: {}})
    if mark["visit"] not in mark_avg[mark["date"]]:
        mark_avg[mark["date"]].update({mark["visit"]: 1})


def avg_mark_mark_column_line_mix(mark, subject, mark_avg):
    if mark["date"] not in mark_avg[subject["subject"]]:
        mark_avg[subject["subject"]].update({mark["date"]: {"mark": [0, 0]}})
    if mark["visit"] not in mark_avg[subject["subject"]][mark["date"]]:
        mark_avg[subject["subject"]][mark["date"]].update({mark["visit"]: 0})
    if mark["mark"]:
        mark_avg[subject["subject"]][mark["date"]]["mark"][0] += mark["mark"]
        mark_avg[subject["subject"]][mark["date"]]["mark"][1] += 1
    mark_avg[subject["subject"]][mark["date"]][mark["visit"]] += 1


def avg_mark_student(chart_type, student_id,
                     subject_id=None, topic=None,
                     mark_type=None,
                     date1=None, date2=None):
    mas_subject = None
    for item in mydb['student'].find({'idStudent': student_id}, {'_id': 1, 'subjects': 1}):
        mas_subject = item
    mark_avg = {}
    title = "Student " + str(student_id) + " "
    date_mas = get_date_topic(subject_id, topic, date1, date2)
    avg_mark_subject(mas_subject["subjects"], subject_id,
                     mark_type,
                     date_mas[0], date_mas[1],
                     mark_avg,
                     title, chart_type)
    if chart_type == "line":
        mas_avg1 = prepare_data_day(mark_avg, title=title, oxname="Date", oyname="Mark")
    elif chart_type == "column_visit":
        mas_avg1 = prepare_data_column_visit(mark_avg, title=title, oxname="Предмет", oyname="Пропуск занятий в %")
    else:
        mas_avg1 = None
    return mas_avg1


def avg_mark_teacher(chart_type, region,
                     teacher_id, class_id=None,
                     subject_id=None, topic=None,
                     mark_type=None,
                     date1=None, date2=None, title=None):
    myreg = mydb['region']
    mas_ = myreg.find({}, {'areas': 1})
    areas = {}
    for area in mas_:
        areas = area.get("areas")
    mark_avg = {}
    subject_teach = None
    for item in mydb['teacher'].find({'idTeacher': teacher_id}, {'_id': 1, 'subjects': 1}):
        subject_teach = item
    date_mas = get_date_topic(subject_id, topic, date1, date2)
    for area in areas:
        for school in areas.get(area).values():
            subjects = None
            for item in mydb['school'].find({'idSchool': school}, {'_id': 1, 'subject': 1}):
                subjects = item
            avg_mark_teacher_subject(school, subjects["subject"],
                                     subject_teach["subjects"], class_id,
                                     subject_id, teacher_id,
                                     mark_type, mark_avg,
                                     date_mas[0], date_mas[1],
                                     title, chart_type)
    if chart_type == "line":
        mas_avg1 = prepare_data_week(mark_avg, title=title, oxname="Date", oyname="Mark")
    elif chart_type == "column_visit":
        mas_avg1 = prepare_data_column_visit(mark_avg, title=title, oxname="Date", oyname="Mark")
    elif chart_type == 'column_line_mix':
        mas_avg1 = prepare_data_column_line_mix(mark_avg, title=title,
                                                oxname="Дата", oyname="Посещения",
                                                linename="Средняя оенка")
    else:
        mas_avg1 = None
    return mas_avg1


def avg_mark_teacher_subject(school, subjects,
                             subject_teach, class_id,
                             subject_id, teacher_id,
                             mark_type, mark_avg,
                             date1, date2,
                             title, chart_type):
    for subject in subjects:
        if subject_id is not None:
            if (subject["idSubject"] == subject_id) and (subject["idSubject"] in subject_teach):
                title += "Subject " + str(subject_id) + " "
                avg_mark_teacher_class(school, subject,
                                       class_id, teacher_id,
                                       mark_type, mark_avg,
                                       date1, date2,
                                       title, chart_type)
        elif subject["idSubject"] in subject_teach:
            avg_mark_teacher_class(school, subject,
                                   class_id, teacher_id,
                                   mark_type, mark_avg,
                                   date1, date2,
                                   title, chart_type)


def avg_mark_teacher_class(school, subject,
                           class_id, teacher_id,
                           mark_type, mark_avg,
                           date1, date2,
                           title, chart_type):
    for teacher in subject["teachers"]:
        if teacher_id == teacher["teacher"]:
            if class_id is not None:
                if teacher["class"] == class_id:
                    title += "Class " + str(class_id) + " "
                    avg_mark_teacher_date(teacher, school,
                                          subject, mark_type,
                                          mark_avg,
                                          date1, date2,
                                          title, chart_type)
            else:
                avg_mark_teacher_date(teacher, school,
                                      subject, mark_type,
                                      mark_avg,
                                      date1, date2,
                                      title, chart_type)


def avg_mark_teacher_date(teacher, school,
                          subject, mark_type,
                          mark_avg,
                          date1, date2,
                          title, chart_type):
    date_of_start = teacher["date_of_start"]
    date_of_end = teacher["date_of_end"]
    date_mas = compare_date(date_of_start, date_of_end, date1, date2)
    avg_mark_school_student(school, teacher["class"],
                            subject["idSubject"], mark_type,
                            date_mas[0], date_mas[1],
                            mark_avg,
                            title, chart_type)


def get_date_topic(subject_id, topic, date1, date2):
    if subject_id is not None:
        themes = []
        for item in mydb['subject'].find({'idSubject': subject_id}, {'_id': 1, 'themes': 1}):
            themes = item["themes"]
        if topic is not None:
            for theme in themes:
                if theme["theme"] == topic:
                    date_of_begin = theme["date_of_begin"]
                    date_of_end = theme["date_of_end"]
                    return compare_date(date_of_begin, date_of_end, date1, date2)
    return [date1, date2]


def compare_date(date1, date2, date3, date4):
    if date1 is None:
        date1 = date3
    if date2 is None:
        date2 = date4
    if date3 is not None and date4 is not None:
        if date1 >= date3 and date2 <= date4:
            return [date1, date2]
        elif date1 >= date3 and date2 >= date4:
            return [date1, date4]
        elif date1 <= date3 and date2 <= date4:
            return [date3, date2]
        elif date1 <= date3 and date2 >= date4:
            return [date3, date4]
    elif date3 is not None and date4 is None:
        if date1 >= date3:
            return [date1, date2]
        else:
            return [date3, date2]
    elif date4 is not None and date3 is None:
        if date2 <= date4:
            return [date1, date2]
        else:
            return [date1, date4]
    return [date1, date2]


def prepare_data_day(mas_avg, title=None, oxname=None, oyname=None):
    mas_avg1 = []
    dates = []
    titles = []
    for count, item in enumerate(mas_avg):
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
            titles.append({'title': info, 'value': f'value{count + 1}'})
        for item1 in sorted(mas_avg[item]):
            if item1 not in dates:
                dates.append(item1)
                mas_avg1.append({'date': item1})
            for i in mas_avg1:
                if item1 == i['date']:
                    i.update({f"value{count + 1}": float('{:.2f}'.format(mas_avg[item][item1][0] /
                                                                         mas_avg[item][item1][1]))})
    return {"title": title, "oxName": oxname, "oyName": oyname, "series": {'titles': titles,
                                                                           'data': sorted(mas_avg1,
                                                                                          key=lambda ii: ii['date'])}}


# def prepare_data_week(mas_avg, title=None, oxname=None, oyname=None):
#     # mas_avg1 = []
#     titles = []
#     data = []
#     pprint.pprint(mas_avg)
#     for count, item in enumerate(mas_avg):
#         info = None
#         for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
#             info = item2["info"]
#         titles.append({'title': info, 'value': f'value{count+1}'})
#         sorted_mas = sorted(mas_avg[item].keys())
#         week_date = datetime.datetime(int(sorted_mas[0][:4]),
#                                       int(sorted_mas[0][5:7]),
#                                       int(sorted_mas[0][8:])) + datetime.timedelta(6)
#         mas_week = [0, 0]
#         for cnt, item1 in enumerate(sorted_mas):
#             d = datetime.datetime(int(item1[:4]), int(item1[5:7]), int(item1[8:]))
#             if d <= week_date and cnt + 1 != len(sorted_mas):
#                 mas_week[0] += mas_avg[item][item1][0]
#                 mas_week[1] += mas_avg[item][item1][1]
#             elif d <= week_date and cnt + 1 == len(sorted_mas):
#                 mas_week[0] += mas_avg[item][item1][0]
#                 mas_week[1] += mas_avg[item][item1][1]
#                 data.append(
#                     {"date": week_date.__str__(),
#                      f"value{count + 1}": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
#             elif d > week_date and cnt + 1 != len(sorted_mas):
#                 data.append(
#                     {"date": week_date.__str__(),
#                      f"value{count + 1}": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
#                 mas_week = [0, 0]
#                 while d > week_date:
#                     week_date += datetime.timedelta(7)
#                 mas_week[0] += mas_avg[item][item1][0]
#                 mas_week[1] += mas_avg[item][item1][1]
#             elif d > week_date and cnt + 1 == len(sorted_mas):
#                 data.append(
#                     {"date": week_date.__str__(),
#                      f"value{count + 1}": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
#                 mas_week = [0, 0]
#                 while d > week_date:
#                     week_date += datetime.timedelta(7)
#                 mas_week[0] += mas_avg[item][item1][0]
#                 mas_week[1] += mas_avg[item][item1][1]
#                 data.append(
#                     {"date": week_date.__str__(),
#                      f"value{count + 1}": float('{:.2f}'.format(mas_week[0] / mas_week[1]))})
#             else:
#                 print("ERROOR HAPPANED")
#     pprint.pprint(data)
#     origin_data = []
#     for cnt, item in enumerate(data):
#         if 'value1' in item.keys():
#             origin_data.append(item)
#         else:
#             for it in origin_data:
#                 if it['date'] == item['date']:
#                     it.update(item)
#
#     return {"title": title, "oxName": oxname, "oyName": oyname, "series": {'titles': titles, 'data': origin_data}}


def prepare_data_week(mas_avg, title=None, oxname=None, oyname=None):
    # mas_avg1 = []
    titles = []
    data = []
    # pprint.pprint(mas_avg)
    sorted_mas = []
    mas_week = {}
    for count, item in enumerate(mas_avg):
        info = None
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
        titles.append({'title': info, 'value': f'value{count+1}'})
        mas_week.update({f'value{count+1}': None})
        for item3 in mas_avg[item]:
            sorted_mas.append({"date": item3, "value": f'value{count+1}', "data": mas_avg[item][item3]})
    sorted_mas1 = sorted(sorted_mas, key=lambda ii: ii['date'])
    week_date = datetime.datetime(int(sorted_mas1[0]["date"][:4]),
                                  int(sorted_mas1[0]["date"][5:7]),
                                  int(sorted_mas1[0]["date"][8:])) + datetime.timedelta(6)
    mas_week1 = mas_week.copy()
    for cnt, item1 in enumerate(sorted_mas1):
        d = datetime.datetime(int(item1["date"][:4]), int(item1["date"][5:7]), int(item1["date"][8:]))
        if d <= week_date and cnt + 1 != len(sorted_mas1):
            if mas_week1[item1["value"]] is None:
                mas_week1[item1["value"]] = [0, 0]
            mas_week1[item1["value"]][0] += item1["data"][0]
            mas_week1[item1["value"]][1] += item1["data"][1]
        elif d <= week_date and cnt + 1 == len(sorted_mas1):
            if mas_week1[item1["value"]] is None:
                mas_week1[item1["value"]] = [0, 0]
            mas_week1[item1["value"]][0] += item1["data"][0]
            mas_week1[item1["value"]][1] += item1["data"][1]
            for item4 in mas_week1:
                if mas_week1[item4] is not None:
                    mas_week1[item4] = float('{:.2f}'.format(mas_week1[item4][0] / mas_week1[item4][1]))
            mas_week1.update({"date": week_date.__str__()})
            data.append(mas_week1)
        elif d > week_date and cnt + 1 != len(sorted_mas1):
            for item4 in mas_week1:
                if mas_week1[item4] is not None:
                    mas_week1[item4] = float('{:.2f}'.format(mas_week1[item4][0] / mas_week1[item4][1]))
            mas_week1.update({"date": week_date.__str__()})
            data.append(mas_week1)
            mas_week1 = mas_week.copy()
            while d > week_date:
                week_date += datetime.timedelta(7)
            if mas_week1[item1["value"]] is None:
                mas_week1[item1["value"]] = [0, 0]
            mas_week1[item1["value"]][0] += item1["data"][0]
            mas_week1[item1["value"]][1] += item1["data"][1]
        elif d > week_date and cnt + 1 == len(sorted_mas1):
            for item4 in mas_week1:
                if mas_week1[item4] is not None:
                    mas_week1[item4] = float('{:.2f}'.format(mas_week1[item4][0] / mas_week1[item4][1]))
            mas_week1.update({"date": week_date.__str__()})
            data.append(mas_week1)
            mas_week1 = mas_week.copy()
            while d > week_date:
                week_date += datetime.timedelta(7)
            if mas_week1[item1["value"]] is None:
                mas_week1[item1["value"]] = [0, 0]
            mas_week1[item1["value"]][0] += item1["data"][0]
            mas_week1[item1["value"]][1] += item1["data"][1]
            for item4 in mas_week1:
                if mas_week1[item4] is not None:
                    mas_week1[item4] = float('{:.2f}'.format(mas_week1[item4][0] / mas_week1[item4][1]))
            mas_week1.update({"date": week_date.__str__()})
            data.append(mas_week1)
            mas_week1 = mas_week.copy()
        else:
            print("ERROOR HAPPANED")
    return {"title": title, "oxName": oxname, "oyName": oyname, "series": {'titles': titles, 'data': data}}


def prepare_data_pie_mark(mas_avg):
    mas_avg1 = []
    for count, item in enumerate(mas_avg):
        info = None
        for item2 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item2["info"]
        sum_ = 0
        series = []
        for item3 in mas_avg[item]:
            sum_ += mas_avg[item][item3]
        for item4 in mas_avg[item]:
            series.append({"sector": str(item4),
                           "size": float('{:.3f}'.format(mas_avg[item][item4] / sum_))})
        mas_avg1.append({"info": info, "series": series})
    return mas_avg1


def prepare_data_pie_student(mas_avg):
    series = []
    for item in mas_avg:
        series.append({"sector": item, "size": mas_avg[item]})
    return series


def prepare_data_column_student(mas_avg, title=None, oxname=None, oyname=None):
    series = {}
    series.update({"titles": [{"title": "C-student", "value": "value1"},
                              {"title": "B-student", "value": "value2"},
                              {"title": "A-student", "value": "value3"}]})
    data = []
    for item in mas_avg:
        info = None
        for item1 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item1["info"]
        data1 = {}
        data1.update({"value1": None, "value2": None, "value3": None})
        for item2 in mas_avg[item]:
            if item2 == 3:
                data1.update({"value1": mas_avg[item][item2]})
            if item2 == 4:
                data1.update({"value2": mas_avg[item][item2]})
            if item2 == 5:
                data1.update({"value3": mas_avg[item][item2]})
        data1.update({"category": info})
        data.append(data1)
    series.update({"data": data})
    return {"title": title, "oxName": oxname, "oyName": oyname, "series": series}


def prepare_data_pie_visit(mas_avg):
    series = []
    data = {}
    for item in mas_avg:
        for item1 in mas_avg[item]:
            if item1 not in data:
                data.update({item1: 0})
            data[item1] += mas_avg[item][item1]
    for item2 in data:
        series.append({"sector": item2, "size": data[item2]})
    return series


def prepare_data_column_visit(mas_avg, title=None, oxname=None, oyname=None):
    # series = {}
    data = []
    for item in mas_avg:
        info = None
        for item1 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item1["info"]
        minn = 0
        maxx = 0
        for item2 in mas_avg[item]:
            # if item2 == "Уважительная причина":
            #     min += mas_avg[item][item2]
            if item2 == "Не уважительная причина":
                minn += mas_avg[item][item2]
            maxx += mas_avg[item][item2]
        data.append({"category": info, 'value': minn/maxx * 100})
    return {"title": title, "oxName": oxname, "oyName": oyname, "series": {'data': data}, 'type': 'simple_column'}


def prepare_data_radial_visit(mas_avg):
    series = {}
    series.update({"titles": []})
    data = {}
    mas_week1 = {}
    percent_visit = {}
    for item in mas_avg:
        info = None
        for item3 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item3["info"]
        value = "value" + str(item + 1)
        series["titles"].append({"title": info, "value": value})
        mas_week1.update({value: None})
        percent_visit.update({info: [0, 0, 0]})
        for item1 in mas_avg[item]:
            if item1 not in data:
                data.update({item1: {}})
            if value not in data[item1]:
                data[item1].update({value: 0})
            for item2 in mas_avg[item][item1]:
                if item2 == 'Был':
                    percent_visit[info][0] += mas_avg[item][item1][item2]
                if item2 == "Уважительная причина":
                    percent_visit[info][1] += mas_avg[item][item1][item2]
                    data[item1][value] += mas_avg[item][item1][item2]
                elif item2 == "Не уважительная причина":
                    percent_visit[info][2] += mas_avg[item][item1][item2]
                    data[item1][value] += mas_avg[item][item1][item2]
    for item5 in percent_visit:
        percent_visit[item5] = float('{:.3f}'.format(percent_visit[item5][0] / (
                                                     percent_visit[item5][0] +
                                                     percent_visit[item5][1] +
                                                     percent_visit[item5][2])))
    sorted_mas = sorted(data.keys())
    week_date = datetime.datetime(int(sorted_mas[0][:4]),
                                  int(sorted_mas[0][5:7]),
                                  int(sorted_mas[0][8:])) + datetime.timedelta(6)
    mas_week = mas_week1.copy()
    data1 = []
    for cnt, item1 in enumerate(sorted_mas):
        d = datetime.datetime(int(item1[:4]), int(item1[5:7]), int(item1[8:]))
        if d <= week_date and cnt + 1 != len(sorted_mas):
            for item4 in data[item1]:
                if mas_week[item4] is None:
                    mas_week[item4] = 0
                mas_week[item4] += data[item1][item4]
        elif d <= week_date and cnt + 1 == len(sorted_mas):
            for item4 in data[item1]:
                if mas_week[item4] is None:
                    mas_week[item4] = 0
                mas_week[item4] += data[item1][item4]
            mas_week.update({"date": week_date.__str__()})
            data1.append(mas_week)
        elif d > week_date and cnt + 1 != len(sorted_mas):
            mas_week.update({"date": week_date.__str__()})
            data1.append(mas_week)
            mas_week = mas_week1.copy()
            while d > week_date:
                week_date += datetime.timedelta(7)
            for item4 in data[item1]:
                if mas_week[item4] is None:
                    mas_week[item4] = 0
                mas_week[item4] += data[item1][item4]
        elif d > week_date and cnt + 1 == len(sorted_mas):
            mas_week.update({"date": week_date.__str__()})
            data1.append(mas_week)
            mas_week = mas_week1.copy()
            while d > week_date:
                week_date += datetime.timedelta(7)
            for item4 in data[item1]:
                if mas_week[item4] is None:
                    mas_week[item4] = 0
                mas_week[item4] += data[item1][item4]
            mas_week.update({"date": week_date.__str__()})
            data1.append(mas_week)
            mas_week = mas_week1.copy()
        else:
            print("ERROOR HAPPANED")
    series.update({"data": data1})
    return [series, percent_visit]


def prepare_data_column_line_mix(mas_avg, title=None, oxname=None, oyname=None, linename=None):
    all_subjects = {}
    mas_week1 = {}
    for item in mas_avg:
        info = None
        for item3 in mydb['subject'].find({'idSubject': item}, {'_id': 1, 'info': 1}):
            info = item3["info"]
        all_subjects.update({info: {}})
        sorted_mas = sorted(mas_avg[item].keys())
        week_date = datetime.datetime(int(sorted_mas[0][:4]),
                                      int(sorted_mas[0][5:7]),
                                      int(sorted_mas[0][8:])) + datetime.timedelta(6)
        mas_week = {"value1": None, "value2": None, "value3": None, "lineY": None}
        data1 = []
        for cnt, item1 in enumerate(sorted_mas):
            d = datetime.datetime(int(item1[:4]), int(item1[5:7]), int(item1[8:]))
            if d <= week_date and cnt + 1 != len(sorted_mas):
                for item4 in mas_avg[item][item1]:
                    if item4 == "mark" and mas_week["lineY"] is None:
                        mas_week.update({"lineY": [0, 0]})
                    elif item4 == "mark" and mas_week["lineY"] is not None:
                        mas_week["lineY"][0] += mas_avg[item][item1][item4][0]
                        mas_week["lineY"][1] += mas_avg[item][item1][item4][1]
                    if item4 == 'Был':
                        if mas_week["value1"] is None:
                            mas_week["value1"] = 0
                        mas_week["value1"] += mas_avg[item][item1][item4]
                    elif item4 == 'Уважительная причина':
                        if mas_week["value2"] is None:
                            mas_week["value2"] = 0
                        mas_week["value2"] += mas_avg[item][item1][item4]
                    elif item4 == 'Не уважительная причина':
                        if mas_week["value3"] is None:
                            mas_week["value3"] = 0
                        mas_week["value3"] += mas_avg[item][item1][item4]

            elif d <= week_date and cnt + 1 == len(sorted_mas):
                for item4 in mas_avg[item][item1]:
                    if item4 == "mark" and mas_week["lineY"] is None:
                        mas_week.update({"lineY": [0, 0]})
                    elif item4 == "mark" and mas_week["lineY"] is not None:
                        mas_week["lineY"][0] += mas_avg[item][item1][item4][0]
                        mas_week["lineY"][1] += mas_avg[item][item1][item4][1]
                    if item4 == 'Был':
                        if mas_week["value1"] is None:
                            mas_week["value1"] = 0
                        mas_week["value1"] += mas_avg[item][item1][item4]
                    elif item4 == 'Уважительная причина':
                        if mas_week["value2"] is None:
                            mas_week["value2"] = 0
                        mas_week["value2"] += mas_avg[item][item1][item4]
                    elif item4 == 'Не уважительная причина':
                        if mas_week["value3"] is None:
                            mas_week["value3"] = 0
                        mas_week["value3"] += mas_avg[item][item1][item4]
                mas_week.update({"date": week_date.__str__()})
                mas_week["lineY"] = float('{:.3f}'.format(mas_week["lineY"][0] / mas_week["lineY"][1]))
                data1.append(mas_week)
                mas_week = {"value1": None, "value2": None, "value3": None, "lineY": None}
            elif d > week_date and cnt + 1 != len(sorted_mas):
                mas_week.update({"date": week_date.__str__()})
                mas_week["lineY"] = float('{:.3f}'.format(mas_week["lineY"][0] / mas_week["lineY"][1]))
                data1.append(mas_week)
                mas_week = {"value1": None, "value2": None, "value3": None, "lineY": None}
                while d > week_date:
                    week_date += datetime.timedelta(7)
                for item4 in mas_avg[item][item1]:
                    if item4 == "mark" and mas_week["lineY"] is None:
                        mas_week.update({"lineY": [0, 0]})
                    elif item4 == "mark" and mas_week["lineY"] is not None:
                        mas_week["lineY"][0] += mas_avg[item][item1][item4][0]
                        mas_week["lineY"][1] += mas_avg[item][item1][item4][1]
                    if item4 == 'Был':
                        if mas_week["value1"] is None:
                            mas_week["value1"] = 0
                        mas_week["value1"] += mas_avg[item][item1][item4]
                    elif item4 == 'Уважительная причина':
                        if mas_week["value2"] is None:
                            mas_week["value2"] = 0
                        mas_week["value2"] += mas_avg[item][item1][item4]
                    elif item4 == 'Не уважительная причина':
                        if mas_week["value3"] is None:
                            mas_week["value3"] = 0
                        mas_week["value3"] += mas_avg[item][item1][item4]
            elif d > week_date and cnt + 1 == len(sorted_mas):
                mas_week.update({"date": week_date.__str__()})
                mas_week["lineY"] = float('{:.3f}'.format(mas_week["lineY"][0] / mas_week["lineY"][1]))
                data1.append(mas_week)
                mas_week = {"value1": None, "value2": None, "value3": None, "lineY": None}
                while d > week_date:
                    week_date += datetime.timedelta(7)
                for item4 in mas_avg[item][item1]:
                    if item4 == "mark" and mas_week["lineY"] is None:
                        mas_week.update({"lineY": [0, 0]})
                    elif item4 == "mark" and mas_week["lineY"] is not None:
                        mas_week["lineY"][0] += mas_avg[item][item1][item4][0]
                        mas_week["lineY"][1] += mas_avg[item][item1][item4][1]
                    if item4 == 'Был':
                        if mas_week["value1"] is None:
                            mas_week["value1"] = 0
                        mas_week["value1"] += mas_avg[item][item1][item4]
                    elif item4 == 'Уважительная причина':
                        if mas_week["value2"] is None:
                            mas_week["value2"] = 0
                        mas_week["value2"] += mas_avg[item][item1][item4]
                    elif item4 == 'Не уважительная причина':
                        if mas_week["value3"] is None:
                            mas_week["value3"] = 0
                        mas_week["value3"] += mas_avg[item][item1][item4]
                mas_week.update({"date": week_date.__str__()})
                mas_week["lineY"] = float('{:.3f}'.format(mas_week["lineY"][0] / mas_week["lineY"][1]))
                data1.append(mas_week)
                mas_week = {"value1": None, "value2": None, "value3": None, "lineY": None}
            else:
                print("ERROOR HAPPANED")
            all_subjects[info].update({'oxName': oxname, 'oyName': oyname,
                                       'lineName': linename, 'title': title,
                                       'type': 'column_line_mix',
                                       'series': {"titles": [{'title': 'Был', 'value': 'value1'},
                                                             {'title': 'Уважительная причина', 'value': 'value2'},
                                                             {'title': 'Не уважительная причина', 'value': 'value3'}],
                                                  'data': data1}})
    return all_subjects


# def prepare_data_mix_chart(mas_avg, title=None, oxname=None, oyname=None, linename=None, id_teacher=None):
#     mark_mas = {}
#     visit_mas = {'Был': 0, 'Уважительная причина': 0, 'Не уважительная причина': 0}
#     visit_templ = {}
#     global_mas = {'oxName': oxname, 'oyName': oyname, 'lineName': linename, 'title': title, 'type': 'column-line-mix',
#                   'series': {"titles": [{'title': 'Был', 'value': 'value1'},
#                                         {'title': 'Уважительная причина', 'value': 'value2'},
#                                         {'title': 'Не уважительная причина', 'value': 'value3'}],
#                              'data': []}}
#     for school_id in mas_avg:
#         for sch in mydb['school'].find({'idSchool': school_id}, {'_id': 0, 'subject': 1, 'students': 1}):
#             for sub in sch['subject']:
#                 for teacher in sub['teachers']:
#                     if id_teacher and id_teacher == teacher['teacher']:
#                         # print('origin is down')
#                         # print({'id': f'{school_id + 5}_{sub["idSubject"]}_{id_teacher}'})
#                         for student in sch['students']:
#                             for item in mydb['student'].find({'idStudent': student, 'class': teacher['class']},
#                                                              {'_id': 0, 'class': 1, 'subjects': 1}):
#                                 for mark in item['subjects']:
#                                     if mark['subject'] == sub['idSubject']:
#                                         for val in mark['marks']:
#                                             a = datetime.datetime.strptime(val['date'], '%Y-%m-%d')
#                                             no_year = datetime.datetime.isocalendar(a)[0]
#                                             no_week = datetime.datetime.isocalendar(a)[1]
#                                             # Kostil
#                                             st = datetime.timedelta(weeks=no_week)
#                                             dt = datetime.datetime(year=no_year, month=1, day=1)
#                                             total = st.total_seconds() + time.mktime(dt.timetuple())
#                                             no_week = datetime.datetime.fromtimestamp(total).strftime('%Y-%m-%d')
#                                             # End of kostil
#                                             if no_week not in visit_templ.keys():
#                                                 visit_templ.update({no_week: visit_mas.copy()})
#                                             visit_templ[no_week].update(
#                                                 {val['visit']: visit_templ[no_week][val['visit']] + 1})
#                                             if val['mark'] is not None:
#                                                 if no_week in mark_mas.keys():
#                                                     mark_mas.update({no_week: (mark_mas[no_week] + val['mark']) / 2})
#                                                 else:
#                                                     mark_mas.update({no_week: val['mark']})
#                         # global_mas.update({teacher['teacher']: {'line': mark_mas, 'column': visit_templ}})
#                         correct_data = []
#                         # pprint.pprint(mark_mas)
#                         # pprint.pprint(visit_templ)
#                         for i in sorted(visit_templ.keys()):
#                             # print(i + 1)
#                             if i not in mark_mas.keys():
#                                 mark_mas.update({i: None})
#                             correct_data.append({'date': i, 'value1': visit_templ[i]['Был'],
#                                                  'value2': visit_templ[i]['Уважительная причина'],
#                                                  'value3': visit_templ[i]['Не уважительная причина'],
#                                                  'lineY': mark_mas[i]})
#                             # pprint.pprint(correct_data)
#                         if len(correct_data) == 0:
#                             print('OMAGAAAAD')
#                             pprint.pprint(teacher)
#                             pprint.pprint(sub)
#                         global_mas['series'].update({'data': correct_data})
#                         mark_mas = {}
#                         visit_templ = {}
#                 # pprint.pprint(global_mas)
#                 return global_mas


def alerts_get_avg_line(mas_avg):
    sub = {}
    for item in mas_avg["series"]["titles"]:
        sub.update({item["value"]: 0})
    for count, item1 in enumerate(mas_avg["series"]["data"]):
        for item2 in item1:
            if item2 in sub:
                sub[item2] += item1[item2]
        if count + 1 == len(mas_avg["series"]["data"]):
            for item3 in sub:
                sub[item3] = float('{:.3f}'.format(sub[item3] / (count + 1)))
    sub1 = {}
    for item in mas_avg["series"]["titles"]:
        sub1.update({item["title"]: sub[item["value"]]})
    return sub1


# def alerts_compare_line(sub_big, sub_small):
#     alert_bool = {}
#     print(sub_big, sub_small)
#     for item in sub_small:
#         mark = sub_big.get(item)
#         if mark is not None:
#             print(item, mark, sub_small[item])
#             if 0 < (mark - sub_small[item]) >= 0.5:
#                 alert_bool.update({item: {"low": True, "hight": False}})
#             elif (mark - sub_small[item]) <= -0.5:
#                 alert_bool.update({item: {"low": False, "hight": True}})
#             else:
#                 alert_bool.update({item: {"low": False, "hight": False}})
#     return alert_bool


def alerts_compare_line(sub_big, sub_small):
    alert_bool = {}
    print(sub_big, sub_small)
    for item in sub_small:
        mark = sub_big.get(item)
        if mark is not None:
            print(item, mark, sub_small[item])
            if 0 < (mark - sub_small[item]) >= 0.5:
                alert_bool.update({'type': 'warning',
                                   'info': 'Low marks '+item})
            elif (mark - sub_small[item]) <= -0.5:
                alert_bool.update({'type': 'warning',
                                   'info': 'Hight marks '+item})
            else:
                pass
    return alert_bool


def alerts_compare_radial(sub_big, sub_small):
    alert_bool = {}
    print(sub_big, sub_small)
    for item in sub_small:
        percent = sub_big.get(item)
        if percent is not None:
            print(item, percent, sub_small[item])
            if 0 < (percent - sub_small[item]) >= 0.001:
                alert_bool.update({'type': 'warning',
                                   'info': 'Low visits ' + item})
            else:
                pass
    return alert_bool


if __name__ == "__main__":
    # mas = avg_mark_region("Башкортостан")
    # pprint.pprint(mas)

    # mas = avg_mark_region("Башкортостан",district="Area0",
    #                       school_id=11,class_id=10,
    #                       subject_id=5,
    #                       date1='2017-10-17',date2='2018-12-31')

    # mas = avg_mark_region("radial_visit", "Башкортостан", district="Area0")
    # pprint.pprint(mas)

    # mas = avg_mark_student(student_id=100,mark_type='Обычная',
    #                        subject_id=5,
    #                        topic="He looked inquisitively at his keyboard and wrote another sentence.",
    #                        date1='2017-11-21',date2='2018-12-25')
    # pprint.pprint(mas)

    # mas = avg_mark_student("line", student_id=100)
    # org = {'id': 5, 'simple_column': mas}
    # pprint.pprint(mas)
    # mydb['tmp'].insert_one(org)

    # dic = avg_mark_region(chart_type='column_line_mix', region="Башкортостан",
    #                       district='Area1', school_id=22, title="Башкортостан")
    # dic.update({'id': f'{1}_line', 'type': 'line'})
    # pprint.pprint(dic)

    # mas = avg_mark_teacher("Башкортостан",teacher_id=0,subject_id=1,topic="Where are my pants?")
    # pprint.pprint(mas)

    # mas = prepare_data_mix_chart([30], title='Mix chart', oxname='Date', oyname='% of student',
    #                              linename='AVG mark', id_teacher=429)
    # mas.update({'id': '5_mix'})

    # mydb['tmp'].insert_one({'column-line-mix': mas})

    # mas1 = avg_mark_region("line", "Башкортостан", district="Area0", title="")
    # # pprint.pprint(mas1)
    # for i in range(20):
    #     mas = avg_mark_region("line", "Башкортостан", district="Area0", school_id=i, title="")
    #     print(i)
    #     if i == 9:
    #         pprint.pprint(mas)
    #     # pprint.pprint(mas)
    #     pprint.pprint(alerts_compare_line(alerts_get_avg_line(mas1), alerts_get_avg_line(mas)))

    mas = avg_mark_region("radial_visit", "Башкортостан", title="")
    pprint.pprint(mas)

    for i in range(20):
        mas1 = avg_mark_region("radial_visit", "Башкортостан", district="Area0", school_id=i, title="")
        print(i)
        print(alerts_compare_radial(mas[1], mas1[1]))
