import pprint
from selects_clear import avg_mark_region, alerts_compare_mark, alerts_compare_visit
from datetime import datetime
from config import mydb
import Collect_tmp_teacher


mytt = mydb['tmp']
myreg = mydb['region']

global_counter = 1

region_alerts = {}
area_alerts = {}
school_alerts = {}

count_region = mydb['region'].count_documents({})
count_areas = len(mydb['region'].find_one({}, {'_id': 0, 'areas': 1})['areas'])
count_schools = mydb['school'].count_documents({})


def create_table_and_insert_data(area=None, school=None):
    global global_counter
    if area is not None:
        if school is not None:
            for region in myreg.find({}, {'_id': 0, 'region': 1, 'areas': 1}):
                count_area = -1
                for area, schools in region['areas'].items():
                    count_area += 1
                    for i, school in enumerate(schools):
                        make_inserts(region=region, area=area, school=school, school_id=i + count_area * len(schools),
                                     line=1, pie=1, column=1, radial=1)
        else:
            for region in myreg.find({}, {'_id': 0, 'region': 1, 'areas': 1}):
                for area in region['areas']:
                    make_inserts(region=region, area=area, line=1, pie=1)
    else:
        for region in myreg.find({}, {'_id': 0, 'region': 1}):
            make_inserts(region=region, line=1, pie=1)
    return


def make_inserts(region=None, area=None, school=None, school_id=None, line=None, pie=None, column=None, radial=None):
    global global_counter
    print(global_counter, area, school, school_id)
    origin = {'id': global_counter}
    if school is None:
        _, alert_radial = avg_mark_region('column_visit', region=region, district=area, title=f'{region} {area}')
        if area is None:
            if origin['id'] in region_alerts:
                region_alerts[origin['id']].update({'visit': alert_radial})
            else:
                region_alerts.update({origin['id']: {'visit': alert_radial}})
        elif school is None:
            if origin['id'] in region_alerts:
                area_alerts[origin['id']].update({'visit': alert_radial})
            else:
                area_alerts.update({origin['id']: {'visit': alert_radial}})
    if line is not None:
        dic, alert_line = avg_mark_region(chart_type='line', region=region['region'],
                                          district=area, school_id=school_id, title=region['region'])
        dic.update({'id': f'{global_counter}_line', 'type': 'line'})
        origin.update({'line': dic})
        # if area is None:
        #     region_alerts[origin['id']].update({'mark': alert_line})
        # elif school is None:
        #     area_alerts[origin['id']].update({'mark': alert_line})
        # else:
        #     school_alerts[origin['id']].update({'mark': alert_line})
        if area is None:
            region_alerts[origin['id']].update({'mark': alert_line})
        elif school is None:
            area_alerts[origin['id']].update({'mark': alert_line})
        else:
            school_alerts.update({origin['id']: {'mark': alert_line}})
    if pie is not None:
        data_pie = avg_mark_region(chart_type='pie_student', region=region['region'],
                                   district=area, school_id=school_id, title=region['region'])
        data_pie = paint_pie(data_pie)
        pie_dic = {}
        pie_dic.update({'id': f'{global_counter}_pie', 'type': 'pie', 'series': {'data': data_pie},
                        'title': 'Students', 'id_child': 0})
        origin.update({'pie': pie_dic})
    if column is not None:
        data_column = avg_mark_region(chart_type='column_student', region=region['region'],
                                      district=area, school_id=school_id,
                                      title=f'{area} {school}')
        data_column.update({'id': f'{global_counter}_column', 'type': 'stacked-column'})
        origin.update({'column': data_column})
    if radial is not None:
        radial_dic = {}
        data_vitits, alert_radial = avg_mark_region(chart_type='radial_visit', region=region['region'],
                                                    district=area, school_id=school_id,
                                                    title=f'{area} {school}')
        radial_dic.update({'id': f'{global_counter}_radial', 'type': 'radial',
                           'title': f'Visits 4 {area} {school}', 'series': data_vitits})
        origin.update({'radial': radial_dic})
        if area is None:
            region_alerts[origin['id']].update({'visit': alert_radial})
        elif school is None:
            area_alerts[origin['id']].update({'visit': alert_radial})
        else:
            school_alerts[origin['id']].update({'visit': alert_radial})
    mytt.insert_one(origin)
    global_counter += 1


def paint_pie(pie):
    for item in pie:
        if item['sector'] == 3:
            item.update({"config": {"fill": "#fcc244"}})
        elif item['sector'] == 4:
            item.update({"config": {"fill": "#ffe900"}})
        else:
            item.update({"config": {"fill": "#05c609"}})
    return pie


def collect_alerts():
    alerts_area = {}
    alerts_region = {}
    counter_region = 1
    print(len(region_alerts), len(area_alerts), len(school_alerts))
    for region_key, region_arg in region_alerts.items():
        counter_area = 1
        # region_key, region_arg = region.pop()
        for area_key, ar_args in area_alerts.items():
            counter_school = 1
            # if len(area):
                # area_key, ar_args = area.pop()
            if len(alerts_area) == 0:
                for school_key, args in school_alerts.items():
                    # if len(school):
                        # school_key, args = school.pop()
                    attent = []
                    # teacher_attent = []
                    for theme, school_arg in args.items():
                        if theme == 'mark':
                            attent.extend(alerts_compare_mark(ar_args[theme], school_arg))
                        else:
                            # if theme not in ar_args.keys():
                            #     ar_args.update({theme: {}})
                            attent.extend(alerts_compare_visit(ar_args[theme], school_arg))
                            pprint.pprint(attent)
                        # print(attent)
                    for course in attent:
                        course.update({'id': counter_school, 'redirect_id': school_key,
                                       'redirect_type': 'school', 'header': f'Attention ! {school_key}'})
                        if (counter_school - 1) // (count_schools // count_areas) not in alerts_area.keys():
                            alerts_area.update({(counter_school - 1) // (count_schools // count_areas): []})
                        alerts_area[(counter_school - 1) // (count_schools // count_areas)].append(course)
                    counter_area += 1
                    counter_school += 1
                    print(school_key, (school_key - count_region - count_areas) // (count_schools // count_areas))


            attent = []
            for theme, area_arg in ar_args.items():
                if theme == 'mark':
                    attent.extend(alerts_compare_mark(region_arg[theme], area_arg))
                else:
                    # if theme not in region_arg.keys():
                    #     region_arg.update({theme: {}})
                    attent.extend(alerts_compare_visit(region_arg[theme], area_arg))
                    pprint.pprint(attent)
                # print(attent)
            if len(attent):
                for att in attent:
                    att.update({'id': counter_area, 'redirect_id': area_key,
                                'redirect_type': 'area', 'header': f'Attention ! {area_key}'})
                    if counter_region not in alerts_region.keys():
                        alerts_region.update({counter_region: []})
                    alerts_region[counter_region].append(att)
                counter_area += 1
    if len(alerts_region):
        for t, value in alerts_region.items():
            mydb['alerts'].insert_one({'id': t + count_region - 1, 'data': value})
            pprint.pprint({'id': t + count_areas - 1, 'data': value})
    if len(alerts_area):
        for t, value in alerts_area.items():
            mydb['alerts'].insert_one({'id': t + count_areas - 1, 'data': value})
            pprint.pprint({'id': t + count_areas - 1, 'data': value})


a = datetime.now()
create_table_and_insert_data()
b = datetime.now()
print(b - a)
create_table_and_insert_data(area=1)
c = datetime.now()
print(c - b)
create_table_and_insert_data(area=1, school=1)
print(datetime.now() - c)
d = datetime.now()
teacher_visits, teacher_marks = Collect_tmp_teacher.create_table_and_insert_data(count_region + count_areas)
print(datetime.now() - d)
collect_alerts()
