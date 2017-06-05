import numpy as np
import os
import png
import nibabel as nib
from sklearn import feature_extraction
from PIL import Image

num_patches =50
t1_in_dir = './brain/T1'
t1_out_dir = './brain/T1_patches'
t2_in_dir = './brain/T2_FLAIR'
t2_out_dir = './brain/T2_FLAIR_patches'
patches3d_in_dir = './brain/reg'
patches3d_out_dir = './brain/patches3d'
midslice_3d_dir = './brain/slices'
t1_scans =  os.listdir(t1_in_dir)
t2_scans =  os.listdir(t2_in_dir)
scans_3d = os.listdir(patches3d_in_dir)

def patches_2d(scan_set):
    if (scan_set==t1_scans):
        in_dir = t1_in_dir
        out_dir = t1_out_dir
    else:
        in_dir = t2_in_dir
        out_dir = t2_out_dir
    for inst in scan_set:
        if inst.endswith('.png'):
            full_name = os.path.join(in_dir, inst)
            scan = Image.open(full_name)
            #scan.split()
            data = np.array(scan)
            patch = feature_extraction.image.extract_patches_2d(data, (64,64),num_patches)
            inst = os.path.splitext(inst)[0]
            for i in range(num_patches):
                patch_name = os.path.join(out_dir, inst+'_{}'.format(i)+'.png')
                f = open(patch_name, 'wb')
                w = png.Writer(64,64, greyscale=True)
                scaled = scale_img(patch[i])
                w.write(f, scaled)
                f.close()
    return patch

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
    return image_2d_scaled

def extract_midslice(img_name, in_direc, out_direc):
    full_name = os.path.join(in_direc, img_name)
    slices = nib.load(full_name)
    data = slices.get_data()
    midpoint = int(np.floor(data.shape[2]/2))
    midslice=data[:,:,midpoint]
    midslice_name = os.path.join(out_direc, img_name+'.png')
    f = open(midslice_name, 'wb')
    w = png.Writer(np.shape(midslice)[1], np.shape(midslice)[0], greyscale=True)
    scaled = scale_img(midslice)
    w.write(f, scaled) #optional: save midslices in folder
    f.close()
    return midslice, scaled

def patches_3d(scan_set):
    in_dir = patches3d_in_dir
    out_dir = patches3d_out_dir
    for inst in scan_set:
        if inst.endswith('.nii'):
            midslice, _ = extract_midslice(inst,in_dir,midslice_3d_dir)
            patch = feature_extraction.image.extract_patches_2d(midslice, (64,64), num_patches)
            for i in range(num_patches):
                patch_name = os.path.join(out_dir, inst+'_{}'.format(i)+'.png')
                f = open(patch_name, 'wb')
                w = png.Writer(64,64, greyscale=True)
                scaled = scale_img(patch[i])
                w.write(f, scaled)
                f.close()
    return patch

patches_2d(t1_scans)
