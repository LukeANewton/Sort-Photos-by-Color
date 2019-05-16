# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:24:16 2019

@author: luken
"""
from PIL import Image
from math import sqrt
import os, numpy

foldername = "C:\\Users\\luken\\Documents\\stackskills\\Clustering-Classification-with-ML-Python\\K-means sorting\\Images_to_sort"
clusters = { "red" : 0xFF0000, "green" : 0x00FF00, "blue" : 0x0000FF, "violet" : 0xEE82EE, "yellow" : 0xFFFF00, 
            "orange" : 0xFFA500, "black" : 0x000000, "white" : 0xFFFFFF}

def load_image(filename):
    image = Image.open(filename, 'r')
    image.load()
    data = numpy.asarray(image, dtype="uint8" )
    return data

def save_image(image_data, filename, classification):
   image =  Image.fromarray(image_data)
   image.save(foldername + "\\" + classification + "\\" + filename, mode="RGB")

def find_avg_color(image_data):
    avg_R = 0
    avg_G = 0
    avg_B = 0
    for row in image_data:
        for pixel in row:
            avg_R += pixel[0]
            avg_G += pixel[1]
            avg_B += pixel[2]
    avg_R /= len(image_data)*len(image_data[0])
    avg_G /= len(image_data)*len(image_data[0])
    avg_B /= len(image_data)*len(image_data[0])
    avg_color = mergeRGB(avg_R, avg_G, avg_B)
    return avg_color

def splitRGB(color):
    R = color >> 16
    G = (color >> 8) % pow(16, 2)
    B = color % pow(16, 2)
    return R, G, B

def mergeRGB(R, G, B):
    return (int(R) << 16) |  (int(G) << 8) | int(B)

def calc_distance(color1, color2):
    R1, G1, B1 = splitRGB(color1)
    R2, G2, B2 = splitRGB(color2)
    distance = sqrt(pow(R1-R2, 2) + pow(G1-G2, 2) + pow(B1-B2, 2))
    return distance

def classify_image(color, filename):
    #calculate distance from each mean
    distances = {};
    for key in clusters:
        distance = calc_distance(color, clusters[key])
        distances.update({key : distance})
    #pick smallest distance and add photo
    smallest_key = list(distances.keys())[0]
    for key in distances:
        if distances[key] < distances[smallest_key]:
            smallest_key = key
    print("average color:", smallest_key)
    return smallest_key
    
    
def main():
     #create folders to sort photos into
    for color in clusters:
        if not os.path.exists(foldername + "\\" + color):
            os.mkdir(foldername + "\\" + color)
    #get names of files in folder
    filenames = os.listdir(foldername)
    for i in range(len(filenames)):
        split_name = filenames[i].split(".")
        extension = split_name[len(split_name) - 1] 
        #assign only pictures to a folder
        if(extension == "jpg" or extension == "png"):
            print(filenames[i])
            image_data = load_image(foldername + "\\" + filenames[i])
            color = find_avg_color(numpy.ndarray.tolist(image_data))
            classification = classify_image(color, filenames[i])
            save_image(image_data, filenames[i], classification)
  
if __name__== "__main__":
  main()