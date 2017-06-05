# Program to randomly select sample patches and prompt user to classify as
# anomolous or normal. Saves results in txt file (dictionary format).

import numpy as np
import os
import json
import png
import matplotlib.pyplot as plt
from PIL import Image

data_dir = './brain/t1_patches'
sample_dir = './brain/sample_patches'
class_list =  open("sample_class.txt",'r+')

def scale_img(slic):
    max_val=0
    for row in slic:
        for col in row:
            if col > max_val:
                max_val=col
    image_2d_scaled = []
    for row in slic:
        row_scaled = []
        for col in row:
            col_scaled = int((float(col)/float(max_val+1e-10))*255.0)
            row_scaled.append(col_scaled)
        image_2d_scaled.append(row_scaled)
    return image_2d_scaled;

def sample_patches():
    '''create random subset of samples'''
    patches = os.listdir(data_dir)
    rand_list = np.random.random_integers(0,len(patches),(300,1))
    rand_patches=[]
    for i in range(len(rand_list)):
        k = int(rand_list[i])
        rand_patches.append(str(patches[k]))
    for patch in rand_patches:
        if (patch.endswith('.png')): #avoid txt files etc
            full_name = os.path.join(data_dir,patch)
            img = np.array(Image.open(full_name))
            patch_name = os.path.join(sample_dir, patch)
            f = open(patch_name, 'wb')
            w = png.Writer(64,64, greyscale=True)
            w.write(f, img)
            f.close()
    return 0;

def create_label():
    sample_patches = os.listdir(sample_dir)
    sample_list = {}
    print("Classify each image as: \n 0 = NO anomaly \n 1 = anomaly present")
    i=0
    for patch in sample_patches:
        if (patch.endswith('.png')):
            i+=1
            full_name = os.path.join(data_dir,patch)
            img = np.array(Image.open(full_name))
            print ("Showing image {}".format(i))
            plt.imshow(img,cmap='gray')
            plt.show()
            val = raw_input("Select either 0= NO anomaly or 1=anomaly present: \n")
            if (int(val)==0 or int(val)==1):
                sample_list[patch] = val
            if(i%10==0):#every time 10 more classifications made, save dictionary
                json.dump(sample_list, class_list)
    return 0;

def query_label():
    sample_patches = os.listdir(sample_dir)
    classes = json.load(class_list)
    for patch in sample_patches:
        label = int(classes[patch])
        print label

#create_label()
#query_label()
