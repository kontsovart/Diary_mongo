import pprint
from selects_clear_v3 import avg_mark_region
from datetime import datetime
from config import mydb


mytt = mydb['tmp']
myreg = mydb['region']

global_counter = 1

count_region = mydb['region'].count_documents({})
count_areas = len(mydb['region'].find_one({}, {'_id': 0, 'areas': 1})['areas'])
count_schools = mydb['school'].count_documents({})


def create_table_and_insert_data(area=None, school=None):
    global global_counter
    if area is not None:
        if school is not None:
            for region in myreg.find({}, {'_id': 0, 'region': 1, 'areas': 1}):
                for area, schools in region['areas'].items():
                    for i, school in enumerate(schools):
                        origin = {}
                        dic = avg_mark_region(chart_type='line', region=region['region'], district=area,
                                              school_id=i, title=f'{area} {school}')
                        dic.update({'id': f'{global_counter}_line', 'type': 'line'})
                        data_pie = avg_mark_region(chart_type='pie_student', region=region['region'],
                                                   district=area, school_id=i, title=f'{area} {school}')
                        data_pie = paint_pie(data_pie)
                        pie_dic = {}
                        pie_dic.update({'id': f'{global_counter}_pie', 'type': 'pie', 'series': data_pie,
                                        'title': 'Students', 'id_child': 0})
                        data_column = avg_mark_region(chart_type='column_student', region=region['region'],
                                                      district=area, school_id=i,
                                                      title=f'{area} {school}')
                        data_column.update({'id': f'{global_counter}_column', 'type': 'stacked-column'})
                        radial_dic = {}
                        data_vitits = avg_mark_region(chart_type='radial_visit', region=region['region'],
                                                      district=area, school_id=i,
                                                      title=f'{area} {school}')
                        radial_dic.update({'id': f'{global_counter}_radial', 'type': 'radial',
                                           'title': f'Visits 4 {area} {school}', 'series': data_vitits})
                        origin.update({'id': global_counter, 'line': dic, 'pie': pie_dic, 'column': data_column,
                                       'radial': radial_dic})
                        mytt.insert_one(origin)
                        global_counter += 1
        else:
            for region in myreg.find({}, {'_id': 0, 'region': 1, 'areas': 1}):
                for area in region['areas']:
                    origin = {}
                    dic = avg_mark_region(chart_type='line', region=region['region'],
                                          district=area, title=area)
                    dic.update({'id': f'{global_counter}_line', 'type': 'line'})
                    data_pie = avg_mark_region(chart_type='pie_student', region='Башкортостан',
                                               district=area,
                                               title=area)
                    data_pie = paint_pie(data_pie)
                    pie_dic = {}
                    pie_dic.update({'id': f'{global_counter}_pie', 'type': 'pie', 'series': data_pie,
                                    'title': 'Students', 'id_child': 0})
                    origin.update({'id': global_counter, 'line': dic, 'pie': pie_dic})
                    mytt.insert_one(origin)
                    global_counter += 1
    else:
        for region in myreg.find({}, {'_id': 0, 'region': 1}):
            origin = {}
            dic = avg_mark_region(chart_type='line', region=region['region'])
            dic.update({'id': f'{global_counter}_line', 'type': 'line'})
            data_pie = avg_mark_region(chart_type='pie_student', region=region['region'],
                                       title=region['region'])
            data_pie = paint_pie(data_pie)
            pie_dic = {}
            pie_dic.update({'id': f'{global_counter}_pie', 'type': 'pie', 'series': data_pie,
                            'title': 'Students', 'id_child': 0})
            origin.update({'id': global_counter, 'line': dic, 'pie': pie_dic})
            mytt.insert_one(origin)
            global_counter += 1
    return


def paint_pie(pie):
    for item in pie:
        if item['sector'] == 3:
            item.update({"config": {"fill": "#fcc244"}})
        elif item['sector'] == 4:
            item.update({"config": {"fill": "#ffe900"}})
        else:
            item.update({"config": {"fill": "#05c609"}})
    return pie


a = datetime.now()
create_table_and_insert_data()
b = datetime.now()
print(b - a)
create_table_and_insert_data(area=1)
c = datetime.now()
print(c - b)
create_table_and_insert_data(area=1, school=1)
print(datetime.now() - c)
