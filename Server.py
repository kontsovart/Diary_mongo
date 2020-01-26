from flask import render_template, request, abort, session, redirect, url_for, Flask, Response
import json
from Build_tree import get_tree
import datetime
import pprint
from config import mydb

app = Flask(__name__)

mytt = mydb['tmp']
mystudent = mydb['tmp_student']
myalert = mydb['alerts']


def date_picker_student(nodeId, classId, studentId, graph):
    ffrom = datetime.datetime.strptime(request.args.get('from'), '%Y-%m')
    tto = datetime.datetime.strptime(request.args.get('to'), '%Y-%m')
    for iter, item in enumerate(mystudent.find({'id': int(nodeId)}, {'_id': 0,  'data': 1})):
        for _, value in item.items():
            for student in value[int(classId) - 1]['students']:
                if student['id'] == int(studentId):
                    for chart in student['charts']:
                        if chart['id'] == graph:
                            mas = chart['series']['data']
                            new_data = []
                            for line in mas:
                                if ffrom <= datetime.datetime.strptime(line['date'], '%Y-%m-%d') <= tto:
                                    new_data.append(line)
                            chart['series'].update({'data': new_data})
                            return json.dumps({'charts': chart})
    return json.dumps(None)


def date_picker(nodeId, graphId, specId=None, extra=None, type=None):
    print(nodeId, graphId, specId)
    if type is not None:
        mytmp = mydb['tmp_teacher']
        id = f'{nodeId}_{graphId}_{specId}'
    else:
        mytmp = mytt
        id = int(nodeId)
    ffrom = datetime.datetime.strptime(request.args.get('from'), '%Y-%m')
    tto = datetime.datetime.strptime(request.args.get('to'), '%Y-%m')
    for iter, item in enumerate(mytmp.find({'id': id}, {'_id': 0, 'line': 1, 'pie': 1, 'column': 1,
                                                        'radial': 1, 'column-line-mix': 1,
                                                        'simple-column': 1, 'data': 1})):
        for _, value in item.items():
            if type is not None:
                for chart in value:
                    if chart['id'] == extra:
                        mas = chart['series']['data']
                        new_data = []
                        for line in mas:
                            if ffrom <= datetime.datetime.strptime(line['date'], '%Y-%m-%d %H:%M:%S') <= tto:
                                new_data.append(line)
                        chart['series'].update({'data': new_data})
                        return json.dumps({'charts': chart})
            elif value['id'] == graphId:
                mas = value['series']['data']
                new_data = []
                for line in mas:
                    if ffrom <= datetime.datetime.strptime(line['date'], '%Y-%m-%d %H:%M:%S') <= tto:
                        new_data.append(line)
                value['series'].update({'data': new_data})
                return json.dumps({'charts': value})
    return json.dumps(None)


@app.route('/tree')
def tree():
    # print(json.dumps(get_tree('tree')))
    return json.dumps({'tree': get_tree('tree')})


@app.route('/<nodeId>/alerts')
def alerts(nodeId):
    for alrt in myalert.find({'id': int(nodeId)}, {'_id': 0, 'data': 1, 'id': 1}):
        alerts = alrt['data']
        pprint.pprint(alerts)
        return json.dumps({'alerts': alerts})
    return json.dumps(None)


@app.route('/<nodeId>/statistic/')
def charts(nodeId):
    if nodeId != 'null':
        id = int(nodeId)
        ex = []
        for iter, item in enumerate(mytt.find({'id': id}, {'_id': 0, 'line': 1, 'pie': 1, 'column': 1,
                                                           'radial': 1, 'column-line-mix': 1, 'simple-column': 1})):
            for _, value in item.items():
                a = datetime.datetime.now()
                ex.append(value)
                print(datetime.datetime.now() - a)
        print(ex)
        return json.dumps({'charts': ex})
    return json.dumps(None)


@app.route('/<nodeId>/statistic/<graphId>')
def charts_dt(nodeId, graphId):
    if request.args.get('from') is not None:
        return date_picker(nodeId, graphId)
    id = int(nodeId)
    for iter, item in enumerate(mytt.find({'id': id}, {'_id': 0, 'line': 1, 'pie': 1, 'column': 1,
                                                       'radial': 1, 'column-line-mix': 1, 'simple-column': 1})):
        for _, value in item.items():
            if value['id'] == graphId:
                return json.dumps({'charts': value})
    return json.dumps(None)


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
    print('cock', nodeId, id)
    for item in mydb['school'].find({'idSchool': int(nodeId)}, {'_id': 0, 'subject': 1}):
        if item['subject'][ids]['idSubject'] == ids:
            for counter, teacher_id in enumerate(item['subject'][ids]['teachers']):
                for teacher in mydb['teacher'].find({'idTeacher': teacher_id['teacher']}, {'_id': 0, 'first_name': 1,
                                                                                           'last_name': 1,
                                                                                           'patronymic': 1}):
                    teachers.append({'id': teacher_id['teacher'], 'fio': f'{teacher["last_name"]} '
                                                                         f'{teacher["first_name"]} '
                                                                         f'{teacher["patronymic"]}'})
    print(teachers)
    return json.dumps({'department': sorted(teachers, key = lambda i: i['fio'])})


@app.route('/<nodeId>/departments/<depId>/teachers/<teachId>/charts')
def teachers(nodeId, depId, teachId):
    print(nodeId, depId, teachId)
    for item in mydb['tmp_teacher'].find({'id': f'{nodeId}_{depId}_{teachId}'}, {'_id': 0, 'data': 1}):
        return json.dumps({'charts': item['data']})
    return json.dumps(None)


@app.route('/<nodeId>/departments/<depId>/teachers/<teachId>/charts/<chartId>')
def teachers_date(nodeId, depId, teachId, chartId):
    return date_picker(nodeId, depId, teachId, chartId, type='teacher')


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
    for iter, item in enumerate(mystudent.find({'id': int(nodeId)}, {'_id': 0, 'data': 1})):
        for _, it in item.items():
            for cls in it:
                if cls['id'] == int(classId):
                    for student in cls['students']:
                        if student['id'] == int(stId):
                            return json.dumps({'charts': student['charts']})
    return json.dumps(None)


@app.route('/<nodeId>/classes/<classId>/students/<stId>/charts/<chartId>')
def students_date(nodeId, classId, stId, chartId):
    return date_picker_student(nodeId, classId, stId, chartId)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

