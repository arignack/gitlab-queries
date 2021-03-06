import gitlab
import datetime
import dateutil.parser
import requests
import os
import itertools

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

def sort_issues(i):
    return i.project_id


issues_sorted = \
    sorted(
        list(
            filter(lambda x: x.assignee is not None and
                                        x.updated_at is not None and
                                        x.labels is not None and
                                        x.assignee['username'] == assignee and
                                        x.labels.__contains__(label) and
                            start_date< datetime.datetime.strptime(x.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ") < end_date,
                       issues)), key=sort_issues)

groups_by_project = itertools.groupby(issues_sorted, sort_issues)

for id, issuesGroup in groups_by_project:
    project_issues = list(issuesGroup)
    time_spent = sum(issue.time_stats['total_time_spent'] for issue in project_issues)
    time_estimate = sum(issue.time_stats['time_estimate'] for issue in project_issues)

    # TODO: Format as table
    print('================================')
    print('Project: {}'.format(gl.projects.list(id=id)[0].name))
    print('User: ' + assignee)
    print('Period: From {} to {}'.format(start_date, end_date))
    print('Total issues:' + str(len(project_issues)))
    print('Time spent in hours: ' + str(datetime.timedelta(seconds=time_spent)))
    print('Time estimated in hours: ' + str(datetime.timedelta(seconds=time_estimate)))
