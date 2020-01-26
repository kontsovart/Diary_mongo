from flask import render_template, request, abort, session, redirect, url_for, Flask, Response
import json
import Build_tree
from selects_clear_v3 import avg_mark_region
import datetime
from selects_clear_v3 import prepare_data_mix_chart
import pprint
from config import mydb

app = Flask(__name__)

mytt = mydb['tmp']
mystudent = mydb['tmp_student']


@app.route('/tree')
def tree():
    print(json.dumps(Build_tree.get_tree('tree')))
    return json.dumps({'tree': Build_tree.get_tree('tree')})


@app.route('/<nodeId>/alerts')
def alerts(nodeId):
    alert = [
        {
            'id': 1,
            'redirect_id': 5,
            'redirect_type': 'school',
            'type': 'warning',
            'info': 'So high marks',
            'header': 'Attention !'
        },
        {
            'id': 2,
            'redirect_id': 4,
            'redirect_type': 'area',
            'type': 'error',
            'info': 'So low marks',
            'header': 'Make an attention !'
        }
    ]
    pprint.pprint(alert)
    return json.dumps({'alerts': alert})


# @app.route('/charts/<id>')
@app.route('/<nodeId>/statistic/')
def charts(nodeId):
    try:
        ffrom = request.form('from')
        tto = request.form('to')
        print(tto, ffrom)
    except Exception as e:
        print(e)
    print(nodeId)
    id = int(nodeId)
    ex = []
    for iter, item in enumerate(mytt.find({'id': id}, {'_id': 0, 'line': 1, 'pie': 1, 'column': 1,
                                                       'radial': 1, 'column-line-mix': 1, 'simple-column': 1})):
        for _, value in item.items():
            a = datetime.datetime.now()
            # print(a)
            # pprint.pprint(value)
            ex.append(value)
            print(datetime.datetime.now() - a)
    # print(ex)
    return json.dumps({'charts': ex})


@app.route('/<nodeId>/departments')
def all_departments(nodeId):
    print(nodeId)
    data = []
    for item in mydb['subject'].find({}, {'_id': 0, 'info': 1, 'idSubject': 1}):
        data.append({'id': item['idSubject'], 'title': item['info']})
    return json.dumps({'departments': data})


@app.route('/<nodeId>/departments/<id>')
def department(nodeId, id):
    ids = int(id)
    teachers = []
    for item in mydb['school'].find({'idSchool': int(nodeId)}, {'_id': 0, 'subject': 1}):
        # pprint.pprint(item)
        if item['subject'][ids]['idSubject'] == ids:
            for counter, teacher_id in enumerate(item['subject'][ids]['teachers']):
                # print(teacher_id)
                for teacher in mydb['teacher'].find({'idTeacher': teacher_id['teacher']}, {'_id': 0, 'first_name': 1,
                                                                                           'last_name': 1,
                                                                                           'patronymic': 1}):
                    # pprint.pprint(teacher)
                    teachers.append({'id': counter + 1, 'fio': f'{teacher["last_name"]} {teacher["first_name"]} '
                                                               f'{teacher["patronymic"]}'})
    return json.dumps({'department': sorted(teachers, key = lambda i: i['fio'])})


@app.route('/<nodeId>/departments/<depId>/teachers/<teachId>/charts')
def teachers(nodeId, depId, teachId):
    print(nodeId, depId, teachId)
    # ffrom = request.form('from')
    # tto = request.form('to')
    for item in mydb['tmp_teacher'].find({'id': f'{nodeId}_{depId}'}, {'_id': 0, 'data': 1}):
        return json.dumps({'charts': item['data']})
    return


@app.route('/<nodeId>/classes')
def class_list(nodeId):
    id = int(nodeId)
    classes = []
    for iter, item in enumerate(mystudent.find({'id': id}, {'_id': 0, 'data': 1})):
        for _, it in item.items():
            for cls in it:
                classes.append({'id': cls['id'], 'title': cls['title']})
    return json.dumps({'classes': classes})


@app.route('/<nodeId>/classes/<classId>')
def clas(nodeId, classId):
    id = int(nodeId)
    classes = []
    for iter, item in enumerate(mystudent.find({'id': id}, {'_id': 0, 'data': 1})):
        for _, it in item.items():
            for cls in it:
                if cls['id'] == int(classId):
                    for student in cls['students']:
                        classes.append({'id': student['id'], 'fio': student['fio']})
    return json.dumps({'class': classes})


@app.route('/<nodeId>/classes/<classId>/students/<stId>/charts')
def student(nodeId, classId, stId):
    print(nodeId, classId, stId)
    # ffrom = request.form('from')
    # tto = request.form('to')
    classes = []
    for iter, item in enumerate(mystudent.find({'id': int(nodeId)}, {'_id': 0, 'data': 1})):
        for _, it in item.items():
            for cls in it:
                if cls['id'] == int(classId):
                    for student in cls['students']:
                        if student['id'] == int(stId):
                            return json.dumps({'charts': student['charts']})
    return json.dumps(None)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

