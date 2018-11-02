#I find the 2500 most frequently occuring words with emotion>1 and 2500 with emotion<-0.5

lines = [line.rstrip('\n') for line in open('TRAINlabeledBow.feat')]
d = {}	#stores the num of times a word has occured for the entire TRAINlabeledBow.feat
for line in lines:
	tokens = line.split(" ")
	i = 0
	for token in tokens:
		if(i==0):
			i = i+1
		else:
			info = token.split(":")
			if int(info[0]) in d:
				d[int(info[0])] = d[int(info[0])] + int(info[1])
			else:
				d[int(info[0])] = int(info[1])

dictEmotionOfaword = {}
lines = [line.rstrip('\n') for line in open('imdbEr.txt')]
i = 0
for line in lines:
	dictEmotionOfaword[i] = float(line)
	i = i + 1

attributeFile = open("selected-features-indices.txt","w")

poswords = 0
negwords = 0
for key in sorted(d.items(), key=lambda x: x[1], reverse=True):
	if dictEmotionOfaword[key[0]]>1 and poswords<2500:
		attributeFile.write(str(key[0]))
		attributeFile.write("\n")
		poswords = poswords + 1

	elif dictEmotionOfaword[key[0]]<-0.5 and negwords<2500:
		attributeFile.write(str(key[0]))
		attributeFile.write("\n")
		negwords = negwords + 1









