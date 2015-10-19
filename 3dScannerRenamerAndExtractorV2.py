import os
from os import listdir
from os.path import isfile, join
import shutil

def get_all_files_from(my_path):
    """return all filename in a folder, without their path"""
    file_list_without_path = [ f for f in listdir(my_path) if isfile(join(my_path,f)) and 'desktop.ini' not in f ]
    return file_list_without_path
    
def get_all_folders_from(my_path):
    """ return all folder in a folder without their path"""
    folder_list_without_path = [ f for f in listdir(my_path) if not isfile(join(my_path,f)) ]
    return folder_list_without_path

def move_safely_to(destination, file_name_with_path):
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:
        shutil.move(file_name_with_path, destination)
    except shutil.Error:
        pass

CAMERA_NUMBER = 21 #there is 21 cameras, from 1 to 21
OUTPUT_FOLDER = "scanData"

print os.path.abspath(os.getcwd())

for counter in range(1, 22):
    print "Processing folder %d" % (counter)
    folder_to_process = join(os.path.abspath(os.getcwd()), str(counter).zfill(2))
    output_path = join(os.path.abspath(os.getcwd()), OUTPUT_FOLDER)
    file_list = get_all_files_from(folder_to_process)
    view_counter = 0
    for file_name in file_list:
        print "deplacepent de " + join(folder_to_process, file_name)
        file_ouput_path = join(output_path, str(view_counter).zfill(4))
        move_safely_to(file_ouput_path, join(folder_to_process, file_name))
        output_name = "Scan_"+ str(view_counter).zfill(4) +"_camera_"+ str(counter).zfill(2)+ ".JPG"
        print "renommage de "+join(output_path, file_name)+ " en " + output_name
        os.rename(join(file_ouput_path, file_name), join(file_ouput_path, output_name))
        view_counter = view_counter+1
    print " "