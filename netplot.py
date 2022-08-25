import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
fig, _ = plt.subplots()
title=["Ping","Download","Upload"]
color=['r','g','c']
plot=[[],[],[]]
i = 0
with open('/var/log/speed') as spe:
	for line in spe:
		speed = float(line.split()[1])
		if(i==0 and speed > 100):
			speed=-5
		plot[i].append(speed)
		i += 1
		i = i % 3
plt.figure(1)
for b in range(len(plot)):
	plt.subplot(b+311).set_ylabel(title[b],color=color[b])
	plt.plot([*range(len(plot[b]))],plot[b],c=color[b])
	plt.tick_params(axis='y', labelcolor=color[b])
fig.tight_layout()
plt.show()
