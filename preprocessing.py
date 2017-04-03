from datetime import datetime
import dateutil.parser, numpy
import iofile

user_keys = ['sessionId', 'class', 'details', 'duration', 'page_per_time', 'browsed_page']
product_keys = ['produk', 'jumlah']

def getIndex(lst, key, val):
	return next(index for (index, d) in enumerate(lst) if d[key] == val)

def getDuration(startTime, endTime):
	diff = endTime - startTime
	return diff.total_seconds()

def createUser(sesId, isBuy, list_page, duration, page_per_time):
	# info is array of information for fulfill the user_keys
	# checkout_success	: the variable indication wheteger the session contained the 
	#		checkout success interaction (1 if a purchase was realized successfully in session 
	#		and 0 otherwise)
	# details						: the number of visited pages with detailed information about products
	# duration 					: the session in duration (in seconds)
	# page_per_time 		: the mean time per page (in seconds)
	# browsed_page 			: list of browsed pages in array 
	userInfo = [sesId, isBuy, len(list_page), duration, page_per_time, list_page]
	users = dict(zip(user_keys, userInfo))
	print "User added", users
	return users

def getMeanVisit(listTime):
	if len(listTime) < 2:
		return 0
	listDuration = []
	for i in xrange(len(listTime)-1):
		listDuration.append(getDuration(listTime[i],listTime[i+1]))
	return sum(listDuration) / (len(listTime)-1)

def processingBuy(filename):
	f = open(datasetDir+filename,'r')
	listBuySession = []
	buying_keys = ['sessionId','timestamp','itemId','price','qty']
	for line in f:
		line = line.rstrip('\n')
		info = line.split(',')
		session = dict(zip(buying_keys, info))
		listBuySession.append(session)
	return listBuySession

def getAllBuyingSession():
	f = open(datasetDir+'yoochoose-buys.txt','r')
	listSession = []
	i = 0
	j = 0
	for line in f:
		sesId = line.split(',')[0]
		i += 1
		if sesId not in listSession:
			j += 1
			print "adding",sesId,' | ',j,' added from ',i
			listSession.append(sesId)
	f.close()
	return listSession

def getAllProducts(filename, listProducts = []):
	f = open(iofile.datasetDir+filename,'r')
	for line in f:
		items = line.split(',')
		if items[2] not in (x['produk'] for x in listProducts):
			product = {'produk': items[2], 'jumlah': 1}
			listProducts.append(product)
			print "Create product",items[2]
		else:
			ix = getIndex(listProducts, 'produk', items[2])
			listProducts[ix]['jumlah'] += 1
			print "Add product",items[2]
	f.close()
	return listProducts

def processingBrowsing(filename, buyingSession, mode='Train'):
	f = open(iofile.datasetDir+filename,'r') 
	listTime, listPage, listUser, listBuy = [],[],[],[]
	sesId = '1' if mode=='Train' else '150019' #users session id start
	i = 0
	j = 0
	for line in f:
		j += 1
		arrLine = line.split(',')
		newSesId = arrLine[0]
		if j > 1:
			if sesId != newSesId:
				i += 1
				meanTime = getMeanVisit(listTime)
				duration = getDuration(listTime[0],listTime[-1])
				buyStatus = 'buy' if sesId in buyingSession else 'browse'
				print i,
				listUser.append(createUser(sesId, buyStatus, listPage, duration, meanTime))
				if buyStatus == 1:
					listBuy.append(sesId)
				sesId = newSesId
				listTime, listPage = [],[]
		listTime.append(dateutil.parser.parse(arrLine[1]))
		listPage.append(arrLine[2])
	iofile.saveListToPickle('buying-session-'+mode, listBuy)
	print "Successfully save",i,"users"
	f.close()
	return listUser


browsingSessionTrain = iofile.readListFromFile('browsing-session-train.txt')
iofile.saveDictToCSV('browsing-session-train.csv', user_keys, browsingSessionTrain)

# nProcessingUsers = 100000