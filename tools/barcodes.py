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
def get_all_conflicts(libraries, min_distance=2):
    conflicts = {}
    for i, l1 in enumerate(libraries):
        for l2 in libraries[i+1:]:
            c = get_conflicts(l1, l2, min_distance)
            if len(c) > 0:
                if not l1['id'] in conflicts:
                    conflicts[l1['id']] = {}
                if not l2['id'] in conflicts:
                    conflicts[l2['id']] = {}
                conflicts[l1['id']][l2['id']] = c
                conflicts[l2['id']][l1['id']] = c
    return conflicts

def test_conflicts(min_distance=1):
    from sims.models import Library
    from sims.api.serializers import LibrarySerializer
#     for l in Library
    return get_all_conflicts(LibrarySerializer(list(Library.objects.all()),many=True).data,min_distance=min_distance)
# def is_compatible(s1, s2, h):