##Scripts to query Gitlab using python-gitlab

- You need to create a private token in your Gitlab in order to use this script. There are other methods of authentication
described in [https://python-gitlab.readthedocs.io/en/stable/]
- Execute ```pip install -r requirements.txt```
- Configure ```~\.python-gitlab.cfg```
  - Add the following entries
```  
[global]
default = gitlab.cu
ssl_verify = false
timeout = 5

[gitlab.cu]
url = https://gitlab.cu.aleph.engineering
private_token = <your private token>
api_version = 4
```
- Right now, just change in the code the url of Gitlab, username, label of tasks, and dates.
- The script will return: 
  - Total tasks
  - Time spent
 
##TODO
- Pass arguments as paremeters in script call
