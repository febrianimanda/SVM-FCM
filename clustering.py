import iofile, numpy as np, pickle
from pymongo import MongoClient

client = MongoClient()
db = client.yoochoose

buyingSession = iofile.readPickle('test-cluster-1.pkl')
N = len(buyingSession)
C = 6
q = 2.5

def getIndex(lst, key, val): # return value is index, use it for list of dictionary
	return next(index for (index, d) in enumerate(lst) if d[key] == val)

def getProducts(sessions):
	listPages = []
	for session in sessions:
		for page in session['browsed_page']:
			try:
				ix = getIndex(listPages, 'page', page)
				listPages[ix]['jumlah'] += 1
			except Exception as e:
				obj = {'page':page, 'jumlah': 1}
				listPages.append(obj)
	return listPages

products =  getProducts(buyingSession)

def filteringProducts(products, x):
	j = 0
	filtered, pages = [], []
	for product in products:
		if product['jumlah'] > x:
			j+= 1
			print product['jumlah'],
			filtered.append(product)
			pages.append(product['page'])
	print "\n",j, len(products)
	return pages, filtered

filteredPages, filteredProducts = filteringProducts(products, 3)
print filteredPages

def collectAllPages(session):
	print "== Collecting All Pages =="
	pages = []
	for obj in session:
		for page in obj['browsed_page']:
			if page not in pages:
				pages.append(page)
	pages.sort()
	print "Done\n"
	return pages

pages = collectAllPages(buyingSession)

def getSessionParam():
	print "== Get Session Param =="
	data = []
	for obj in buyingSession:
		arr = np.zeros(len(pages))
		for i in range(len(pages)):
			if pages[i] in obj['browsed_page']:
				arr[i] = obj['browsed_page'].count(pages[i])
		data.append(arr)
	print "Done\n"
	return data

def saveSessionParams():
	print "== Save Session Param =="
	ix = 0
	print "delete all rows in param"
	db.params.drop()
	print "collecting all params"
	for obj in buyingSession:
		arr = [0 for i in range(len(pages))]
		for i in range(len(pages)):
			if pages[i] in obj['browsed_page']:
				arr[i] = obj['browsed_page'].count(pages[i])
		obj = {'index':ix,'sessionId': obj['sessionId'], 'pages': arr}
		db.params.insert_one(obj)
		ix += 1
	print "Done\n"

def euclidean(a, b):
	return np.linalg.norm(a-b)

def calcCenter(X, c, j):
	atas = 0
	bawah = 1
	for i in range(N):
		atas += np.multiply(calcMembership(X,c,i,j), X[i])
	for i in range(N):
		bawah += calcMembership(X,c,i,j)
	Cj = np.divide(atas, bawah)
	return Cj

def dbCalcCenter(c, j):
	atas = 0
	bawah = 1
	for i in range(N):
		X = db.params.find_one({'index':i})
		Xi = np.array(X['pages'])
		atas += np.multiply(dbCalcMembership(c,i,j), Xi)
	for i in range(N):
		bawah += dbCalcMembership(c,i,j)
	Cj = np.divide(atas, bawah)
	return Cj

def calcMembership(X, c, i, j):
	bawah = 0
	for k in range(C):
		pangkat = 2 / (q-1)
		div = (euclidean(X[i], c[j]) / euclidean(X[i], c[k]))
		res = div ** pangkat
		bawah += res
	Mic = 1 / bawah
	return Mic

def dbCalcMembership(c, i, j):
	bawah = 0
	for k in range(C):
		pangkat = 2 / (q-1)
		X = db.params.find_one({'index':i})
		Xi = np.array(X['pages'])
		div = (euclidean(Xi, c[j]) / euclidean(Xi, c[k]))
		res = div ** pangkat
		bawah += res
	Mic = 1 / bawah
	return Mic

def calcObjectiveFunction(X,c):
	jm = 0
	for i in range(N):
		for j in range(C):
			jm += calcMembership(X, c, i, j) * (euclidean(X[i],c[j]) ** 2)
	return Jm

def fuzzyClustering():
	c = np.random.rand(C, len(pages))
	stop, k, elm = False, 1, .03
	m = np.random.rand(N, C)
	while not stop:
		k += 1
		# save old m
		oldm = np.array(m, copy=True)

		# caluclate the centers (Cj)
		for j in range(C):
			print "calculate center of cluster",j
			c[j] = dbCalcCenter(c,j)

		# update Fuzzy Membership
		for i in range(N):
			for j in range(C):
				print "Updating membership session",i,"in cluster",j
				m[i][j] = dbCalcMembership(c, i, j)

		if k > 1:
			Jm = euclidean(oldm, m)
			print k," \t| ", Jm
			if Jm < elm or k > 100: stop = True
			else: print "Process again"
	print "Done\n"
	return c, m

def processingFCM():
	print "=== Run Fuzzy C Means ==="
	# initialize Fuzzy Membership Value
	X = np.array(getSessionParam())
	c = np.random.rand(C, len(pages))
	stop, k, elm = False, 1, .005
	m = np.random.rand(N, C)
	while not stop:
		k += 1
		# save old m
		oldm = np.array(m, copy=True)

		# caluclate the centers (Cj)
		for j in range(C):
			print "calculate center of cluster",j
			c[j] = calcCenter(X,c,j)

		# update Fuzzy Membership
		for i in range(N):
			for j in range(C):
				print "Updating membership session",i,"in cluster",j
				m[i][j] = calcMembership(X, c, i, j)

		if k > 1:
			Jm = euclidean(oldm, m)
			print k," \t| ", Jm
			if Jm < elm or k > 100: stop = True
			else: print "Process again"
	print "Done\n"
	return c, m

center, membership = processingFCM()
# membership = iofile.readPickle('fcm-membership-1.pkl')
# center = iofile.readPickle('fcm-center-1.pkl')

listCenter = []

for koord in center:
	print koord
	obj = {'kord': koord, 'member': []}
	listCenter.append(obj)

print ""
j = 1
for item in membership:
	j += 1
	ix = [i for i, x in enumerate(item) if x == max(item)][0]
	listCenter[ix]['member'].append(j)
	print "session %s to center %s" % (j, ix)

for i, x in enumerate(listCenter):
	print i, x['member'], "\n"
