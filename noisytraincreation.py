#To create a noisy dataset
#find the average over4-5 values to find the actual correct prediction of 20% noise and so on
#on noise of 20%, the percent correct prediction is 65%, on 15% it was 68%, on 5% false accuracy is 67.4%
#on 1% noise, 67.6%accuracy

import random
noise = 100	#noisy elements
lines = [line.rstrip('\n') for line in open('train.txt')]
d = {}
i = 1
for line in lines:
	d[i] = line
	i = i + 1
for i in range(0,noise):
	a = random.randint(1,1000)
	if d[a][0]=='1' and d[a][1]=='0':
		string = "1"
		string = string + d[a][2:]
		d[a] = string
	elif int(d[a][0])>=7:
		string = "1"
		string = string + d[a][1:]
		d[a] = string
	elif int(d[a][0])<=4:
		string = "9"
		string = string + d[a][1:]
		d[a] = string

posfile = open("noisytrain.txt","w")
for key in d:
	posfile.write(d[key])
	posfile.write("\n")