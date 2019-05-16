# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:24:16 2019

@author: luken
"""
from PIL import Image
import os

foldername = "C:\\Users\\luken\\Documents\\stackskills\\Clustering-Classification-with-ML-Python\\K-means sorting\\Images_to_sort"
clusters = { "red" : 0xFF0000, "green" : 0x00FF00, "blue" : 0x0000FF, "violet" : 0xEE82EE, "yellow" : 0xFFFF00, 
            "orange" : 0xFFA500, "grey" : 0x808080}

def load_image( infilename ):
    image = Image.open(infilename, 'r')
    image.load()
    #data = np.asarray(image, dtype="int32")
    data = list(image.getdata())
    return data

def find_avg_color(image_data):
    avg_R = 0
    avg_G = 0
    avg_B = 0
    for pixel in image_data:
        avg_R += pixel[0]
        avg_G += pixel[1]
        avg_B += pixel[2]
    avg_R /= len(image_data)
    avg_G /= len(image_data)
    avg_B /= len(image_data)
    avg_color = (int(avg_R) << 16) |  (int(avg_G) << 8) | int(avg_B)
    print(hex(avg_color))
    return avg_color

def main():
    #get names of files in folder
    filenames = os.listdir(foldername)
    valid_names = []
    for i in range(len(filenames)):
        split_name = filenames[i].split(".")
        extension = split_name[len(split_name) - 1]  
        if(extension == "jpg" or extension == "png"):
            valid_names.append(filenames[i])
    filenames = valid_names
    #create folders to sort photos into
    #for color in clusters:
        #os.mkdir(foldername + "\\" + color)
    #assign each picture to a folder
    for filename in filenames:
        print(filename)
        image_data = load_image(foldername + "\\" + filename)
        color = find_avg_color(image_data)
        classify_image(color, filename)
  
  
if __name__== "__main__":
  main()