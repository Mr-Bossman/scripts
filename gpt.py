import requests
import json

# Replace with your GitHub username
username = 'Mr-Bossman'

# Make a GET request to retrieve the user's repositories
response = requests.get(f'https://api.github.com/users/{username}/repos')

# Filter out forked repositories
repositories = [repo for repo in response.json() if not repo['fork']]

# Create an empty list to store the files
files = []

# For each repository, retrieve all the files and add them to the list
for repo in repositories:
    repo_name = repo['name']
    response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/contents')
    files.extend(response.json())

# Write the files to a JSON file
with open(f'{username}_files.json', 'w') as f:
    json.dump(files, f)
