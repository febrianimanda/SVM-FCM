from datetime import datetime
import dateutil.parser
import csv, pickle, ast, os.path

datasetDir = 'dataset/'
exportDir = 'exported/'

def printOut(name, mode='Load'):
	print mode + "\t| " + name + " successfull"

def printProgress(name, mode='Loading'):
	print mode + " file " + name

def saveListToFile(filename, myList):
	printProgress(filename, 'saving')
	thefile = open(exportDir+filename, 'w')
	for item in myList:
		print>>thefile, item
	printOut(filename, mode='Save to txt')
	thefile.close()

def readListFromFile(filename):
	printProgress(filename)
	f = open(exportDir+filename,'r')
	myList = [ast.literal_eval(line) for line in f]
	f.close()
	printOut(filename)
	return myList

def savePickle(filename, myList):
	printProgress(filename, 'saving')
	with open(exportDir+filename,'wb') as f:
		pickle.dump(myList, f)
	printOut(filename, mode='Save to pickle')

def readPickle(filename):
	printProgress(filename)
	with open('exported/'+filename,'rb') as f:
		data = pickle.load(f)
		printOut(filename)
		return data

def saveListToCsv(filename, fields, data):
	printProgress(filename, 'saving')
	with open(exportDir+filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		writer.writerow(fields)
		for item in data:
			writer.writerow(item)
	printOut(filename, mode='Save to csv')

def saveDictToCSV(filename, fieldnames, data):
	printProgress(filename, 'saving')
	with open(exportDir+filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in data:
			writer.writerow(item)
	printOut(filename, mode='Save to csv')

def readDictFromCSV(filename):
	printProgress(filename)
	f = open(exportDir+filename,'rb')
	reader = csv.DictReader(csvfile)
	f.close()
	printOut(filename)
	return reader

def isFileExist(filepath):
	return os.path.exists(filepath)