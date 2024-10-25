def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

"""
l1, l2: {'id':'id1', 'barcodes': {'P5':[...]}} 
"""
def get_conflicts(l1, l2, min_distance=2):
#     print('test distance {} + {}'.format(l1,l2))
    conflicts = []
    for k in l1['barcodes'].keys():
#         print('barcodes {}'.format(k))
        if k in l2['barcodes']:
            for s1 in l1['barcodes'][k]:
                for s2 in l2['barcodes'][k]:
                    d = hamming_distance(s1, s2)
                    if d < min_distance:
                        print('hamming distance {} - {} = {}'.format(s1,s2,d))
                        conflicts.append({l1['id']: s1, l2['id']: s2, 'distance': d})
    return conflicts
#     if len(conflicts) > 0:
#         errors = {l1['id']: {l2['id']:[]}, l2['id']: {l1['id']:[]}}
#         for c in conflicts:
#             errors[l1['id']][l2['id']].append({'barcode1'})

"""
libraries: [{'id':'id1', 'barcodes': {'P5':[...]}}, ...] 
returns: {'id1': {'id3': [{'barcode':'...','distance':2},...]}, 'id3': {'id1': [{'barcode':'...','distance':2},...]}
"""
def get_all_conflicts(libraries, min_distance=2, keys=['i5', 'i7']):
    conflicts = {}
    # raise Exception(libraries)
    for i, l1 in enumerate(libraries):
        for l2 in libraries[i+1:]:
            print(l1['barcodes'], l2['barcodes'])
            for k in keys:
                distance = hamming_distance(l1['barcodes'][k], l2['barcodes'][k])
                if distance < min_distance:
                    if not l1['id'] in conflicts:
                        conflicts[l1['id']] = {}
                    if not l2['id'] in conflicts:
                        conflicts[l2['id']] = {}
                    if k not in conflicts[l1['id']]:
                        conflicts[l1['id']][k] = []
                    if k not in conflicts[l2['id']]:
                        conflicts[l2['id']][k] = []
                    conflicts[l1['id']][k].append(l2['id'])
                    conflicts[l2['id']][k].append(l1['id'])
    return conflicts

def test_all_library_conflicts(min_distance=1):
    from sims.models import Library
    from sims.api.serializers import LibrarySerializer
#     for l in Library
    return get_all_conflicts(LibrarySerializer(list(Library.objects.all()),many=True).data,min_distance=min_distance)
# def is_compatible(s1, s2, h):

def test_adapter_conflicts(min_distance=1, adapter_db=None):
    from sims.models import AdapterDB
    db_conflicts = {}
    if adapter_db:
        dbs = AdapterDB.objects.filter(id=adapter_db)
    else:
        dbs = AdapterDB.objects.all()
    for db in dbs:
        print(db.id)
        libraries = [{'id': a.name, 'barcodes': a.barcodes} for a in db.adapters.all()]
        db_conflicts[db.id] = get_all_conflicts(libraries,min_distance=min_distance)
    return db_conflicts