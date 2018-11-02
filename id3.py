import sys
sys.setrecursionlimit(10**6)
testfile = sys.argv[1]
exptno = sys.argv[2]
if exptno == '2':

	sah = 0
	if sah==0:
		class node:
		    def __init__(self, attrib, posinst, neginst, label):	
		        self.left = None 				#left child in the tree
		        self.right = None
		        self.attrib = attrib 			#attrib is the index of the word used as attribute in this node
		        self.posinst = posinst 			#posinst is the number of positive examples at this node
		        self.neginst = neginst
		        self.label = label				#label = "notleaf" OR "yes" if the prediction is positive(i.e. the movie review is positive) OR "no"-if the prediction is negative

		    def insert(self, attrib, posinst, neginst, lorR, label):
		    	if lorR == 'left':				#insert at the left child of the node
		    		self.left = node(attrib, posinst, neginst, label)
		    		return self.left
		    	elif lorR == 'right':
		    		self.right = node(attrib, posinst, neginst, label)
		    		return self.right

		    def count_attr_freq(self):
		    	attr_freq = {}
		    	self.count_attr_freq_helper(attr_freq)
		    	return attr_freq

		    def count_attr_freq_helper(self, attr_freq):
		    	if self.label != "notleaf":
		    		return
		    	else:
		    		if self.attrib in attr_freq:
		    			attr_freq[self.attrib] = attr_freq[self.attrib] + 1
		    		else:
		    			attr_freq[self.attrib] = 1
		    		if self.left:
		    			self.left.count_attr_freq_helper(attr_freq)
		    		if self.right:
		    			self.right.count_attr_freq_helper(attr_freq)

		    def count_leaf_nodes(self):
		    	leaf_nodes = []
		    	self.count_leaf_nodes_helper(leaf_nodes)
		    	return len(leaf_nodes)

		    def count_leaf_nodes_helper(self, leaf_nodes):
		    	if self.label != "notleaf":
		    		leaf_nodes.append(self)
		    	else:
		    		if self.left:
		    			self.left.count_leaf_nodes_helper(leaf_nodes)
		    		if self.right:
		    			self.right.count_leaf_nodes_helper(leaf_nodes)


		import math
		def entropy(numpos,numneg):		#caclulate the entropy where numpos is the number of positive examples
			total = numpos + numneg
			if total==0:
				return 0
			ppos = numpos/total
			pneg = numneg/total
			if(ppos==0 or pneg==0):
				return 0
			return (-ppos)*math.log2(ppos)-pneg*math.log2(pneg)

		def splitting(node1,posI,negI,attr,parent):			#to create the children of node1 and then this is recursively called
			#print(len(posI),len(negI))
			
				ig = {}						#ig keeps the info gain for each of the attributes
				for index in attr:			#one by one see all attributes to check which has the max info gain
					yespos = 0				#num of positive examples(review pos) who has this "index" attribute
					nopos = 0				#num of positive examples who does not have this attribute
					yesneg = 0
					noneg = 0
					for itemDict in posI:		#posI is a list of dictionaries with each dictionary containing one positive review from the training set
						if int(index) in itemDict:
							yespos = yespos + 1
						else:
							nopos = nopos + 1
					for itemDict in negI:
						if int(index) in itemDict:
							yesneg = yesneg + 1
						else:
							noneg = noneg + 1
					totalI = len(posI) + len(negI)
					ig[index] = entropy(len(posI),len(negI)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
					#print(nopos, noneg, entropy(nopos,noneg))
				maxig = ig[list(ig.keys())[0]]			#find the max info gain of all the ig
				indexOfmaxig = list(ig.keys())[0]		#stores the index of max info gain
				for key in ig:
					if(ig[key]>maxig):
						maxig = ig[key]
						indexOfmaxig = key
				if maxig==0:
					if len(posI)<len(negI):
						node1.label = "no"
					else:
						node1.label = "yes"
				else:
					node1.attrib = indexOfmaxig			#made the attribute of this node as the one with max ig
					yesposI = []		#list of all instances which are positive reviewed and contains the attribute "indexofmaxig"
					yesnegI = []
					noposI = []
					nonegI = []
					for dictionary in posI:
						if int(indexOfmaxig) in dictionary:
							yesposI.append(dictionary)
						else:
							noposI.append(dictionary)
					for dictionary in  negI:
						if int(indexOfmaxig) in dictionary:
							yesnegI.append(dictionary)
						else:
							nonegI.append(dictionary)
					if len(yesposI)+len(yesnegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					elif len(noposI)+len(nonegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					else:
						node2 = node1.insert("attr",yesposI,yesnegI,"left","notleaf")	#create the two children of node1
						node3 = node1.insert("attr",noposI,nonegI,"right","notleaf")
						attrr = []
						attrri = []
						for item in attr:
							attrr.append(item)
							attrri.append(item)
						attrr.remove(indexOfmaxig)		#remove the attribute and then use the new attribute list
						attrri.remove(indexOfmaxig)
						splitting(node2,yesposI,yesnegI,attrr,node1)
						splitting(node3,noposI,nonegI,attrr,node1)


		attributes = [line.rstrip('\n') for line in open('selected-features-indices.txt')]	#extract the indices of words to be used as attribute
		posInstances = []
		negInstances = []
		lines = [line.rstrip('\n') for line in open('train.txt')]
		for line in lines:
			l = line.split(" ")
			if int(l[0])<=4:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				negInstances.append(d)
			elif int(l[0])>=7:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				posInstances.append(d)


		ig = {}
		for index in attributes:
			yespos = 0
			nopos = 0
			yesneg = 0
			noneg = 0
			for itemDict in posInstances:
				if int(index) in itemDict:
					yespos = yespos + 1
				else:
					nopos = nopos + 1
			for itemDict in negInstances:
				if int(index) in itemDict:
					yesneg = yesneg + 1
				else:
					noneg = noneg + 1
			totalI = len(posInstances) + len(negInstances)
			ig[index] = entropy(len(posInstances),len(negInstances)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
			#print(nopos, noneg, entropy(nopos,noneg))
		maxig = ig[list(ig.keys())[0]]
		indexOfmaxig = list(ig.keys())[0]
		for key in ig:
			if(ig[key]>maxig):
				maxig = ig[key]
				indexOfmaxig = key
		#print(maxig)
		root = node(indexOfmaxig,posInstances,negInstances,"notleaf")
		temp = root
		if(len(posInstances)==0):
			root.label = "no"
		elif len(negInstances)==0:
			root.label = "yes"
		else:
			yesposI = []
			yesnegI = []
			noposI = []
			nonegI = []
			for dictionary in posInstances:
				if int(indexOfmaxig) in dictionary:
					yesposI.append(dictionary)
				else:
					noposI.append(dictionary)
			for dictionary in  negInstances:
				if int(indexOfmaxig) in dictionary:
					yesnegI.append(dictionary)
				else:
					nonegI.append(dictionary)
			node1 = root.insert("attr",yesposI,yesnegI,"left","notleaf")
			node2 = root.insert("attr",noposI,nonegI,"right","notleaf")
			attributes.remove(indexOfmaxig)
			splitting(node1,yesposI,yesnegI,attributes,root)
			splitting(node2,noposI,nonegI,attributes,root)
		#checking the test examples to find the percentage of correct predictions
		totalcorrect = 0
		lines = [line.rstrip('\n') for line in open(sys.argv[1])]
		total = len(lines)
		for line in lines:
			l = line.split(" ")
			rating = int(l[0])
			ans = ""
			if(rating>=7):
				ans = "yes"
			if(rating<=4):
				ans = "no"
			myans = ""
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i + 1
				else:
					info = item.split(":")
					d[int(info[0])] = int(info[1])
			temp = root
			while True:
				if temp.label=="notleaf":
					if int(temp.attrib) in d:
						temp = temp.left
					else:
						temp = temp.right
				else:
					if temp.label=="yes":
						myans = "yes"
					elif temp.label=="no":
						myans = "no"
					if myans==ans:
						totalcorrect = totalcorrect + 1
					break

		correctPercent = totalcorrect/total
		correctPercent = correctPercent*100
		print("id3 without early stopping: \n\nAccuracy: ",correctPercent)
		print("\nnum of leaves: ",root.count_leaf_nodes())
		dict_attr_freq = root.count_attr_freq()
		i = 0
		print("\n5 most used attributes to split are(attributeIndex numOfTimesUsed): ")
		for key in sorted(dict_attr_freq.items(), key=lambda x: x[1], reverse=True):
			i = i+1
			print(key[0], "\t", key[1])
			if i>4:
				break
		sah = 1

	if sah==1:
		class node:
		    def __init__(self, attrib, posinst, neginst, label):	
		        self.left = None 				#left child in the tree
		        self.right = None
		        self.attrib = attrib 			#attrib is the index of the word used as attribute in this node
		        self.posinst = posinst 			#posinst is the number of positive examples at this node
		        self.neginst = neginst
		        self.label = label				#label = "notleaf" OR "yes" if the prediction is positive(i.e. the movie review is positive) OR "no"-if the prediction is negative

		    def insert(self, attrib, posinst, neginst, lorR, label):
		    	if lorR == 'left':				#insert at the left child of the node
		    		self.left = node(attrib, posinst, neginst, label)
		    		return self.left
		    	elif lorR == 'right':
		    		self.right = node(attrib, posinst, neginst, label)
		    		return self.right

		    def count_attr_freq(self):
		    	attr_freq = {}
		    	self.count_attr_freq_helper(attr_freq)
		    	return attr_freq

		    def count_attr_freq_helper(self, attr_freq):
		    	if self.label != "notleaf":
		    		return
		    	else:
		    		if self.attrib in attr_freq:
		    			attr_freq[self.attrib] = attr_freq[self.attrib] + 1
		    		else:
		    			attr_freq[self.attrib] = 1
		    		if self.left:
		    			self.left.count_attr_freq_helper(attr_freq)
		    		if self.right:
		    			self.right.count_attr_freq_helper(attr_freq)

		    def count_leaf_nodes(self):
		    	leaf_nodes = []
		    	self.count_leaf_nodes_helper(leaf_nodes)
		    	return len(leaf_nodes)

		    def count_leaf_nodes_helper(self, leaf_nodes):
		    	if self.label != "notleaf":
		    		leaf_nodes.append(self)
		    	else:
		    		if self.left:
		    			self.left.count_leaf_nodes_helper(leaf_nodes)
		    		if self.right:
		    			self.right.count_leaf_nodes_helper(leaf_nodes)


		import math
		def entropy(numpos,numneg):		#caclulate the entropy where numpos is the number of positive examples
			total = numpos + numneg
			if total==0:
				return 0
			ppos = numpos/total
			pneg = numneg/total
			if(ppos==0 or pneg==0):
				return 0
			return (-ppos)*math.log2(ppos)-pneg*math.log2(pneg)

		def splitting(node1,posI,negI,attr,parent):			#to create the children of node1 and then this is recursively called
			#print(len(posI),len(negI))
			if len(posI)+len(negI)<30:
				if len(posI)<len(negI):
					node1.label = "no"
				else:
					node1.label = "yes"
			else:
				ig = {}						#ig keeps the info gain for each of the attributes
				for index in attr:			#one by one see all attributes to check which has the max info gain
					yespos = 0				#num of positive examples(review pos) who has this "index" attribute
					nopos = 0				#num of positive examples who does not have this attribute
					yesneg = 0
					noneg = 0
					for itemDict in posI:		#posI is a list of dictionaries with each dictionary containing one positive review from the training set
						if int(index) in itemDict:
							yespos = yespos + 1
						else:
							nopos = nopos + 1
					for itemDict in negI:
						if int(index) in itemDict:
							yesneg = yesneg + 1
						else:
							noneg = noneg + 1
					totalI = len(posI) + len(negI)
					ig[index] = entropy(len(posI),len(negI)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
					#print(nopos, noneg, entropy(nopos,noneg))
				maxig = ig[list(ig.keys())[0]]			#find the max info gain of all the ig
				indexOfmaxig = list(ig.keys())[0]		#stores the index of max info gain
				for key in ig:
					if(ig[key]>maxig):
						maxig = ig[key]
						indexOfmaxig = key
				#print("maxig:", maxig)
				if maxig<=0:
					if len(posI)<len(negI):
						node1.label = "no"
					else:
						node1.label = "yes"
				else:
					node1.attrib = indexOfmaxig			#made the attribute of this node as the one with max ig
					yesposI = []		#list of all instances which are positive reviewed and contains the attribute "indexofmaxig"
					yesnegI = []
					noposI = []
					nonegI = []
					for dictionary in posI:
						if int(indexOfmaxig) in dictionary:
							yesposI.append(dictionary)
						else:
							noposI.append(dictionary)
					for dictionary in  negI:
						if int(indexOfmaxig) in dictionary:
							yesnegI.append(dictionary)
						else:
							nonegI.append(dictionary)
					if len(yesposI)+len(yesnegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					elif len(noposI)+len(nonegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					else:
						node2 = node1.insert("attr",yesposI,yesnegI,"left","notleaf")	#create the two children of node1
						node3 = node1.insert("attr",noposI,nonegI,"right","notleaf")
						attrr = []
						attrri = []
						for item in attr:
							attrr.append(item)
							attrri.append(item)
						attrr.remove(indexOfmaxig)		#remove the attribute and then use the new attribute list
						attrri.remove(indexOfmaxig)
						splitting(node2,yesposI,yesnegI,attrr,node1)
						splitting(node3,noposI,nonegI,attrr,node1)


		attributes = [line.rstrip('\n') for line in open('selected-features-indices.txt')]	#extract the indices of words to be used as attribute
		posInstances = []
		negInstances = []
		lines = [line.rstrip('\n') for line in open('train.txt')]
		for line in lines:
			l = line.split(" ")
			if int(l[0])<=4:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				negInstances.append(d)
			elif int(l[0])>=7:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				posInstances.append(d)


		ig = {}
		for index in attributes:
			yespos = 0
			nopos = 0
			yesneg = 0
			noneg = 0
			for itemDict in posInstances:
				if int(index) in itemDict:
					yespos = yespos + 1
				else:
					nopos = nopos + 1
			for itemDict in negInstances:
				if int(index) in itemDict:
					yesneg = yesneg + 1
				else:
					noneg = noneg + 1
			totalI = len(posInstances) + len(negInstances)
			ig[index] = entropy(len(posInstances),len(negInstances)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
			#print(nopos, noneg, entropy(nopos,noneg))
		maxig = ig[list(ig.keys())[0]]
		indexOfmaxig = list(ig.keys())[0]
		for key in ig:
			if(ig[key]>maxig):
				maxig = ig[key]
				indexOfmaxig = key
		#print(maxig)
		root = node(indexOfmaxig,posInstances,negInstances,"notleaf")
		temp = root
		if(len(posInstances)==0):
			root.label = "no"
		elif len(negInstances)==0:
			root.label = "yes"
		else:
			yesposI = []
			yesnegI = []
			noposI = []
			nonegI = []
			for dictionary in posInstances:
				if int(indexOfmaxig) in dictionary:
					yesposI.append(dictionary)
				else:
					noposI.append(dictionary)
			for dictionary in  negInstances:
				if int(indexOfmaxig) in dictionary:
					yesnegI.append(dictionary)
				else:
					nonegI.append(dictionary)
			node1 = root.insert("attr",yesposI,yesnegI,"left","notleaf")
			node2 = root.insert("attr",noposI,nonegI,"right","notleaf")
			attributes.remove(indexOfmaxig)
			splitting(node1,yesposI,yesnegI,attributes,root)
			splitting(node2,noposI,nonegI,attributes,root)
		#checking the test examples to find the percentage of correct predictions
		totalcorrect = 0
		lines = [line.rstrip('\n') for line in open(sys.argv[1])]
		total = len(lines)
		for line in lines:
			l = line.split(" ")
			rating = int(l[0])
			ans = ""
			if(rating>=7):
				ans = "yes"
			if(rating<=4):
				ans = "no"
			myans = ""
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i + 1
				else:
					info = item.split(":")
					d[int(info[0])] = int(info[1])
			temp = root
			while True:
				if temp.label=="notleaf":
					if int(temp.attrib) in d:
						temp = temp.left
					else:
						temp = temp.right
				else:
					if temp.label=="yes":
						myans = "yes"
					elif temp.label=="no":
						myans = "no"
					if myans==ans:
						totalcorrect = totalcorrect + 1
					break

		correctPercent = totalcorrect/total
		correctPercent = correctPercent*100
		print("\n\nid3 after early stopping(stopped at num of examples in a node<30): \n\nAccuracy: ",correctPercent)
		print("\nnum of leaves: ",root.count_leaf_nodes())
		dict_attr_freq = root.count_attr_freq()
		i = 0
		print("\n5 most used attributes to split are(attributeIndex numOfTimesUsed): ")
		for key in sorted(dict_attr_freq.items(), key=lambda x: x[1], reverse=True):
			i = i+1
			print(key[0], "\t", key[1])
			if i>4:
				break
		totalcorrect = 0
		lines = [line.rstrip('\n') for line in open("train.txt")]
		total = len(lines)
		for line in lines:
			l = line.split(" ")
			rating = int(l[0])
			ans = ""
			if(rating>=7):
				ans = "yes"
			if(rating<=4):
				ans = "no"
			myans = ""
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i + 1
				else:
					info = item.split(":")
					d[int(info[0])] = int(info[1])
			temp = root
			while True:
				if temp.label=="notleaf":
					if int(temp.attrib) in d:
						temp = temp.left
					else:
						temp = temp.right
				else:
					if temp.label=="yes":
						myans = "yes"
					elif temp.label=="no":
						myans = "no"
					if myans==ans:
						totalcorrect = totalcorrect + 1
					break
		correctPercent = totalcorrect/total
		correctPercent = correctPercent*100
		print("Accuracy on training set after early stopping: ", correctPercent)

elif exptno == '3':
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
	class node:
	    def __init__(self, attrib, posinst, neginst, label):	
	        self.left = None 				#left child in the tree
	        self.right = None
	        self.attrib = attrib 			#attrib is the index of the word used as attribute in this node
	        self.posinst = posinst 			#posinst is the number of positive examples at this node
	        self.neginst = neginst
	        self.label = label				#label = "notleaf" OR "yes" if the prediction is positive(i.e. the movie review is positive) OR "no"-if the prediction is negative

	    def insert(self, attrib, posinst, neginst, lorR, label):
	    	if lorR == 'left':				#insert at the left child of the node
	    		self.left = node(attrib, posinst, neginst, label)
	    		return self.left
	    	elif lorR == 'right':
	    		self.right = node(attrib, posinst, neginst, label)
	    		return self.right

	import math
	def entropy(numpos,numneg):		#caclulate the entropy where numpos is the number of positive examples
		total = numpos + numneg
		if total==0:
			return 0
		ppos = numpos/total
		pneg = numneg/total
		if(ppos==0 or pneg==0):
			return 0
		return (-ppos)*math.log2(ppos)-pneg*math.log2(pneg)

	def splitting(node1,posI,negI,attr,parent):			#to create the children of node1 and then this is recursively called
		#print(len(posI),len(negI))
		
			ig = {}						#ig keeps the info gain for each of the attributes
			for index in attr:			#one by one see all attributes to check which has the max info gain
				yespos = 0				#num of positive examples(review pos) who has this "index" attribute
				nopos = 0				#num of positive examples who does not have this attribute
				yesneg = 0
				noneg = 0
				for itemDict in posI:		#posI is a list of dictionaries with each dictionary containing one positive review from the training set
					if int(index) in itemDict:
						yespos = yespos + 1
					else:
						nopos = nopos + 1
				for itemDict in negI:
					if int(index) in itemDict:
						yesneg = yesneg + 1
					else:
						noneg = noneg + 1
				totalI = len(posI) + len(negI)
				ig[index] = entropy(len(posI),len(negI)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
				#print(nopos, noneg, entropy(nopos,noneg))
			maxig = ig[list(ig.keys())[0]]			#find the max info gain of all the ig
			indexOfmaxig = list(ig.keys())[0]		#stores the index of max info gain
			for key in ig:
				if(ig[key]>maxig):
					maxig = ig[key]
					indexOfmaxig = key
			if maxig==0:
				if len(posI)<len(negI):
					node1.label = "no"
				else:
					node1.label = "yes"
			else:
				node1.attrib = indexOfmaxig			#made the attribute of this node as the one with max ig
				yesposI = []		#list of all instances which are positive reviewed and contains the attribute "indexofmaxig"
				yesnegI = []
				noposI = []
				nonegI = []
				for dictionary in posI:
					if int(indexOfmaxig) in dictionary:
						yesposI.append(dictionary)
					else:
						noposI.append(dictionary)
				for dictionary in  negI:
					if int(indexOfmaxig) in dictionary:
						yesnegI.append(dictionary)
					else:
						nonegI.append(dictionary)
				if len(yesposI)+len(yesnegI)==0:
					if len(posI)>len(negI):
						node1.label = "yes"
					else:
						node1.label = "no"
				elif len(noposI)+len(nonegI)==0:
					if len(posI)>len(negI):
						node1.label = "yes"
					else:
						node1.label = "no"
				else:
					node2 = node1.insert("attr",yesposI,yesnegI,"left","notleaf")	#create the two children of node1
					node3 = node1.insert("attr",noposI,nonegI,"right","notleaf")
					attrr = []
					attrri = []
					for item in attr:
						attrr.append(item)
						attrri.append(item)
					attrr.remove(indexOfmaxig)		#remove the attribute and then use the new attribute list
					attrri.remove(indexOfmaxig)
					splitting(node2,yesposI,yesnegI,attrr,node1)
					splitting(node3,noposI,nonegI,attrr,node1)


	attributes = [line.rstrip('\n') for line in open('selected-features-indices.txt')]	#extract the indices of words to be used as attribute
	posInstances = []
	negInstances = []
	lines = [line.rstrip('\n') for line in open('noisytrain.txt')]
	for line in lines:
		l = line.split(" ")
		if int(l[0])<=4:
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i+1
				else:
					tokens = item.split(":")
					d[int(tokens[0])] = int(tokens[1])
			negInstances.append(d)
		elif int(l[0])>=7:
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i+1
				else:
					tokens = item.split(":")
					d[int(tokens[0])] = int(tokens[1])
			posInstances.append(d)


	ig = {}
	for index in attributes:
		yespos = 0
		nopos = 0
		yesneg = 0
		noneg = 0
		for itemDict in posInstances:
			if int(index) in itemDict:
				yespos = yespos + 1
			else:
				nopos = nopos + 1
		for itemDict in negInstances:
			if int(index) in itemDict:
				yesneg = yesneg + 1
			else:
				noneg = noneg + 1
		totalI = len(posInstances) + len(negInstances)
		ig[index] = entropy(len(posInstances),len(negInstances)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
		#print(nopos, noneg, entropy(nopos,noneg))
	maxig = ig[list(ig.keys())[0]]
	indexOfmaxig = list(ig.keys())[0]
	for key in ig:
		if(ig[key]>maxig):
			maxig = ig[key]
			indexOfmaxig = key
	#print(maxig)
	root = node(indexOfmaxig,posInstances,negInstances,"notleaf")
	temp = root
	if(len(posInstances)==0):
		root.label = "no"
	elif len(negInstances)==0:
		root.label = "yes"
	else:
		yesposI = []
		yesnegI = []
		noposI = []
		nonegI = []
		for dictionary in posInstances:
			if int(indexOfmaxig) in dictionary:
				yesposI.append(dictionary)
			else:
				noposI.append(dictionary)
		for dictionary in  negInstances:
			if int(indexOfmaxig) in dictionary:
				yesnegI.append(dictionary)
			else:
				nonegI.append(dictionary)
		node1 = root.insert("attr",yesposI,yesnegI,"left","notleaf")
		node2 = root.insert("attr",noposI,nonegI,"right","notleaf")
		attributes.remove(indexOfmaxig)
		splitting(node1,yesposI,yesnegI,attributes,root)
		splitting(node2,noposI,nonegI,attributes,root)
	#checking the test examples to find the percentage of correct predictions
	totalcorrect = 0
	lines = [line.rstrip('\n') for line in open('test.txt')]
	total = len(lines)
	for line in lines:
		l = line.split(" ")
		rating = int(l[0])
		ans = ""
		if(rating>=7):
			ans = "yes"
		if(rating<=4):
			ans = "no"
		myans = ""
		d = {}
		i = 0
		for item in l:
			if(i==0):
				i = i + 1
			else:
				info = item.split(":")
				d[int(info[0])] = int(info[1])
		temp = root
		while True:
			if temp.label=="notleaf":
				if int(temp.attrib) in d:
					temp = temp.left
				else:
					temp = temp.right
			else:
				if temp.label=="yes":
					myans = "yes"
				elif temp.label=="no":
					myans = "no"
				if myans==ans:
					totalcorrect = totalcorrect + 1
				break

	correctPercent = totalcorrect/total
	correctPercent = correctPercent*100
	print("Effect of ",noise/10,"%  noise\n","Accuracy: ",correctPercent)

elif exptno == '4':
	print("The dependance of accuracy on num of pruned nodes is:\n")
	for pruneAmount in [0,0.3,5,100]:
		prunedNodes = 0
		class node:
		    def __init__(self, attrib, posinst, neginst, label):	
		        self.left = None 				#left child in the tree
		        self.right = None
		        self.attrib = attrib 			#attrib is the index of the word used as attribute in this node
		        self.posinst = posinst 			#posinst is the number of positive examples at this node
		        self.neginst = neginst
		        self.label = label				#label = "notleaf" OR "yes" if the prediction is positive(i.e. the movie review is positive) OR "no"-if the prediction is negative

		    def insert(self, attrib, posinst, neginst, lorR, label):
		    	if lorR == 'left':				#insert at the left child of the node
		    		self.left = node(attrib, posinst, neginst, label)
		    		return self.left
		    	elif lorR == 'right':
		    		self.right = node(attrib, posinst, neginst, label)
		    		return self.right
		    def count_nodes(self):
		    	nodes = []
		    	self.count_nodes_helper(nodes)
		    	return len(nodes)

		    def count_nodes_helper(self, nodes):
		    	nodes.append(self)
		    	if self.label == "notleaf":
		    		if self.left:
		    			self.left.count_nodes_helper(nodes)
		    		if self.right:
		    			self.right.count_nodes_helper(nodes)

		import math
		def entropy(numpos,numneg):		#caclulate the entropy where numpos is the number of positive examples
			total = numpos + numneg
			if total==0:
				return 0
			ppos = numpos/total
			pneg = numneg/total
			if(ppos==0 or pneg==0):
				return 0
			return (-ppos)*math.log2(ppos)-pneg*math.log2(pneg)

		def prune(node1):
			if(node1.label!="notleaf"):
				return
			else:
				prune(node1.right)
				prune(node1.left)
				totalcorrect = 0
				lines = [line.rstrip('\n') for line in open('test.txt')]
				total = len(lines)
				for line in lines:
					l = line.split(" ")
					rating = int(l[0])
					ans = ""
					if(rating>=7):
						ans = "yes"
					if(rating<=4):
						ans = "no"
					myans = ""
					d = {}
					i = 0
					for item in l:
						if(i==0):
							i = i + 1
						else:
							info = item.split(":")
							d[int(info[0])] = int(info[1])
					temp = node1
					while True:
						if temp.label=="notleaf":
							if int(temp.attrib) in d:
								temp = temp.left
							else:
								temp = temp.right
						else:
							if temp.label=="yes":
								myans = "yes"
							elif temp.label=="no":
								myans = "no"
							if myans==ans:
								totalcorrect = totalcorrect + 1
							break

				correctPercent = totalcorrect/total
				currentAccuracy = correctPercent*100
				if len(node1.posinst)>len(node1.neginst):
					node1.label = "yes"
				else:
					node1.label = "no"
				totalcorrect = 0
				lines = [line.rstrip('\n') for line in open('test.txt')]
				total = len(lines)
				for line in lines:
					l = line.split(" ")
					rating = int(l[0])
					ans = ""
					if(rating>=7):
						ans = "yes"
					if(rating<=4):
						ans = "no"
					myans = ""
					d = {}
					i = 0
					for item in l:
						if(i==0):
							i = i + 1
						else:
							info = item.split(":")
							d[int(info[0])] = int(info[1])
					temp = node1
					while True:
						if temp.label=="notleaf":
							if int(temp.attrib) in d:
								temp = temp.left
							else:
								temp = temp.right
						else:
							if temp.label=="yes":
								myans = "yes"
							elif temp.label=="no":
								myans = "no"
							if myans==ans:
								totalcorrect = totalcorrect + 1
							break

				correctPercent = totalcorrect/total
				newAccuracy = correctPercent*100
				global prunedNodes
				prunedNodes = prunedNodes + 1
				#print(newAccuracy-currentAccuracy)
				if (newAccuracy-currentAccuracy)<pruneAmount:
					node1.label = "notleaf"
					prunedNodes = prunedNodes - 1


		def splitting(node1,posI,negI,attr,parent):			#to create the children of node1 and then this is recursively called
			#print(len(posI),len(negI))
			
				ig = {}						#ig keeps the info gain for each of the attributes
				for index in attr:			#one by one see all attributes to check which has the max info gain
					yespos = 0				#num of positive examples(review pos) who has this "index" attribute
					nopos = 0				#num of positive examples who does not have this attribute
					yesneg = 0
					noneg = 0
					for itemDict in posI:		#posI is a list of dictionaries with each dictionary containing one positive review from the training set
						if int(index) in itemDict:
							yespos = yespos + 1
						else:
							nopos = nopos + 1
					for itemDict in negI:
						if int(index) in itemDict:
							yesneg = yesneg + 1
						else:
							noneg = noneg + 1
					totalI = len(posI) + len(negI)
					ig[index] = entropy(len(posI),len(negI)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
					#print(nopos, noneg, entropy(nopos,noneg))
				maxig = ig[list(ig.keys())[0]]			#find the max info gain of all the ig
				indexOfmaxig = list(ig.keys())[0]		#stores the index of max info gain
				for key in ig:
					if(ig[key]>maxig):
						maxig = ig[key]
						indexOfmaxig = key
				if maxig==0:
					if len(posI)<len(negI):
						node1.label = "no"
					else:
						node1.label = "yes"
				else:
					node1.attrib = indexOfmaxig			#made the attribute of this node as the one with max ig
					yesposI = []		#list of all instances which are positive reviewed and contains the attribute "indexofmaxig"
					yesnegI = []
					noposI = []
					nonegI = []
					for dictionary in posI:
						if int(indexOfmaxig) in dictionary:
							yesposI.append(dictionary)
						else:
							noposI.append(dictionary)
					for dictionary in  negI:
						if int(indexOfmaxig) in dictionary:
							yesnegI.append(dictionary)
						else:
							nonegI.append(dictionary)
					if len(yesposI)+len(yesnegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					elif len(noposI)+len(nonegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					else:
						node2 = node1.insert("attr",yesposI,yesnegI,"left","notleaf")	#create the two children of node1
						node3 = node1.insert("attr",noposI,nonegI,"right","notleaf")
						attrr = []
						attrri = []
						for item in attr:
							attrr.append(item)
							attrri.append(item)
						attrr.remove(indexOfmaxig)		#remove the attribute and then use the new attribute list
						attrri.remove(indexOfmaxig)
						splitting(node2,yesposI,yesnegI,attrr,node1)
						splitting(node3,noposI,nonegI,attrr,node1)


		attributes = [line.rstrip('\n') for line in open('selected-features-indices.txt')]	#extract the indices of words to be used as attribute
		posInstances = []
		negInstances = []
		lines = [line.rstrip('\n') for line in open('train.txt')]
		for line in lines:
			l = line.split(" ")
			if int(l[0])<=4:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				negInstances.append(d)
			elif int(l[0])>=7:
				d = {}
				i = 0
				for item in l:
					if(i==0):
						i = i+1
					else:
						tokens = item.split(":")
						d[int(tokens[0])] = int(tokens[1])
				posInstances.append(d)


		ig = {}
		for index in attributes:
			yespos = 0
			nopos = 0
			yesneg = 0
			noneg = 0
			for itemDict in posInstances:
				if int(index) in itemDict:
					yespos = yespos + 1
				else:
					nopos = nopos + 1
			for itemDict in negInstances:
				if int(index) in itemDict:
					yesneg = yesneg + 1
				else:
					noneg = noneg + 1
			totalI = len(posInstances) + len(negInstances)
			ig[index] = entropy(len(posInstances),len(negInstances)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
			#print(nopos, noneg, entropy(nopos,noneg))
		maxig = ig[list(ig.keys())[0]]
		indexOfmaxig = list(ig.keys())[0]
		for key in ig:
			if(ig[key]>maxig):
				maxig = ig[key]
				indexOfmaxig = key
		#print(maxig)
		root = node(indexOfmaxig,posInstances,negInstances,"notleaf")
		temp = root
		if(len(posInstances)==0):
			root.label = "no"
		elif len(negInstances)==0:
			root.label = "yes"
		else:
			yesposI = []
			yesnegI = []
			noposI = []
			nonegI = []
			for dictionary in posInstances:
				if int(indexOfmaxig) in dictionary:
					yesposI.append(dictionary)
				else:
					noposI.append(dictionary)
			for dictionary in  negInstances:
				if int(indexOfmaxig) in dictionary:
					yesnegI.append(dictionary)
				else:
					nonegI.append(dictionary)
			node1 = root.insert("attr",yesposI,yesnegI,"left","notleaf")
			node2 = root.insert("attr",noposI,nonegI,"right","notleaf")
			attributes.remove(indexOfmaxig)
			splitting(node1,yesposI,yesnegI,attributes,root)
			splitting(node2,noposI,nonegI,attributes,root)
		#checking the test examples to find the percentage of correct predictions
		print("Nodes before pruning",root.count_nodes())
		prune(root)
		print("Nodes after pruning",root.count_nodes())
		totalcorrect = 0
		lines = [line.rstrip('\n') for line in open('test.txt')]
		total = len(lines)
		for line in lines:
			l = line.split(" ")
			rating = int(l[0])
			ans = ""
			if(rating>=7):
				ans = "yes"
			if(rating<=4):
				ans = "no"
			myans = ""
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i + 1
				else:
					info = item.split(":")
					d[int(info[0])] = int(info[1])
			temp = root
			while True:
				if temp.label=="notleaf":
					if int(temp.attrib) in d:
						temp = temp.left
					else:
						temp = temp.right
				else:
					if temp.label=="yes":
						myans = "yes"
					elif temp.label=="no":
						myans = "no"
					if myans==ans:
						totalcorrect = totalcorrect + 1
					break

		correctPercent = totalcorrect/total
		correctPercent = correctPercent*100
		print(" Accuracy: ",correctPercent)

elif exptno == '5':
	print("Effect of number of trees in forrest on accuracy:\n")
	for numoftrees in [5,10,15,25]:
		class node:
		    def __init__(self, attrib, posinst, neginst, label):	
		        self.left = None 				#left child in the tree
		        self.right = None
		        self.attrib = attrib 			#attrib is the index of the word used as attribute in this node
		        self.posinst = posinst 			#posinst is the number of positive examples at this node
		        self.neginst = neginst
		        self.label = label				#label = "notleaf" OR "yes" if the prediction is positive(i.e. the movie review is positive) OR "no"-if the prediction is negative

		    def insert(self, attrib, posinst, neginst, lorR, label):
		    	if lorR == 'left':				#insert at the left child of the node
		    		self.left = node(attrib, posinst, neginst, label)
		    		return self.left
		    	elif lorR == 'right':
		    		self.right = node(attrib, posinst, neginst, label)
		    		return self.right

		import math
		def entropy(numpos,numneg):		#caclulate the entropy where numpos is the number of positive examples
			total = numpos + numneg
			if total==0:
				return 0
			ppos = numpos/total
			pneg = numneg/total
			if(ppos==0 or pneg==0):
				return 0
			return (-ppos)*math.log2(ppos)-pneg*math.log2(pneg)

		def splitting(node1,posI,negI,attr,parent):			#to create the children of node1 and then this is recursively called
			#print(len(posI),len(negI))
			
				ig = {}						#ig keeps the info gain for each of the attributes
				for index in attr:			#one by one see all attributes to check which has the max info gain
					yespos = 0				#num of positive examples(review pos) who has this "index" attribute
					nopos = 0				#num of positive examples who does not have this attribute
					yesneg = 0
					noneg = 0
					for itemDict in posI:		#posI is a list of dictionaries with each dictionary containing one positive review from the training set
						if int(index) in itemDict:
							yespos = yespos + 1
						else:
							nopos = nopos + 1
					for itemDict in negI:
						if int(index) in itemDict:
							yesneg = yesneg + 1
						else:
							noneg = noneg + 1
					totalI = len(posI) + len(negI)
					ig[index] = entropy(len(posI),len(negI)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
					#print(nopos, noneg, entropy(nopos,noneg))
				maxig = ig[list(ig.keys())[0]]			#find the max info gain of all the ig
				indexOfmaxig = list(ig.keys())[0]		#stores the index of max info gain
				for key in ig:
					if(ig[key]>maxig):
						maxig = ig[key]
						indexOfmaxig = key
				if maxig==0:
					if len(posI)<len(negI):
						node1.label = "no"
					else:
						node1.label = "yes"
				else:
					node1.attrib = indexOfmaxig			#made the attribute of this node as the one with max ig
					yesposI = []		#list of all instances which are positive reviewed and contains the attribute "indexofmaxig"
					yesnegI = []
					noposI = []
					nonegI = []
					for dictionary in posI:
						if int(indexOfmaxig) in dictionary:
							yesposI.append(dictionary)
						else:
							noposI.append(dictionary)
					for dictionary in  negI:
						if int(indexOfmaxig) in dictionary:
							yesnegI.append(dictionary)
						else:
							nonegI.append(dictionary)
					if len(yesposI)+len(yesnegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					elif len(noposI)+len(nonegI)==0:
						if len(posI)>len(negI):
							node1.label = "yes"
						else:
							node1.label = "no"
					else:
						node2 = node1.insert("attr",yesposI,yesnegI,"left","notleaf")	#create the two children of node1
						node3 = node1.insert("attr",noposI,nonegI,"right","notleaf")
						attrr = []
						attrri = []
						for item in attr:
							attrr.append(item)
							attrri.append(item)
						attrr.remove(indexOfmaxig)		#remove the attribute and then use the new attribute list
						attrri.remove(indexOfmaxig)
						splitting(node2,yesposI,yesnegI,attrr,node1)
						splitting(node3,noposI,nonegI,attrr,node1)

		import random
		attributesMain = [line.rstrip('\n') for line in open('selected-features-indices.txt')]	#extract the indices of words to be used as attribute
		rootList = []
		for loop in  range(1,numoftrees):
			attributes = []
			attrmap = {};
			itr = 0
			for item1 in attributesMain:
				attrmap[itr] = item1
				itr = itr + 1
			lis = random.sample(range(0,4999),2000)
			for item1 in lis:
				attributes.append(attrmap[item1])
			posInstances = []
			negInstances = []
			lines = [line.rstrip('\n') for line in open('train.txt')]
			for line in lines:
				l = line.split(" ")
				if int(l[0])<=4:
					d = {}
					i = 0
					for item in l:
						if(i==0):
							i = i+1
						else:
							tokens = item.split(":")
							d[int(tokens[0])] = int(tokens[1])
					negInstances.append(d)
				elif int(l[0])>=7:
					d = {}
					i = 0
					for item in l:
						if(i==0):
							i = i+1
						else:
							tokens = item.split(":")
							d[int(tokens[0])] = int(tokens[1])
					posInstances.append(d)

			ig = {}
			for index in attributes:
				yespos = 0
				nopos = 0
				yesneg = 0
				noneg = 0
				for itemDict in posInstances:
					if int(index) in itemDict:
						yespos = yespos + 1
					else:
						nopos = nopos + 1
				for itemDict in negInstances:
					if int(index) in itemDict:
						yesneg = yesneg + 1
					else:
						noneg = noneg + 1
				totalI = len(posInstances) + len(negInstances)
				ig[index] = entropy(len(posInstances),len(negInstances)) - (yespos+yesneg)/totalI*entropy(yespos,yesneg) - (nopos+noneg)/totalI*entropy(nopos,noneg)
				#print(nopos, noneg, entropy(nopos,noneg))
			maxig = ig[list(ig.keys())[0]]
			indexOfmaxig = list(ig.keys())[0]
			for key in ig:
				if(ig[key]>maxig):
					maxig = ig[key]
					indexOfmaxig = key
			#print(maxig)
			root = node(indexOfmaxig,posInstances,negInstances,"notleaf")
			temp = root
			if(len(posInstances)==0):
				root.label = "no"
			elif len(negInstances)==0:
				root.label = "yes"
			else:
				yesposI = []
				yesnegI = []
				noposI = []
				nonegI = []
				for dictionary in posInstances:
					if int(indexOfmaxig) in dictionary:
						yesposI.append(dictionary)
					else:
						noposI.append(dictionary)
				for dictionary in  negInstances:
					if int(indexOfmaxig) in dictionary:
						yesnegI.append(dictionary)
					else:
						nonegI.append(dictionary)
				node1 = root.insert("attr",yesposI,yesnegI,"left","notleaf")
				node2 = root.insert("attr",noposI,nonegI,"right","notleaf")
				attributes.remove(indexOfmaxig)
				splitting(node1,yesposI,yesnegI,attributes,root)
				splitting(node2,noposI,nonegI,attributes,root)
			rootList.append(root)
		#checking the test examples to find the percentage of correct predictions
		totalcorrect = 0
		lines = [line.rstrip('\n') for line in open('test.txt')]
		total = len(lines)
		for line in lines:
			l = line.split(" ")
			rating = int(l[0])
			ans = ""
			if(rating>=7):
				ans = "yes"
			if(rating<=4):
				ans = "no"
			myans = ""
			d = {}
			i = 0
			for item in l:
				if(i==0):
					i = i + 1
				else:
					info = item.split(":")
					d[int(info[0])] = int(info[1])
			numyes = 0
			numno = 0
			for itr in range(0,numoftrees-1):
				temp = rootList[itr]
				while True:
					if temp.label=="notleaf":
						if int(temp.attrib) in d:
							temp = temp.left
						else:
							temp = temp.right
					else:
						if temp.label=="yes":
							numyes = numyes + 1
						elif temp.label=="no":
							numno = numno + 1
						break
			if(numyes>=numno):
				myans = "yes"
			else:
				myans = "no"
			if(myans==ans):
				totalcorrect = totalcorrect + 1

		correctPercent = totalcorrect/total
		correctPercent = correctPercent*100
		print("NumOftress: ",numoftrees,"Accuracy: ",correctPercent)