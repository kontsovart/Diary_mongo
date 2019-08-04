import pymongo
import pprint
import json
from selects import avg_mark_region
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']
mytt = mydb['tmp']
mypie = mydb['tmp_pie']
mycolumn = mydb['tmp_column']

count_areas = 3
count_schools = 60
count_region = 1


def create_table_and_insert_data(area=None, school=None):
    if school is None:
        if area is None:
            dic = avg_mark_region(chart_type='line', region='Башкортостан')
            dic.update({'id': 1})
            # pprint.pprint(dic)
            mytt.insert_one(dic)
            data_pie = avg_mark_region(chart_type='pie_student', region='Башкортостан',
                                       title=f'Башкортостан')
            # print(len(data_pie))
            # for j, item in enumerate(data_pie):
            pie_dic = {}
            #     pprint.pprint(item)
            pie_dic.update({'id': 1, 'type': 'pie', 'series': data_pie,
                            'title': 'Students', 'id_child': 0})
            # pprint.pprint(pie_dic)
            mypie.insert_one(pie_dic)
        else:
            for i in range(count_areas):
                dic = avg_mark_region(chart_type='line', region='Башкортостан', district=f'Area{i}', title=f'Area{i}')
                dic.update({'id': 2 + i})
                mytt.insert_one(dic)
                data_pie = avg_mark_region(chart_type='pie_student', region='Башкортостан',
                                           district=f'Area{i + 1}',
                                           title=f'Area{i + 1}')
                # print(len(data_pie))
                # for j, item in enumerate(data_pie):
                pie_dic = {}
                #     pprint.pprint(item)
                pie_dic.update({'id': 2 + i, 'type': 'pie', 'series': data_pie,
                                'title': 'Students', 'id_child': 0})
                # pprint.pprint(pie_dic)
                mypie.insert_one(pie_dic)
    else:
        for i in range(count_schools):
            print(i, 5 + i, (i + 5) // 25)
            dic = avg_mark_region(chart_type='line', region='Башкортостан', district=f'Area{(i + 5) // 25}',
                                  school_id=i, title= f'Area{(i + 5) // 25} School#{i - i // 25}')
            dic.update({'id': 5 + i, 'type': 'line'})
            # pprint.pprint(dic)
            mytt.insert_one(dic)
            data_pie = avg_mark_region(chart_type='pie_student', region='Башкортостан', district=f'Area{(i + 5) // 25}',
                                       school_id=i, title= f'Area{(i + 5) // 25} School#{i - i // 25}')
            # print(len(data_pie))
            # for j, item in enumerate(data_pie):
            pie_dic = {}
            #     pprint.pprint(item)
            pie_dic.update({'id': count_areas + count_region + 1 + i, 'type': 'pie', 'series': data_pie,
                            'title': 'Students', 'id_child': 0})
                # pprint.pprint(pie_dic)
            mypie.insert_one(pie_dic)

            data_column = avg_mark_region(chart_type='column', region='Башкортостан', district=f'Area{(i + 5) // 25}',
                                       school_id=i, title=f'Area{(i + 5) // 25} School#{i - i // 25}')
            # print(len(data_pie))
            pprint.pprint(data_column)
            # for j, item in enumerate(data_column):
            #     column_dic = {}
            data_column.update({'id': count_areas + count_region + 1 + i, 'type': 'column'})
            # pprint.pprint(pie_dic)
            mycolumn.insert_one(data_column)

    return

a = datetime.now()
create_table_and_insert_data()
b = datetime.now()
print(b - a)
create_table_and_insert_data(area=1)
c = datetime.now()
print(c - b)
create_table_and_insert_data(area=1, school=1)
print(datetime.now() - c)
