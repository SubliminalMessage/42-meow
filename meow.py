import requests, json, keyboard, os
from datetime import datetime, timedelta
from dotenv import load_dotenv


def fetch(url, data={}, headers={}, post=False):
    if (post):
        result = requests.post(url, data=data)
    else:
        result = request.get(url, headers=headers)
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
students = file.read().split('\n')
#print(students)

# Get API Bearer Token
load_dotenv()
uid = os.getenv("API_UID")
secret = os.getenv("API_SECRET")
(bearer_token, next_refresh) = refresh_token()

# Display a menu to select the exam / project wanted
def get_user_info(user):
    global bearer_token, next_refresh
    time_now = datetime.now()
    # Check if token has expired
        # Refresh if so
    
    # Fetch info from user
    # Filter that info
    # Wait for, at least, 0.5s. If the request delays less than 0.5s, just wait the difference
    # Display info with cool colors (out of the function, for it to be a dependence)