# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:24:16 2019

@author: luken
"""
from PIL import Image
from math import sqrt
import os, numpy, random
from Cluster import Cluster

foldername = "C:\\Users\\luken\\Documents\\stackskills\\Clustering-Classification-with-ML-Python\\K-means sorting\\Images_to_sort"
seed = 123456789
k = 8

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

def save_image(image_data, path):
    """saves an image to a specfied location
    
    Args:
        image_data (numpy array): 2D collection of RGB values
        path (string): the pathname to save the image to
        
    Returns:
        None
    """
    image =  Image.fromarray(image_data)
    image.save(path, mode="RGB")

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

def classify_image(color, clusters):
    """determines the closest classifier to the passed color
    
    Args:
        color (integer): a single RGB value for a color
        clusters (list of Clusters): the different clusters the color can be assigned to
        
    Returns:
        the classification that the color belongs to
    """
    #calculate distance from each mean
    distances = {};
    for cluster in clusters:
        distance = calc_distance(color, cluster.mean)
        distances.update({cluster : distance})
    #pick smallest distance and add photo
    closest_cluster = list(distances.keys())[0]
    for key in distances:
        if distances[key] < distances[closest_cluster]:
            closest_cluster = key
    print("classification:", closest_cluster.title)
    return closest_cluster.title
    
def update_classifiers(color, classification, clusters):
    """updates the passed classification to inclide the new color assigned to it
    
    Args:
        color (integer): a single RGB value for a color
        classification (string): the classification the the color belongs to
        clusters (lsit of Clusters): the different clusters the color can be assigned to
        
    Returns:
        None
    """
    current_mean = clusters[classification].mean
    current_mean *= clusters[classification].numberOfMembers
    current_mean += color
    clusters[classification].numberOfMembers += 1
    current_mean /= clusters[classification].numberOfMembers
    clusters[classification].mean = int(current_mean)
    
def main():
    #get names of files in folder
    print("finding files...")
    filenames = os.listdir(foldername)
    valid_names = []
    for filename in filenames:
        split_name = filename.split(".")
        extension = split_name[len(split_name) - 1] 
        #assign only pictures to a folder
        if(extension == "jpg" or extension == "png"):
            valid_names.append(filename)
    filenames = valid_names
    
    #create initial clusters
    clusters = []
    print("creating initial clusters...")
    random.seed(seed)
    for i in range(k):
        index = random.randint(0, len(filenames))
        data = load_image(foldername + "\\" + filenames[index])
        mean = find_avg_color(numpy.ndarray.tolist(data))
        #create location for cluster photos
        path = foldername + "\\" + str(i)
        if not os.path.exists(path):
            os.mkdir(path)
        clusters.append(Cluster(i, int(mean), path))
        save_image(data, path + "\\" + filenames[index])
        filenames.remove(filenames[index])
       
    #classify each photo
    for filename in filenames: 
        print("classifying:", filename)
        image_data = load_image(foldername + "\\" + filename)
        color = find_avg_color(numpy.ndarray.tolist(image_data))
        classification = classify_image(int(color), clusters)
        update_classifiers(color, classification, clusters)
        save_image(image_data, clusters[classification].path + "\\" + filename)
  
if __name__== "__main__":
  main()