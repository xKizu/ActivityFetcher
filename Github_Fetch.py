import requests
import sys
from datetime import datetime, timedelta

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            raise Exception(f"User '{username}' not found.") from http_err
        else:
            raise Exception(f"HTTP error occurred: {http_err}") from http_err
    except requests.exceptions.RequestException as err:
        raise Exception(f"\nError fetching data from GitHub: {err}") from err

    try:
        events = response.json()
    except ValueError as json_err:
        raise Exception(f"Error parsing JSON response: {json_err}") from json_err

    return events
    

def display_activity(events):
    Found1 = Found2 = Found3 = False
    for event in events:
        if event["type"] == "PushEvent":
            repo_name = event["repo"]["name"]
            commit_count = event["payload"]["size"]
            time = event["created_at"]
            if datetime.now() - datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") <= timedelta(days=1):
                print(f"{datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')} Pushed {commit_count} commits to {repo_name}")
                Found1 = True
        elif event["type"] == "IssueCommentEvent":
            repo_name = event["repo"]["name"]
            action = event["payload"]["action"]
            time = event["created_at"]
            if datetime.now() - datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") <= timedelta(days=1):
                print(f"{datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')} {action.capitalize()} a new issue in {repo_name}")
                Found2 = True
        elif event["type"] == "WatchEvent":
            repo_name = event["repo"]["name"]
            time = event["created_at"]
            if datetime.now() - datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") <= timedelta(days=1):
                print(f"{datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')} Starred {repo_name}")
                Found3 = True
    if not (Found1 or Found2 or Found3):
        print("No recent activity found")


def main():
    if len(sys.argv) < 2:
        print("Usage: python Github_Fetch.py <username>")
        sys.exit(1)

    username = sys.argv[1]

    try:
        events = fetch_github_activity(username)
        if not events:
            print("No recent activity found")
        else:
            display_activity(events)

    except Exception as e:
        print(f"Error fetching recent activity: {e}")
        sys.exit(1)
    
     

if __name__ == "__main__":
    main()