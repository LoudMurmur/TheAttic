from os import listdir
from os.path import isfile, join

#This script will only get lines where column 19, 20, 21 and 22 contains """
SEARCHES = [(19, ""), 
			(20, ""), 
			(21, ""), 
			(22, "")]
SEPARATOR = '|'
#The output file will be created right next to this script
OUTPUT_FILE = "csv_search_result.txt"
#The input folder containig a lot of csv files (ONLY CSV FILES)
INPUT_FOLDER = r"C:\data\test_csv"

def getAllFileFrom(path):
	"""
	Get all files names from a folder
		-path : (string) path of the folder to scan be it relative or absolute
		-return : list(string) list of the files names (not a path, only their names)
	"""
	file_list_without_path = [ f for f in listdir(path) if isfile(join(path,f)) and 'desktop.ini' not in f ]
	return file_list_without_path

def store(path, text):
	"""
	store a data in text file, create file if it does not exist, append if it does
		-path : (string) path of the file to store the data
		-text : list(string) text to store as a list of strings
		
	"""
	with open(path, "a") as textFile:
		for line in text:
			textFile.write(line)

def loadFromCsv(pathCsv):
	"""
	get a list of string from a csv file
		-path : (string) path of the csv file be it relative or absolute
		-return : list(string) data of the csv, WITHOUT it's header
	"""
	with open(pathCsv) as f:
		lines = f.readlines()
	lines = lines[1:] #remove the header
	result = []
	for line in lines:
		result.append(line)
	return result

def getHeader(pathCsv):
	"""
	get the header of a csv file
		-path : (string) path of the csv file be it relative or absolute
		-return : (string) the csv file header
	"""
	with open(pathCsv) as f:
		lines = f.readlines()
	return lines[0]

def isGooDLine(line):
	"""
	return True if the line is 'good', meaning all SEARCHES couples are fulfilled
		-line : (string) a line of a csv file
		-return : (bool) True if the line is what we are looking for
	"""
	line = line.split(SEPARATOR)
	global_result = True
	for column_number, wanted_value in SEARCHES:
		if line[column_number] != wanted_value:
			global_result = False
	return global_result

csv_files = getAllFileFrom(INPUT_FOLDER)
good_lines = []
good_lines.append(getHeader(csv_files[0]))

for n, csv_file in enumerate(csv_files):
	print "traitement du fichier %s sur %s" %(n+1, len(csv_files))
	data = loadFromCsv(csv_file)
	for line in data:
		if isGooDLine(line):
			print line
			good_lines.append(line)

store(OUTPUT_FILE, good_lines)