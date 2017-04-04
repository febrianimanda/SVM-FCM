from datetime import datetime
import dateutil.parser, numpy
import iofile

user_keys = ['sessionId', 'class', 'details', 'duration', 'page_per_time', 'browsed_page', 'cart']
product_keys = ['produk', 'jumlah']
buying_keys = ['sessionId','timestamp','itemId','price','qty']

def getIndex(lst, key, val): # return value is index, use it for list of dictionary
	return next(index for (index, d) in enumerate(lst) if d[key] == val)

def getDict(lst, key, val): # return value is dictionary, use it for list of dictionary
	return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(lst))


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
	for line in f:
		line = line.rstrip('\n')
		info = line.split(',')
		session = dict(zip(buying_keys, info))
		listBuySession.append(session)
	return listBuySession

def getAllBuyingSession():
	f = open(iofile.datasetDir+'yoochoose-buys.txt','r')
	listSession = []
	i = 0
	j = 0
	for line in f:
		line = line.rstrip('\n')
		data = line.split(',')
		sesId = data[0]
		if int(sesId) < 302080: #jumlah session
			i += 1
			exist = any(d['sessionId'] == sesId for d in listSession)
			if not exist:
				sesDict = {
					'sessionId':sesId,
					'listBuy':[dict(zip(buying_keys, data))]
				}
				j += 1
				print "adding",sesId,'\t| ',j,' added from ',i
				listSession.append(sesDict)
			else:
				print "adding buy list from ",sesId
				ix = getIndex(listSession, 'sessionId', sesId)  
				sessionDict = listSession[ix]
				buyDict = dict(zip(buying_keys, data))
				sessionDict['listBuy'].append(buyDict)
	print "Jumlah session ",j," dari total ",i
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
	buySessionList = [d['sessionId'] for d in buyingSession]
	i = 0
	j = 0
	for line in f:
		j += 1
		arrLine = line.split(',')
		newSesId = arrLine[0]
		# shopList = []
		if j > 1:
			if sesId != newSesId:
				i += 1
				print i,
				buyStatus = 'buy' if sesId in buySessionList else 'browse'
				if buyStatus == 'buy':
					listBuy.append(sesId)
					# ix = getIndex(buyingSession, 'sessionId', sesId)
					# for lst in d['listBuy']:
					# 	listTime.append(dateutil.parser.parse(lst['timestamp']))
					# 	shopList.append(lst['itemId'])
				meanTime = getMeanVisit(listTime)
				duration = getDuration(listTime[0],listTime[-1])
				# listUser.append(createUser(sesId, buyStatus, listPage, duration, meanTime, shopList))
				listUser.append(createUser(sesId, buyStatus, listPage, duration, meanTime ))
				sesId = newSesId
				listTime, listPage = [],[]
		listTime.append(dateutil.parser.parse(arrLine[1]))
		listPage.append(arrLine[2])
	iofile.saveListToPickle('buying-session-'+mode, listBuy)
	print "Successfully save",i,"users"
	f.close()
	return listUser

buyingSession = iofile.readListFromPickle('buying-session-pickle.txt')
browsingSession = processingBrowsing('yoochoose-click-train.txt', buyingSession)
browsingSessionTest = processingBrowsing('yoochoose-click-test.txt', buyingSession, mode='Test')
iofile.saveListToFile('browsing-session-train.txt', browsingSession)
iofile.saveListToFile('browsing-session-test.txt', browsingSessionTest)

# nProcessingUsers = 100000