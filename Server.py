from flask import render_template, request, abort, session, redirect, url_for, Flask, Response
import json
import Build_tree
from selects import avg_mark_region
import pymongo
import datetime
import pprint

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']
mytt = mydb['tmp']
mypie = mydb['tmp_pie']
mycolumn = mydb['tmp_column']


@app.route('/tree')
def tree():
    print(json.dumps(Build_tree.get_tree('tree')))
    return json.dumps(Build_tree.get_tree('tree'))


@app.route('/charts/<id>')
def charts(id):
    print(id)
    id = int(id)
    ex = []
    counter = 1
    for iter, item in enumerate(mytt.find({'id': id}, {'_id': 0, 'title': 1, 'id': 1, 'oxName': 1, 'oyName': 1,
                                                       'series': 1, 'type': 1})):
        a = datetime.datetime.now()
        print(a)
        counter += iter
        item.update({'title': id, 'type': 'line'})
        pprint.pprint(item)
        ex.append(item)
        print(datetime.datetime.now() - a)
    print(len(ex))
    # for sub in range(6):
    #     print(id + sub)
    for iter, item in enumerate(mypie.find({'id': id, 'id_child': 0}, {'_id': 0, 'title': 1, 'id': 1,
                                                                         'series': 1, 'type': 1, 'id_child': 1})):
        print({'id': f'{id}_{item["id_child"] + counter}'})
        item.update({'id': f'{id}_{item["id_child"] + counter}'})
        # item.update({'id': counter})
        # if sub > 4:
        # return Response(status=405)
        print('opaaa')
        # item.pop('id')
        pprint.pprint(item)
        ex.append(item)
        counter += 1

    for iter, item in enumerate(mycolumn.find({'id': id}, {'_id': 0, 'title': 1, 'id': 1,
                                                                       'series': 1, 'type': 1})):
        item.update({'id': f'{id}_column', 'type': 'stacked-column'})
        # item.update({'id': counter})
        # if sub > 4:
        #     item.pop('id')
        #     return Response(status=401)
        # item.pop('series')
        pprint.pprint(item)
        ex.append(item)
        # return Response(status=405)
    # pprint.pprint(ex[-1])

            # ex.append({'id': f'{id}_last'})
    print(len(ex))
    print(ex)
    # for item in ex:
    #     print(item['id'])
    # pprint.pprint(ex)
    return json.dumps(ex)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

