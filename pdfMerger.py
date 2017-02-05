import os

from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir
from os.path import isfile, join

"""
Merge all the pdf from the directory that contain this script,
on windows 10 those will be taken by alphabetical order, not tested on others platforms

required : pip install PyPDF2
"""

currentDir = '.'
filenames = [f for f in listdir(currentDir) if isfile(join(currentDir, f))]

merger = PdfFileMerger()
for filename in filenames:
	_, file_extension = os.path.splitext(filename)
	if file_extension == '.pdf':
		print "Adding %s to merged document" %filename
		merger.append(PdfFileReader(file(filename, 'rb')))
print "Merging...."
merger.write("merged_pdfs.pdf")
print "Done"
