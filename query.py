import json
import requests
import time

repos_URL = "https://api.github.com/users/mr-bossman/repos?per_page=1000"
repos = requests.get(repos_URL).json()
repo_names = [dic["full_name"] for dic in repos if not dic["fork"]]
files = {}
for name in repo_names:
	for branch in requests.get("https://api.github.com/repos/" + name + "/branches").json():
		tree_url = "https://github.com/" + name + "/tree-list/" + branch["commit"]["sha"]
		full_name = name + ":" + branch["name"]
		print(full_name)
		files[full_name] = requests.get(tree_url, headers={"accept":"application/json"}).json()["paths"]
		time.sleep(1)

with open("files.json", "w") as jsonfile:
	json.dump(files, jsonfile)