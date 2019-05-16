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
    """loads an image as a 2D array of RGB tuples
    
    Args:
        filename (string): the pathname of the image to load
        
    Returns:
        A 2D numpy array where each element is a tuple of RGB values
    """
    image = Image.open(filename, 'r')
    image.load()
    data = numpy.asarray(image, dtype="uint8" )
    return data

def save_image(image_data, filename, classification):
    """saves an image to a specfied location
    
    Args:
        image_data (numpy array): 2D collection of RGB values
        filename (string): the name of the file to save
        classification (string): the name of the sub-folder to place the image,
                                specifying its classification
        
    Returns:
        None
    """
   image =  Image.fromarray(image_data)
   image.save(foldername + "\\" + classification + "\\" + filename, mode="RGB")

def find_avg_color(image_data):
    """determines the average RGB values of a 2D collection of RGB values
    
    Args:
        image_data (numpy array): 2D collection of RGB values
        
    Returns:
        the average RGB value as a single hex value
    """
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
    """splits a single RGB hex value into 3 values for red, green, and blue
    
    Args:
        color (integer): RGB value as a single number
        
    Returns:
        3 integers for the red, green, and blue values of the input, in that order
    """
    R = color >> 16
    G = (color >> 8) % pow(16, 2)
    B = color % pow(16, 2)
    return R, G, B

def mergeRGB(R, G, B):
    """combines 3 values for red, green, and blue into a single RGB hex integer
    
    Args:
        R (integer): red value
        G (integer): green value
        B (integer): blue value
        
    Returns:
        a single RGB integer value
    """
    return (int(R) << 16) |  (int(G) << 8) | int(B)

def calc_distance(color1, color2):
    """calculates euclidean distance between 2 color values
    
    Args:
        color1 (integer): single RGB value for a color
        color2 (integer): single RGB value for a second color
        
    Returns:
        the distance between those two colors
    """
    R1, G1, B1 = splitRGB(color1)
    R2, G2, B2 = splitRGB(color2)
    distance = sqrt(pow(R1-R2, 2) + pow(G1-G2, 2) + pow(B1-B2, 2))
    return distance

def classify_image(color):
    """determines the closest classifier to the passed color
    
    Args:
        color (integer): a single RGB value for a color
        
    Returns:
        the classification that the color belongs to
    """
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
            classification = classify_image(color)
            save_image(image_data, filenames[i], classification)
  
if __name__== "__main__":
  main()