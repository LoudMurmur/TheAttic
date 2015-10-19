import os
from os import listdir
from os.path import isfile, join
from sets import Set
import shutil
import Image
import math

""" Ce script genere une miniature d'un scan, le placer dans le dossier qui contient les 21 photo,
cliquer dessus et il genere un dossier preview contenant prettyPrint.JPG"""

#On peut regler la taille des photo de sortie avec la variable SIZE_PERCENT
#Si on veut ignorer les image manquante mettre IGNORE_MISSING a True, dans ce cas le script se basse sur les numero a la fin de la photo
#apres l'underscore ex : dqzdzqqzd_qzdqzd_0125.JPG sera convertie en 125 et si on a dis 7 photo par ligne il sera placer a la position
#125 comme si il ne manquait aucune photo, dans ce cas, les photo manquante sont remplacer par du blanc

OUTPUT_FOLDER = "preview"
ROTATION_ANGLE = 90
SIZE_PERCENT = 0.9 #(0.1 = 10%)
IMAGE_PER_ROW = 7
IGNORE_MISSING = True
START_IMAGE_NUMBER = 1

def get_all_files_from(my_path):
    """return all filename in a folder, without their path"""
    file_list_without_path = [ f for f in listdir(my_path) if isfile(join(my_path,f)) and 'desktop.ini' not in f ]
    return file_list_without_path

def create_path_if_not_exist(path):
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])

def getJpgFiles():
    script_folder = os.path.abspath(os.getcwd())
    file_list = get_all_files_from(script_folder)
    jpgList = []
    for file in file_list:
        if os.path.splitext(file)[1].lower() == ".JPG".lower():
            jpgList.append(file)
    return jpgList

def make_number_list():
    number_list = []
    file_list = getJpgFiles()
    for file in file_list:
        number_list.append(extractPicNumber(file))
    return number_list

def missing_elements(number_list, hypothetical_number_of_pic):
    set_list = Set(number_list)
    full_set = Set(range(START_IMAGE_NUMBER, hypothetical_number_of_pic+1))
    return list(full_set - set_list)

""" extrait le chiffre en bout de fichier, doit etre sur deux caractere"""
def extractPicNumber(jpgFileName):
    print jpgFileName
    file_name = os.path.splitext(jpgFileName)[0].lower()
    return int(file_name[len(file_name)-2:len(file_name)])

def get_number_of_pic():
    number_of_pic = 0
    for jpg_file in getJpgFiles():
        pic_number = int(extractPicNumber(jpg_file))
        if(pic_number > number_of_pic):
            number_of_pic = pic_number
    return pic_number


def determine_thumbtail_size(ratio, rotation_angle):
    """ return a tuple containing (width, height)"""
    counter = 0
    width =0
    height = 0
    script_folder = os.path.abspath(os.getcwd())
    file_list = get_all_files_from(script_folder)
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == ".JPG" and counter == 0:
            counter = counter+1
            file_to_process_with_path = join(script_folder, file_name)
            im = Image.open(file_to_process_with_path)
            im = im.rotate(rotation_angle)
            image_size = im.size
            width = int(math.floor(image_size[0]*ratio))
            height = int(math.floor(image_size[1]*ratio))
            return (width, height)

def resize_to_ratio(im, ratio):
    image_size = im.size
    #print(str(image_size[0]) + "width")
    #print math.floor(image_size[0]*ratio)
    #print(str(image_size[1]) + "height")
    #print math.floor(image_size[1]*ratio)
    im_width = int(math.floor(image_size[0]*ratio))
    im_height = int(math.floor(image_size[1]*ratio))
    return im.resize((im_width, im_height), Image.ANTIALIAS)

def get_number_of_row(number_of_pic, image_per_row):
        division_entiere = int(number_of_pic)/image_per_row
        partie_modulo = 0
        if((int(number_of_pic)%image_per_row) > 0):
            partie_modulo = 1
        return division_entiere + partie_modulo

def generate_blank_pic(thumbnail_size):
    return Image.new("RGBA", (thumbnail_size[0], thumbnail_size[1]), (255, 255, 255, 0))

def expand_list_with_garbage(the_list, new_size):
    for x in range(len(the_list), new_size):
        the_list.append("99999.JPG")
    return the_list

def generate_image_list(missing_numbers, hypothetical_number_of_pic, thumbtail_size):
    image_list = []
    script_folder = os.path.abspath(os.getcwd())
    file_list = getJpgFiles()
    file_list = expand_list_with_garbage(file_list, hypothetical_number_of_pic+1)
    file_list_counter = 1
    for counter in range(START_IMAGE_NUMBER, hypothetical_number_of_pic+1):
        print "counter : " + str(counter)
        print "file_list_counter : " + str(file_list_counter)
        print "image at this position " + str(join(script_folder, file_list[counter]))
        print "pic_number : " + str(extractPicNumber(file_list[file_list_counter])) + " compare to " + str(counter)
        if (extractPicNumber(file_list[file_list_counter]) == counter):
            file_to_process_with_path = join(script_folder, file_list[file_list_counter])
            im = Image.open(file_to_process_with_path)
            im = resize_to_ratio(im, SIZE_PERCENT)
            im = im.rotate(ROTATION_ANGLE)
            image_list.append(im)
            file_list_counter = file_list_counter+1
            print str(counter) + " <<<<<<<<<<OK>>>>>>>>>>"
        else:
            print str(counter) + " <<<<<<<<<<blank>>>>>>>>>>"
            image_list.append(generate_blank_pic(thumbtail_size))
    return image_list
    

def pretty_print(ratio, rotation_angle, image_per_row, outputo):
    space_betwen_pic = 5
    borders = space_betwen_pic*2
    thumbnail_size = determine_thumbtail_size(ratio, rotation_angle)
    result_width = borders+6*space_betwen_pic+7*thumbnail_size[0]
    result_height = borders+2*space_betwen_pic+3*thumbnail_size[1]
    number_of_pic = get_number_of_pic()
    number_of_row = get_number_of_row(number_of_pic, image_per_row)
    hypothetical_number_of_pic = IMAGE_PER_ROW*number_of_row

    print ""
    print "building a pretty print of " + str(result_width) + "x" + str(result_height)
    print "image will be reduced to : "+ str(ratio*100) + "%"
    print "there will be " + str(image_per_row) + " image per row,"
    print "and a rotation of a " + str(rotation_angle) + " counter clock wise angle."
    print "number of pic : " + str(number_of_pic)
    print "number of row : " + str(number_of_row)
    print "missing elements : "
    print missing_elements(make_number_list(), hypothetical_number_of_pic)
    print ""

    image_list = generate_image_list(missing_elements(make_number_list(), hypothetical_number_of_pic) ,hypothetical_number_of_pic, thumbnail_size)
    
    result = Image.new("RGBA", (result_width, result_height), (255, 255, 255, 0))
    left_starting_point = 5
    upper_starting_point = 5
    
    counter = 0
    script_folder = os.path.abspath(os.getcwd())
    file_list = get_all_files_from(script_folder)

    for image in image_list:
        print "processing image"
        print image
        result.paste(image, (left_starting_point, upper_starting_point))
        if counter == (image_per_row-1):
            print "going to next row"
            left_starting_point = space_betwen_pic
            upper_starting_point = upper_starting_point + thumbnail_size[1] + space_betwen_pic
            counter = 0
        else:
            left_starting_point = left_starting_point+space_betwen_pic + thumbnail_size[0]
            counter = counter+1
    output_file_with_path = join(script_folder, outputo, "prettyPrint.JPG")
    create_path_if_not_exist(output_file_with_path)
    result.save(output_file_with_path, quality=100)

pretty_print(SIZE_PERCENT, ROTATION_ANGLE, IMAGE_PER_ROW, OUTPUT_FOLDER)
print " "