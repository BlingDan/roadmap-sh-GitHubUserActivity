import urllib.request
import json
import sys

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching activity: {e}")
        return []

def display_github_activity(activity_list):
    """Display the activity list in a readable format"""

    print("Output:")
    
    for event in activity_list:
        type = event['type']
        repo_name = event['repo']['name']

        if type == 'PushEvent':
            commits = event['payload']['commits']
            print(f'- Pushed {len(commits)} commits to {repo_name}')
        elif type == 'IssuesEvent':
            action = event['payload']['action']
            if action == 'opened':
                print(f'- Opened a new issue in {repo_name}')
            elif action == 'closed':
                print(f'- Closed an issue in {repo_name}')
        elif type == 'WatchEvent':
            print(f'- Starred {repo_name}')
        else:
            print(f'- {type} in {repo_name}')
            
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        github_username = sys.argv[1]
        activity = fetch_github_activity(github_username)
        
        with open('github_activity.json', 'w') as f:
            json.dump(activity, f)
        
        display_github_activity(activity)

    else:
        print("Please provide a GitHub username as an argument.")
