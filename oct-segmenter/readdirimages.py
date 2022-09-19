import numpy as np
import h5py
import os
import parameters
from PIL import Image, ImageOps, ImageDraw

# images numpy array should be of the shape: (number of images, image width, image height, 1)
# segs numpy array should be of the shape: (number of images, number of boundaries, image width)

# Create a hdf5 dataset
def addhdf5_dataset(npimgarray, name, filename):
    h5f = h5py.File(filename, "a")
    try:
        npimgarray = np.asarray(npimgarray)
        if npimgarray.size == 0:
            # Create empty dataset
            h5f.create_dataset(name, dtype="f")
        else:
            h5f.create_dataset(name, data=npimgarray)
        h5data = h5f[name][()]
    finally:
        h5f.close()

    return h5data


# Add channel dimension as 4th dimension to image and labels array, e.g. RGB colors
def channels_last_reshape(images, channels):
    dim = images.ndim
    if dim == 3:
        x, y, z = images.shape
        image_array = images.reshape(x, y, z, channels)
    else:
        image_array = []

    return image_array


# Add 4th dim and create hdf5 dataset
def reshape(images, description, h5filename, channels):

    dataset = np.asarray(images)
    dataset = channels_last_reshape(dataset, channels)
    h5dataset = addhdf5_dataset(dataset, description, h5filename)
    return h5dataset


# Black out areas with scanner name and legend
def black_out(im):

    draw = ImageDraw.Draw(im)
    draw.rectangle(parameters.BLACKOUT_COORDS_LEFT, fill=0)
    draw.rectangle(parameters.BLACKOUT_COORDS_RIGHT, fill=0)
    return im


# Change greyscale values to 1,2,3, ... values
def mask_categorical(dset1):

    uniques = np.unique(dset1)

    for i in range(len(uniques)):
        x = uniques[i]
        dset1 = np.where(dset1 == x, i, dset1)

    return dset1


# Check if images have the same shape and type
def iswrongshapetype(dset1, x, y):

    if x == 0 and y == 0:
        return False
    else:
        a, b = dset1.shape
        if a != x and b != y and not np.issubdtype(np.uint8, dset1.dtype):
            return True
        else:
            return False


# load all data  : replaces load_training_data() and load_validation_data()
def load_all_data():

    val_images = []
    val_segs = []
    train_images = []
    train_segs = []
    test_images = []
    test_segs = []
    test_names = []
    h5filename = "img_data.hdf5"
    x = 0
    y = 0
    if os.path.exists(h5filename):
        os.remove(h5filename)

    # Read images from a directory
    dirfiles = os.scandir(parameters.INPUT_LOCATION)
    for item in dirfiles:
        if item.is_dir():
            inputs = os.scandir(parameters.INPUT_LOCATION + item.name)
            for subitem in inputs:
                if not subitem.name.startswith("."):
                    dset1 = np.rot90(
                        np.array(
                            ImageOps.grayscale(black_out(Image.open(subitem.path)))
                        )
                    )
                    if iswrongshapetype(dset1, x, y):
                        print(
                            "Error: Image and segmentation files have different dimensions or non-integer values!"
                        )
                        continue
                    else:
                        x, y = dset1.shape
                    if item.name == "val_images":
                        val_images.append(dset1)

                    elif item.name == "val_segs":
                        dset1 = mask_categorical(dset1)
                        val_segs.append(dset1)

                    elif item.name == "train_images":
                        train_images.append(dset1)

                    elif item.name == "train_segs":
                        dset1 = mask_categorical(dset1)
                        train_segs.append(dset1)

                    elif item.name == "test_images":
                        test_images.append(dset1)
                        test_names.append(os.path.splitext(subitem.name)[0])

                    elif item.name == "test_segs":
                        dset1 = mask_categorical(dset1)
                        test_segs.append(dset1)

    # Reshape and Save as hdf5 dataset
    h5val_images = reshape(val_images, "val_images", h5filename, 1)
    h5val_segs = addhdf5_dataset(np.asarray(val_segs), "val_segs", h5filename)
    h5train_images = reshape(train_images, "train_images", h5filename, 1)
    h5train_segs = addhdf5_dataset(np.asarray(train_segs), "train_segs", h5filename)
    h5test_images = reshape(test_images, "test_images", h5filename, 1)
    h5test_segs = addhdf5_dataset(np.asarray(test_segs), "test_segs", h5filename)

    return (
        h5val_images,
        h5val_segs,
        h5train_images,
        h5train_segs,
        h5test_images,
        h5test_segs,
        test_names,
    )


# When segs contains area labels, just copy over, and add 4th dim for RGB channels
def create_all_area_masks(segs):

    all_masks = channels_last_reshape(segs, 1)
    all_masks = np.array(all_masks)

    return all_masks


# test load_all_data()
# val_images, val_segs, train_images, train_segs, test_images, test_segs = load_all_data()
# train_labels=create_all_area_masks(train_segs)