from django.conf import settings
import urllib.request, json

from sims.models import SubmissionType

def get_submission_types(base_url=settings.SUBMISSION_SYSTEM_URL, lab=settings.SUBMISSION_SYSTEM_LAB):
    url = '{base_url}/server/api/submission_types/?lab={lab}&page=1&page_size=100'.format(base_url=base_url, lab=lab)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return data['results']

def sync_submission_types(base_url=settings.SUBMISSION_SYSTEM_URL, lab=settings.SUBMISSION_SYSTEM_LAB):
    for t in get_submission_types(base_url=base_url, lab=lab):
        st = SubmissionType(id=t['id'], prefix=t['prefix'], name=t['name'], description=t['description'], statuses=t['statuses'], sort_order=t['sort_order'], submission_schema=t['submission_schema'], updated=t['updated'], lab_id=lab, active=t['active'])
        print('saving', st.id, st.save())
        