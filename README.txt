To run->
python3 id3.py test.txt <exptno>

exptno = 2-5
Here, instead of test.txt, you can put any file with the test instances(format of the test file should be same as given in the question)
exptno=2 => Two decision trees will be made one without early stopping and one with early stopping and their statistics are displayed
exptno=3 => The effect of noise can be seen
exptno=4 => Multiple trees are constructed for different number of pruned nodes and accuracies are displayed
exptno=5 => Random forrest using feature bagging is constructed and its accuracy calculated



NOTE:

InstancesExtract.py extracts 500 positive and 500 negative examples randomly from TRAINlabeledBow.feat and creates a file train.txt which is to be used as training set for my learning tree, it also extracts 500 positive and 500 negative examples randomly from TESTlabeledBow.feat and stores it in a file named test.txt which is to be used by the decision tree to make predictions.

minvocab.py extracts top 1000 words from the file imdb.vocab according to frequency of these words used in the file TRAINlabeledBow.feat and 2500 most frequently used words with polarity>+1 and 2500 words with polarity<-0.5 are chosen and saved in selected-features-indices.txt to be used as attributes for my id3 algo.

noisytrain.txt is created by id3.py and the amount of noise may be adjusted in the file id3.py at line no. 585, currently the amount of noise is 10%

tain.txt and test.txt are created by instancesExtract.py
