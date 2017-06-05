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

def create_label(existing_list):
    sample_patches = os.listdir(sample_dir)
    '''if len(existing_list)==0:
        sample_list={}
    else:
        sample_list = existing_list #avoid classifing items already in list'''
    i=0
    for patch in sample_patches:
        if (patch.endswith('.png')):
            print patch
            if (patch in existing_list):
                print('already exists')
                continue
            elif(patch not in existing_list):
                #print("Classify each image as: \n 0 = NO anomaly \n 1 = anomaly present")
                i+=1
                full_name = os.path.join(data_dir,patch)
                img = np.array(Image.open(full_name))
                print ("Showing image {}".format(i))
                plt.title(patch)
                plt.imshow(img,cmap='gray')
                plt.show()
                val = raw_input("Select either 0=NO anomaly; 1=potential anomaly; or\
                 2=anomaly present: \n")
                if (int(val)==0 or int(val)==1 or int(val)==2):
                    existing_list[patch] = val
            if(i%10==0):  #every time 10 more classifications made, save dictionary
                with open("sample_class.txt",'w') as class_list:
                    json.dump(existing_list, class_list)
    return 0;

def query_label():
    sample_patches = os.listdir(sample_dir)
    try:
        with open("sample_class.txt",'r') as class_list:
            classes = json.load(class_list)
    except:
        return {}
    '''for i in range(len(classes)):
        label = classes[sample_patches[i]]
        #print label'''
    print('len classes: ',len(classes))
    return classes

labels = query_label() #query label first to retrieve answers already submitted
create_label(labels)
