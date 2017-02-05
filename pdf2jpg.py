

"""

Required :

1/
install tools/ImageMagick-6.9.7-6-Q8-x86-dll.exe
Latest version : http://www.imagemagick.org/download/binaries/
you have to check Install development headers and libraries for C and C++
then you have to set MAGICK_HOME environment variable to the path of ImageMagick 
(e.g. C:\Program Files\ImageMagick-6.9.7-6-Q8)

2/
Install tools/gs920w32_ghostscript_32bits.exe then add this to your PATH environment variable
C:\Program Files (x86)\gs\gs9.20\bin
Latest version : http://www.ghostscript.com/download/gsdnld.html

3/
get tools/PythonMagick-0.9.10-cp27-none-win_amd64.whl
put it in a folder and open a command prompt in this folder then type :
pip install PythonMagick-0.9.10-cp27-none-win_amd64.whl

(INSTALL THE WHL FILE not the official one doing pip install PythonMagick)
use the 32 bit version if your python interpreter is 32 bits
Latest versions : http://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonmagick
"""

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from tempfile import NamedTemporaryFile
from PythonMagick import Image

REQUIRED_DPI = "300"

pdf_filename = 'merged_pdfs.pdf'
name, _ = os.path.splitext(pdf_filename)
jpg_filename = name + '.jpg'

print 'processing %s' %pdf_filename
reader = PdfFileReader(open(pdf_filename, "rb"))
for page_num in xrange(reader.getNumPages()):
    print 'processing page %s' %(page_num+1)
    writer = PdfFileWriter()
    writer.addPage(reader.getPage(page_num))
    temp = NamedTemporaryFile(prefix=str(page_num), suffix=".pdf", delete=False)
    writer.write(temp)
    temp.close()

    im = Image()
    im.density(REQUIRED_DPI)
    im.read(temp.name)
    im.write(jpg_filename + '_%s.jpg' %str(page_num+1).zfill(4))

    os.remove(temp.name)
