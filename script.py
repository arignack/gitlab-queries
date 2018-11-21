import gitlab
import datetime

gl = gitlab.Gitlab('http://gitlab.cu.aleph.engineering', private_token='3WoyUjDo_HiSzrx4EX8n')

assignee = 'alian'
labels = ['Done']
date_start = datetime.datetime(2018, 11, 1)
date_end = datetime.datetime(2018, 12, 1)

issues = gl.issues.list(labels=labels)

list_filter = filter(lambda x: x.assignee['username'] == assignee and
                               x.labels == labels and
                               date_start < datetime.datetime.strptime(x.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ") < date_end,
                     issues)
tasks = list(list_filter)

sum_estimated = 0
for issue in tasks:
    sum_estimated += issue.time_stats['total_time_spent']

print('User: ' + assignee)
print('Total tasks:' + str(len(tasks)))
print('Time spent: ' + str(datetime.timedelta(seconds=sum_estimated)))
