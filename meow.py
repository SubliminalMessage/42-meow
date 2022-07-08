import requests, json, keyboard, os, time
from datetime import datetime, timedelta
from dotenv import load_dotenv

total_calls = 0
def fetch(url, data={}, headers={}, post=False):
    global total_calls
    if (post):
        result = requests.post(url, data=data)
    else:
        result = requests.get(url, headers=headers)
    total_calls += 1
    return result.json()

def refresh_token():
    response = fetch('https://api.intra.42.fr/oauth/token', post=True, data={
        "grant_type": "client_credentials",
        "client_id": uid,
        "client_secret": secret
    })


    bearer_token = response['access_token']
    next_token_update = datetime.now() + timedelta(int(response['expires_in']))
    return (bearer_token, next_token_update)


# Get Student's Logins from 'students.config.txt' file
file = open('./students.config.txt', 'r')
usernames = file.read().split('\n')
#print(students)

# Get API Bearer Token
load_dotenv()
uid = os.getenv("API_UID")
secret = os.getenv("API_SECRET")
(bearer_token, next_refresh) = refresh_token()

# Display a menu to select the exam / project wanted
def get_user_info(user):
    global bearer_token, next_refresh
    time_before_request = datetime.now()
    # Check if token has expired
    if (time_before_request >= next_refresh):
        # Refresh if so
        (bearer_token, next_refresh) = refresh_token()

    #  curl -g  -H "Authorization: Bearer BEARER_TOKEN" "https://api.intra.42.fr/v2/users/:user_id/projects_users"
    # Fetch info from user
    headers = {"Authorization": f"Bearer {bearer_token}"}
    user_info = fetch(f"https://api.intra.42.fr/v2/users/{user}/projects_users", headers=headers)

    # Wait for, at least, 0.5s. If the request delays less than 0.5s, just wait the difference
    time_after_request = datetime.now()
    time_diff = timestamp(time_after_request) - timestamp(time_before_request)
    time_to_wait = 0.5 - time_diff
    time.sleep( (0, time_to_wait)[time_to_wait > 0])
    return user_info

def timestamp(datetime):
    return time.mktime(datetime.timetuple()) + datetime.microsecond/1e6

# Filter that user info
def get_user_projects(info, projects = []):
    for project in info:
        final_mark = project['final_mark']
        status = project['status']
        name = project['project']['name']
        if name in projects:
            # ToDo: handle multiple projects at once
            print(project)
            return str(final_mark)
    return "KO"

# Parse usernames into an object
everyone = {}
for login in usernames:
    everyone[login] = True # Is this user still on the Exam?


#print(everyone)
# Display info with cool colors (out of the function, for it to be a dependence)

info2 = get_user_info("username")
print(get_user_projects(info2, ["C Piscine Exam 00"]))


# KO -> Not registered
# None -> Not in, but registered
# 0-100 -> Final Mark
    #