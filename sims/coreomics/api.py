from django.conf import settings
import urllib.request, json

def get_submission_types(base_url=settings.SUBMISSION_SYSTEM_URL, lab=settings.SUBMISSION_SYSTEM_LAB):
    url = '{base_url}/server/api/submission_types/?lab={lab}&page=1&page_size=100'.format(base_url=base_url, lab=lab)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return data['results']
