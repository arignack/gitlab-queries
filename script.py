import gitlab
import datetime
import requests

session = requests.Session()
# session.proxies = {
#     'https': 'http://localhost:8123',
#     'http': 'http://localhost:8123',
# }

url = 'http://localhost:381'
# private_token = 'H74t_h4NczxRbxaQsauH' # gitlab.com
private_token = 'wz1uCSEVzb6vfyVxRqxm'  # gitlab.docker
assignee = 'root'
label = 'To Do'
date_start = datetime.datetime(2018, 10, 1)
date_end = datetime.datetime(2018, 12, 1)

gl = gitlab.Gitlab(url, private_token, api_version=4, session=session)
issues = gl.issues.list()

issues_filter = filter(lambda x: x.assignee['username'] == assignee and
                                 x.labels.__contains__(label) and
                                 date_start < datetime.datetime.strptime(x.updated_at,
                                                                         "%Y-%m-%dT%H:%M:%S.%fZ") < date_end,
                       issues)
tasks = list(issues_filter)

sum_estimated = 0
for issue in tasks:
    sum_estimated += issue.time_stats['total_time_spent']

print('User: ' + assignee)
print('Total tasks:' + str(len(tasks)))
print('Time spent: ' + str(datetime.timedelta(seconds=sum_estimated)))
