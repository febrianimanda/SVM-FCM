from datetime import datetime
import dateutil.parser
import csv, pickle, ast

datasetDir = 'dataset/'
exportDir = 'exported/'

def saveListToFile(filename, myList):
	thefile = open(exportDir+filename, 'w')
	for item in myList:
		print>>thefile, item
	print "Saving file successfully"
	thefile.close()

def readListFromFile(filename):
	f = open(exportDir+filename,'r')
	myList = [ast.literal_eval(line) for line in f]
	f.close()
	return myList

def saveListToPickle(filename, myList):
	with open(exportDir+filename,'wb') as f:
		pickle.dump(myList, f)
	print "Saving with pickle successfully"

def readListFromPickle(filename):
	with open('exported/'+filename,'rb') as f:
		return pickle.load(f)

def saveDictToCSV(filename, fieldnames, data):
	with open(exportDir+filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in data:
			writer.writerow(item)
	print "%s.csv | Save successfull" % (filename)

def readDictFromCSV(filename):
	f = open(exportDir+filename,'rb')
	reader = csv.DictReader(csvfile)
	f.close()
	return reader