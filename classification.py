import iofile, numpy as np
from sklearn import svm


def processingData(mode='train'):
	mentah = iofile.readListFromPickle('browsing-session-'+mode+'-pickle.txt')
	data = []
	target = []
	for line in mentah:
		obj = [line['details'], line['duration'], line['page_per_time']]
		target.append(line['class'])
		data.append(obj)
	return data, target

data, target = processingData()
X = np.array(data)
print X
print X.shape