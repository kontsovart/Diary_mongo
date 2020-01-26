from config import mydb


def build_tree_table(table=None):
    myreg = mydb['region']
    mytt = mydb[table]
    tree = None
    for region in myreg.find({}, {'_id': 1, 'region': 1, 'areas': 1}):
        count = 4
        tree = {'id': 1, 'name': region.get('region'), 'toggled': True, 'type': 'region', 'parent': None}
        areas = region.get('areas')
        children = []
        a_count = 1
        for area in areas:
            a_count += 1
            child_area = {'id': a_count, 'name': area, 'type': 'area', 'parent': 1}
            children_schools = []
            for school in areas.get(area):
                count += 1
                child_school = {'id': count, 'name': school, 'type': 'school', 'parent': a_count}
                children_schools.append(child_school)
            child_area.update({'children': children_schools})
            children.append(child_area)
        tree.update({'children': children})
    mytt.insert_one(tree)


build_tree_table('tree')


def get_tree(table=None):
    mytt = mydb[table]
    for item in mytt.find({}, {'_id': 0, 'id': 1, 'name': 1, 'children': 1, 'type': 1, 'parent': 1}):
        return item
