import argparse

parser = argparse.ArgumentParser('Vox2Vox training and validation script', add_help=False)

## training parameters
parser.add_argument('-g', '--gpu', default=0, type=int, help='GPU position')
parser.add_argument('-nc', '--num_classes', default=1, type=int, help='number of classes')
parser.add_argument('-bs', '--batch_size', default=8, type=int, help='batch size')
parser.add_argument('-a', '--alpha', default=5, type=int, help='alpha weight')
parser.add_argument('-ne', '--num_epochs', default=200, type=int, help='number of epochs')

args = parser.parse_args()
gpu = args.gpu
n_classes = args.num_classes
batch_size = args.batch_size
alpha = args.alpha
n_epochs = args.num_epochs


import os
import tensorflow as tf
#os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu)

physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))
#physical_devices = tf.config.experimental.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], True)
os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)

import numpy as np
import nibabel as nib
import glob
import time
from sys import stdout
import matplotlib.pyplot as plt
import matplotlib.image as mpim
from scipy.ndimage.interpolation import affine_transform
from sklearn.model_selection import train_test_split

from utils import *
from augmentation import *
from losses import *
from models import *
from train_v2v import *

input_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\sample\input_image'
predict_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\sample\predict_image'
input_image_list = []
predict_image_list = []

for root, dirs, files in os.walk(input_image_dir_path):
    for file in files:
        if file.endswith('.v3dpbd'):
            input_image_list.append(os.path.join(root, file))
            relative_path = os.path.relpath(root, input_image_dir_path)
            predict_image_list.append(os.path.join(predict_image_dir_path, relative_path, file))

input_image_list = sorted(input_image_list)
predict_image_list = sorted(predict_image_list)

list = []
for i in range(len(input_image_list)):
    list.append([input_image_list[i], predict_image_list[i]])

predict_gen = DataGenerator(list, batch_size=batch_size, n_classes=n_classes, augmentation=False, shuffle=False, is_predict=True)
predict(predict_gen)