import pprint
from selects_clear import avg_mark_teacher
from datetime import datetime
from config import mydb


mytt = mydb['tmp_teacher']
myalerts = mydb['alerts']
myreg = mydb['region']
myteacher = mydb['teacher']
myschool = mydb['school']


def create_table_and_insert_data(global_counter):
    a = datetime.now()
    teacher_visits = {}
    teacher_marks = {}
    for sch in myschool.find({}, {'_id': 0, 'subject': 1, 'idSchool': 1}):
        print(sch['idSchool'])
        tter = []
        for subj in sch['subject']:
            for teacher in subj['teachers']:
                if teacher['teacher'] in tter:
                    pass
                else:
                    tter.append(teacher['teacher'])
                    mas, visits, marks = avg_mark_teacher('column_line_mix', "Башкортостан", school_id=sch['idSchool'],
                                                          teacher_id=teacher["teacher"], title='')
                    if sch['idSchool'] not in teacher_marks.keys():
                        teacher_marks.update({sch['idSchool']: []})
                    if sch['idSchool'] not in teacher_visits.keys():
                        teacher_visits.update({sch['idSchool']: []})
                    teacher_marks[sch['idSchool']].append(marks)
                    teacher_visits[sch['idSchool']].append(visits)
                    origin = []
                    cnt = 0
                    for title, value in mas.items():
                        for it in mydb['subject'].find({'idSubject': subj['idSubject']}, {'_id': 0, 'info': 1}):
                            if title == it['info']:
                                value['title'] = title
                                value.update({'id': f'{sch["idSchool"] + global_counter}_{subj["idSubject"]}'
                                                    f'_{teacher["teacher"]}_{cnt}', 'type': 'column-line-mix'})
                                origin.append(value)
                                cnt += 1
                # mytt.insert_one({'id': f'{sch["idSchool"] + global_counter}_{subj["idSubject"]}_{teacher["teacher"]}',
                    #                  'data': origin})
        print(datetime.now() - a)
    print(datetime.now() - a)
    return [teacher_visits, teacher_marks]


if __name__ == '__main__':
    global_counter = 2 + len(mydb['region'].find_one({}, {'_id': 0, 'areas': 1})['areas'])
    create_table_and_insert_data(global_counter)
