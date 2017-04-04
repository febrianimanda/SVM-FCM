from datetime import datetime
import dateutil.parser
import csv, pickle, ast

datasetDir = 'dataset/'
exportDir = 'exported/'

def printOut(name, mode='Load'):
	print mode + "\t| " + name + " successfull"

def saveListToFile(filename, myList):
	thefile = open(exportDir+filename, 'w')
	for item in myList:
		print>>thefile, item
	printOut(filename, mode='Save to txt')
	thefile.close()

def readListFromFile(filename):
	f = open(exportDir+filename,'r')
	myList = [ast.literal_eval(line) for line in f]
	f.close()
	printOut(filename)
	return myList

def saveListToPickle(filename, myList):
	with open(exportDir+filename,'wb') as f:
		pickle.dump(myList, f)
	printOut(filename, mode='Save to pickle')

def readListFromPickle(filename):
	with open('exported/'+filename,'rb') as f:
		data = pickle.load(f)
		printOut(filename)
		return data

def saveDictToCSV(filename, fieldnames, data):
	with open(exportDir+filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in data:
			writer.writerow(item)
	printOut(filename, mode='Save to csv')

def readDictFromCSV(filename):
	f = open(exportDir+filename,'rb')
	reader = csv.DictReader(csvfile)
	f.close()
	printOut(filename)
	return reader