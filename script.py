import gitlab
import datetime
import requests
import os

session = requests.Session()
if os.getenv('GQ_PROXY_HTTP'):
    session.proxies = {
        'https': os.getenv('GQ_PROXY_HTTPS'),
        'http': os.getenv('GQ_PROXY_HTTP'),
    }

private_token = os.getenv('GQ_PRIVATE_TOKEN')
url = os.getenv('GQ_URL')
assignee = os.getenv('GQ_ASSIGNEE')
label = os.getenv('GQ_LABEL')

date_start = datetime.datetime(2018, 10, 1)
date_end = datetime.datetime(2018, 12, 1)

gl = gitlab.Gitlab(url, private_token, api_version=4, session=session)
issues = gl.issues.list()

issues_filtered = list(filter(lambda x: x.assignee is not None and
                                        x.updated_at is not None and
                                        x.assignee['username'] == assignee and
                                        x.labels.__contains__(label) and
                            date_start < datetime.datetime.strptime(x.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ") < date_end,
                       issues))

time_spent = sum(issue.time_stats['total_time_spent'] for issue in issues_filtered)

print('User: ' + assignee)
print('Period: From {} to {}'.format(date_start, date_end))
print('Tasks completed:' + str(len(issues_filtered)))
print('Time spent in hours: ' + str(datetime.timedelta(seconds=time_spent)))
