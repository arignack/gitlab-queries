import gitlab
import datetime
import dateutil.parser
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
start_date = dateutil.parser.parse(os.getenv('GQ_START_DATE'))
end_date = dateutil.parser.parse(os.getenv('GQ_END_DATE'))

gl = gitlab.Gitlab(url, private_token, api_version=4, session=session)
issues = gl.issues.list()

issues_filtered = list(filter(lambda x: x.assignee is not None and
                                        x.updated_at is not None and
                                        x.labels is not None and
                                        x.assignee['username'] == assignee and
                                        x.labels.__contains__(label) and
                            start_date< datetime.datetime.strptime(x.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ") < end_date,
                       issues))

time_spent = sum(issue.time_stats['total_time_spent'] for issue in issues_filtered)
time_estimate = sum(issue.time_stats['time_estimate'] for issue in issues_filtered)

print('User: ' + assignee)
print('Period: From {} to {}'.format(start_date, end_date))
print('Total issues:' + str(len(issues_filtered)))
print('Time spent in hours: ' + str(datetime.timedelta(seconds=time_spent)))
print('Time estimated in hours: ' + str(datetime.timedelta(seconds=time_estimate)))
