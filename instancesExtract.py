lines = [line.rstrip('\n') for line in open('TRAINlabeledBow.feat')]	#read the file line by line and store in a list
import random
positive = 0;		#keep count of positive training instances stored
negative = 0;		#keep count of negative training instances stored
indicesDict = {}	#keep the indices of the list 'lines' that are to be used as training set
while True:
	if positive>=500 and negative>=500:			#check if 500 of both examples stored 
		break
	key = random.randint(0,25000)
	if key not in indicesDict:					#so that no review is repeated 
		splitted = lines[key].split(" ")
		rating = int(splitted[0])
		if rating>= 7 and positive<500:			#store 1 as value in dict for positive review
			indicesDict[key] = 1
			positive = positive + 1
		if rating<=4 and negative<500:			#store -1 as value in dict for positive review
			indicesDict[key] = -1
			negative = negative + 1
posfile = open("train.txt","w")				#write the 1000 positive and negative reviewed training instances in file named train.txt
for key in indicesDict:
	if indicesDict[key]==1:						#indicesDict[key] == 1 means its positive review else -1 means negative review
		posfile.write(lines[key])
		posfile.write("\n")
	elif indicesDict[key]==-1:
		posfile.write(lines[key])
		posfile.write("\n")

#similar steps are taken to make positive and negative test data set

lines = [line.rstrip('\n') for line in open('TESTlabeledBow.feat')]	#read the file line by line and store in a list
positive = 0;
negative = 0;
indicesDict = {}
while True:
	if positive>=500 and negative>=500:
		break
	key = random.randint(0,25000)
	if key not in indicesDict:
		splitted = lines[key].split(" ")
		rating = int(splitted[0])
		if rating>= 7 and positive<500:
			indicesDict[key] = 1
			positive = positive + 1
		if rating<=4 and negative<500:
			indicesDict[key] = -1
			negative = negative + 1
posfile = open("test.txt","w")
for key in indicesDict:
	if indicesDict[key]==1:
		posfile.write(lines[key])
		posfile.write("\n")
	elif indicesDict[key]==-1:
		posfile.write(lines[key])
		posfile.write("\n")