#!/usr/bin/env python
# --*-- encoding: iso-8859-1 --*--

import hashlib
from os import listdir
from os.path import isfile, join

def computeMd5(src_file):
    """Compute the md5 of a file, file is cut in 4MB data packets to avoid
    memory saturation"""
    h = hashlib.md5()
    with open(src_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return str(h.hexdigest())

def get_all_files_from(my_path):
    """return all filename in a folder, without their path"""
    file_list_without_path = [ f for f in listdir(my_path) if isfile(join(my_path,f)) and 'desktop.ini' not in f ]
    return file_list_without_path

for file in get_all_files_from("."):
    print "MD5 %s fot %s" %(computeMd5(file), file)
