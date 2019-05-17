# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:24:16 2019

@author: luken
"""
from PIL import Image
from math import sqrt
import os, numpy, random
from Cluster import Cluster
from ImageFeatures import ImageFeatures

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

def find_features(filename, image_data):
    """determines the features of an image based on pixel data
    
    Args:
        image_data (2D list of RGB tuples): a collection of an image's pixels
        
    Returns:
        A Features object containing the feature information of the image data
    """
    brightness = 0
    redMajority = 0
    greenMajority = 0
    blueMajority = 0
    numberPixels = len(image_data) * len(image_data[0])
    for row in image_data:
        for pixel in row:
            brightness += (pixel[0]+pixel[1]+pixel[2])/3
            if(pixel[0] > pixel[1] and pixel[0] > pixel[2]):
                redMajority += 1
            elif(pixel[1] > pixel[0] and pixel[1] > pixel[2]):
                greenMajority += 1
            elif(pixel[2] > pixel[0] and pixel[2] > pixel[1]):
                blueMajority += 1
            elif(pixel[0] == pixel[1]):
                redMajority += 1
                greenMajority += 1
            elif(pixel[1] == pixel[2]):
                blueMajority += 1
                greenMajority += 1
            elif(pixel[0] == pixel[2]):
                redMajority += 1
                blueMajority += 1
            else:
                redMajority += 1
                greenMajority += 1
                blueMajority += 1
    brightness /= numberPixels
    redMajority /= numberPixels
    greenMajority /= numberPixels
    blueMajority /= numberPixels
    return ImageFeatures(filename, brightness, redMajority, greenMajority, blueMajority)

def calc_distance(features1, features2):
    """calculates euclidean distance between 2 image features
    
    Args:
        features1 (Features): the color features of an image
        features2 (Features): the color features of an second image
        
    Returns:
        the distance between those two features
    """
    red_difference = features1.majorityRed - features2.majorityRed
    blue_difference = features1.majorityBlue - features2.majorityBlue
    green_difference = features1.majorityGreen - features2.majorityGreen
    brightness_difference = features1.brightness - features2.brightness
    distance = sqrt(pow(red_difference, 2) + pow(green_difference, 2) 
        + pow(blue_difference, 2) + pow(brightness_difference, 2))
    return distance

def classify_image(features, clusters):
    """determines the closest classifier to the passed image feature set
    
    Args:
        features (Features): the color features of an image
        clusters (list of Clusters): the different clusters the color can be assigned to
        
    Returns:
        the classification that the color belongs to
    """
    #calculate distance from each mean
    distances = {};
    for cluster in clusters:
        distance = calc_distance(features, cluster.mean)
        distances.update({cluster : distance})
    #pick smallest distance and add photo
    closest_cluster = list(distances.keys())[0]
    for key in distances:
        if distances[key] < distances[closest_cluster]:
            closest_cluster = key
    return closest_cluster.title
    
def update_classifiers(features, classification, clusters):
    """updates the passed classification to include the new image assigned to it
    
    Args:
        features (Features): the color features of an image
        classification (integer): the classification the the color belongs to
        clusters (list of Clusters): the different clusters the color can be assigned to
        
    Returns:
        None
    """
    current_mean = clusters[classification].mean
    current_mean.brightness *= clusters[classification].numberOfMembers
    current_mean.majorityRed *= clusters[classification].numberOfMembers
    current_mean.majorityGreen *= clusters[classification].numberOfMembers
    current_mean.majorityBlue *= clusters[classification].numberOfMembers
    current_mean.brightness += features.brightness
    current_mean.majorityRed += features.majorityRed
    current_mean.majorityGreen += features.majorityGreen
    current_mean.majorityBlue += features.majorityBlue
    clusters[classification].numberOfMembers += 1
    current_mean.brightness /= clusters[classification].numberOfMembers
    current_mean.majorityRed /= clusters[classification].numberOfMembers
    current_mean.majorityGreen /= clusters[classification].numberOfMembers
    current_mean.majorityBlue /= clusters[classification].numberOfMembers
    clusters[classification].mean = current_mean
    
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
    filenames = list.copy(valid_names)
    
    #get features of each image
    print("finding features...")
    images = {}
    for filename in filenames:
        print("building features for:", filename)
        data = load_image(foldername + "\\" + filename)
        features = find_features(filename, numpy.ndarray.tolist(data))
        images.update({filename : features})
    
    #create initial clusters
    clusters = []
    print("creating initial clusters...")
    random.seed(seed)
    for i in range(k):
        print("creating cluster:", i)
        index = random.randint(0, len(valid_names))
        initial_mean = images[valid_names[index]]
        #create location for cluster photos
        path = foldername + "\\" + str(i)
        if not os.path.exists(path):
            os.mkdir(path)
        clusters.append(Cluster(i, initial_mean, path))
        valid_names.remove(valid_names[index])
       
    #classify each photo
    for filename in filenames: 
        print("classifying:", filename)
        image_features = images[filename]
        classification = classify_image(image_features, clusters)
        print("classification:", classification)
        update_classifiers(features, classification, clusters)
        #move photo to appropriate cluster
        image_data = load_image(foldername + "\\" + filename)
        save_image(image_data, clusters[classification].path + "\\" + filename)
  
if __name__== "__main__":
  main()