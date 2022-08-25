import json
import re
import numpy as np

with open("files.json", "r") as jsonfile:
	raw_stats = json.load(jsonfile)

epsilon = 1
endings = []
def liststats(liststat):
	tupple_stats = np.unique(liststat, return_counts=True)
	stats = dict(zip(tupple_stats[0],tupple_stats[1]))
	stats = dict(sorted(stats.items(), key=lambda x: x[1],reverse=True))
	filtered_stats={}
	for key in stats:
		if((100*stats[key])/len(liststat) > epsilon):
			filtered_stats[key] = stats[key]
	for key in filtered_stats:
		filtered_stats[key] = (100*filtered_stats[key])/sum(filtered_stats.values())
	return filtered_stats

for repo in raw_stats:
	if "wallet" in repo:
		continue
	#print(repo)
	repoend = [re.split("\.|\/|-|_",fname)[-1] for fname in raw_stats[repo]]
	endings += repoend
	#stats = liststats(repoend)
	#for key in stats:
	#	if stats[key] > epsilon:
	#		print(key, ':', stats[key])
print("\n\n\n\nTotal:")
stats = liststats(endings)
for key in stats:
	if stats[key] > epsilon:
		print(key, ':', stats[key])