import pprint
from selects_clear import avg_mark_region , avg_mark_student
from datetime import datetime
from config import mydb


mytt = mydb['tmp_student']
myschool = mydb['school']
mystudent = mydb['student']

count_schools = mydb['school'].count_documents({})
student_visits = {}
student_marks = {}


def create_table_and_insert_data(id_school):
    print('Schoool == ', id_school)
    origin = []
    counter_of_class = {}
    for i in range(11):
        origin.append({'id': i+1, 'title': i + 1, 'students': []})
        counter_of_class.update({i + 1: 0})
    for school in myschool.find({'idSchool': id_school}, {'_id': 0, 'students': 1}):
        for student_id in school['students']:
            # print(student_id)
            for item in mystudent.find({'idStudent': student_id}, {'_id': 0, 'first_name': 1, 'last_name': 1,
                                                                   'patronymic': 1, 'class': 1}):
                # pprint.pprint(item)
                # pprint.pprint(school)

                counter_of_class[item['class']] += 1
                charts = []
                if id_school not in student_marks.keys():
                    student_marks.update({id_school: []})
                if id_school not in student_visits.keys():
                    student_visits.update({id_school: []})
                mas, marks = avg_mark_student('line', student_id=student_id)
                mas.update({'id': f'{id_school}_{counter_of_class[item["class"]]}_{student_id}_{0}', 'type': 'line'})
                charts.append(mas)
                mas_st, visits = avg_mark_student("column_visit", student_id=student_id)
                mas_st.update({'id': f'{id_school}_{counter_of_class[item["class"]]}_{student_id}_{1}'})
                charts.append(mas_st)
                student_marks[id_school].append(marks)
                student_visits[id_school].append(visits)
                student = {'id': counter_of_class[item['class']],
                           'fio': f'{item["last_name"]} {item["first_name"]} {item["patronymic"]}',
                           'charts': charts}
                origin[item['class'] - 1]['students'].append(student)
        # pprint.pprint(origin)
    for counter, it in enumerate(origin):
        if len(it['students']) == 0:
            origin.pop(counter)
    # pprint.pprint(origin)
    if id_school == 60:
        pprint.pprint(origin)
    mytt.insert_one({'id': id_school, 'data': origin})
    return


def collect_student_graphs():
    for i in range(count_schools):
        print(i + 1)
        create_table_and_insert_data(i + 1)
    return [student_visits, student_marks]


if __name__ == '__main__':
    # pprint.pprint(collect_student_graphs())
    a, b = collect_student_graphs()
    print(len(a), len(b))
