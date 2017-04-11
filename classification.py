import iofile, numpy as np, pickle
from sklearn import svm
# import matplotlib.pyplot as plt

def processingData(mode='train'):
	mentah = iofile.readPickle('browsing-session-'+mode+'-pickle.txt')
	data = []
	target = []
	i = 0
	for line in mentah:
		i += 1
		obj = [line['details'], line['duration'], line['page_per_time']]
		c = 1 if line['class'] == 'buy' else 0
		target.append(c)
		data.append(obj)
	return data, target


data, target = processingData()
X = np.array(data)
y = np.array(target)

# print X.shape
# svc = svm.SVC(kernel='linear', C=0.1).fit(X,y)
svc = iofile.readPickle('svc-pickle.pkl')
# print "save done"
Z = svc.predict(X)
print "jumlah target 0 : %d" % (y == 0).sum()
print "jumlah target 1 : %d" % (y == 1).sum()

mislabeled = (y != Z).sum()
correct = len(y) - mislabeled
percent = float(correct) / len(y) * 100
print "Number of correct points : %d" % correct
print "Number of mislabeled points : %d" % mislabeled
print "Correct Percentage : %f%s" % (percent,'%')
# print svc
# print Z