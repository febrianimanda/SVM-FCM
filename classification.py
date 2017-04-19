import iofile, numpy as np, pickle
from sklearn import svm
# import matplotlib.pyplot as plt

def processingData(rawData):
	data = []
	target = []
	i = 0
	for line in rawData:
		i += 1
		obj = [line['details'], line['duration'], line['page_per_time']]
		c = 1 if line['class'] == 'buy' else 0
		target.append(c)
		data.append(obj)
	return data, target

def confussionMatrix(model, testData, target):
	Z = model.predict(testData)
	cm = {
		'tp': 0, 'fp': 0,
		'tn': 0, 'fn': 0
	}
	for ix in range(len(Z)):
		if Z[ix] == 1:
			if target[ix] == Z[ix]: cm['tp'] += 1
			else: cm['fp'] += 1
		else:
			if target[ix] == Z[ix]: cm['tn'] += 1
			else: cm['fn'] += 1
	print cm
	return cm

def errorRate(confMatrix):
	return float(confMatrix['fp'] + confMatrix['fn']) / float(confMatrix['fp'] + confMatrix['fn'] + confMatrix['tp'] + confMatrix['tn'])

def accuracy(confMatrix):
	return float(confMatrix['tp'] + confMatrix['tn']) / float(confMatrix['fp'] + confMatrix['fn'] + confMatrix['tp'] + confMatrix['tn'])

def sensitivity(confMatrix):
	return float(confMatrix['tp']) / float(confMatrix['tp'] + confMatrix['fn'])

def getBuyingSession(rawData, testData, model):
	Z = model.predict(testData)
	data =  []
	for ix in range(len(Z)):
		if Z[ix] == 1:
			data.append(rawData[ix])
			print "add to buying session: ",rawData[ix]
	print len(data)
	iofile.savePickle('buys-1.pkl')
	return data

rawData = iofile.readPickle('clicks-combine.pkl')
data, target = processingData(rawData)
X = np.array(data)
y = np.array(target)

# svc = svm.SVC(kernel='linear', C=0.1, verbose=10).fit(X,y)
# iofile.savePickle('svc-pickle.pkl')
svc = iofile.readPickle('svc-pickle.pkl')

confMatrix = confussionMatrix(svc, data, target)
print "Error Rate: ",errorRate(confMatrix)
print "Accuracy: ",accuracy(confMatrix)
print "Sensitivity: ",sensitivity(confMatrix)