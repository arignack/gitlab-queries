###Scripts to query Gitlab using python-gitlab

- Execute ```pip install -r requirements.txt```
- Configure the following environment variables:
```
GQ_PRIVATE_TOKEN='your_private_token'
GQ_URL='gitlab_url'
GQ_ASSIGNEE='your_username'
GQ_LABEL='one_single_label_now'
```
- Specify start_date and end_date inside the script
- The script will return:
  - User
  - Period 
  - Total tasks
  - Time spent in hours
 
##TODO
- Pass arguments as paremeters in script call
