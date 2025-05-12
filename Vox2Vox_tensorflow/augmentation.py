import numpy as np
from scipy.ndimage.interpolation import affine_transform
import elasticdeform
import multiprocessing as mp

from v3dpy.loaders import PBD


def patch_extraction(Xb, yb, sizePatches=128, Npatches=1):
    """
    3D patch extraction
    """
    
    batch_size, rows, columns, slices, channels = Xb.shape
    X_patches = np.empty((batch_size*Npatches, sizePatches, sizePatches, sizePatches, channels))
    y_patches = np.empty((batch_size*Npatches, sizePatches, sizePatches, sizePatches))
    i = 0
    for b in range(batch_size):
        for p in range(Npatches):
            x = np.random.randint(rows-sizePatches+1) 
            y = np.random.randint(columns-sizePatches+1)
            z = np.random.randint(slices-sizePatches+1) 

            X_patches[i] = Xb[b, x:x+sizePatches, y:y+sizePatches, z:z+sizePatches, :]
            y_patches[i] = yb[b, x:x+sizePatches, y:y+sizePatches, z:z+sizePatches]
            i += 1
                               
    return X_patches, y_patches

def flip3D(X, y):
    """
    Flip the 3D image respect one of the 3 axis chosen randomly
    """
    choice = np.random.randint(3)
    if choice == 0: # flip on x
        X_flip, y_flip = X[::-1, :, :, :], y[::-1, :, :, :]
    if choice == 1: # flip on y
        X_flip, y_flip = X[:, ::-1, :, :], y[:, ::-1, :, :]
    if choice == 2: # flip on z
        X_flip, y_flip = X[:, :, ::-1, :], y[:, :, ::-1, :]
        
    return X_flip, y_flip


def rotation3D(X, y):
    """
    Rotate a 3D image with alfa, beta and gamma degree respect the axis x, y and z respectively.
    The three angles are chosen randomly between 0-30 degrees
    """
    alpha, beta, gamma = np.pi*np.random.random_sample(3,)/12
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(alpha), -np.sin(alpha)],
                   [0, np.sin(alpha), np.cos(alpha)]])
    
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                   [0, 1, 0],
                   [-np.sin(beta), 0, np.cos(beta)]])
    
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                   [np.sin(gamma), np.cos(gamma), 0],
                   [0, 0, 1]])
    
    R = np.dot(np.dot(Rx, Ry), Rz)
    
    X_rot = np.empty_like(X)
    y_rot = np.empty_like(y)
    for channel in range(X.shape[-1]):
        # 0, 0
        X_rot[:,:,:,channel] = affine_transform(X[:,:,:,channel], R, offset=0, order=3, mode='constant')
        # 0, 3
        y_rot[:,:,:,channel] = affine_transform(y[:,:,:,channel], R, offset=0, order=3, mode='constant')
    
    return X_rot, y_rot

def brightness(X, y):
    """
    Changing the brighness of a image using power-law gamma transformation.
    Gain and gamma are chosen randomly for each image channel.
    
    Gain chosen between [0.9 - 1.1]
    Gamma chosen between [0.9 - 1.1]
    
    new_im = gain * im^gamma
    """
    
    X_new = np.zeros(X.shape)
    for c in range(X.shape[-1]):
        im = X[:,:,:,c]        
        gain, gamma = (1.2 - 0.8) * np.random.random_sample(2,) + 0.8
        im_new = np.sign(im)*gain*(np.abs(im)**gamma)
        X_new[:,:,:,c] = im_new 
    
    return X_new, y

def elastic(X, y):
    """
    Elastic deformation on a image and its target
    """
    # 0, 3
    [Xel, yel] = elasticdeform.deform_random_grid([X, y], sigma=0.8, axis=[(0, 1, 2), (0, 1, 2)], order=[3, 3], mode='constant')
    
    return Xel, yel

def random_decisions(N):
    """
    Generate N random decisions for augmentation
    N should be equal to the batch size
    """
    
    decisions = np.zeros((N, 4)) # 4 is number of aug techniques to combine (patch extraction excluded)
    for n in range(N):
        decisions[n] = np.random.randint(2, size=4)
        decisions[n][1] = 0
        decisions[n][3] = 0

    return decisions

def combine_aug(X, y, do):
    """
    Combine randomly the different augmentation techniques written above
    """
    Xnew, ynew = X, y
    
    # make sure to use at least the 25% of original images
    if np.random.random_sample()>0.75:
        return Xnew, ynew
    
    else:   
        if do[0] == 1:
            Xnew, ynew = flip3D(Xnew, ynew)

        if do[1] == 1:
            Xnew, ynew = brightness(Xnew, ynew)   

        if do[2] == 1:
            Xnew, ynew = rotation3D(Xnew, ynew)

        if do[3] == 1:
            Xnew, ynew = elastic(Xnew, ynew)
        
        return Xnew, ynew

def aug_batch(Xb, Yb):
    """
    Generate a augmented image batch 
    """
    batch_size = len(Xb)
    newXb, newYb = np.empty_like(Xb), np.empty_like(Yb)
    
    decisions = random_decisions(batch_size)            
    inputs = [(X, y, do) for X, y, do in zip(Xb, Yb, decisions)]
    pool = mp.Pool(processes=8)
    multi_result = pool.starmap(combine_aug, inputs)
    pool.close()
    
    for i in range(len(Xb)):
        newXb[i], newYb[i] = multi_result[i][0], multi_result[i][1]
        
    return newXb, newYb 


if __name__ == '__main__':
    pbd = PBD()
    input_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\input_image_has_signal_origin_val_256\00505_P005_T01-S006_MFG_R0368_LJ-20220525_YXQ\x_0_y_1.v3dpbd'
    target_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\target_image_has_signal_origin_val_256\00505_P005_T01-S006_MFG_R0368_LJ-20220525_YXQ\x_0_y_1.v3dpbd'
    target_img = pbd.load(target_path)
    input_img = pbd.load(input_path)
    save_target_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\target_image_has_signal_origin_val_256\00505_P005_T01-S006_MFG_R0368_LJ-20220525_YXQ\target_aug.v3dpbd'
    save_input_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\target_image_has_signal_origin_val_256\00505_P005_T01-S006_MFG_R0368_LJ-20220525_YXQ\input_aug.v3dpbd'
    target_img = np.transpose(target_img, (3, 2, 1, 0)).astype('float32')
    input_img = np.transpose(input_img, (3, 2, 1, 0)).astype('float32')

    input_img, target_img = rotation3D(input_img, target_img)
    input_img, target_img = elastic(input_img, target_img)

    input_img = np.transpose(input_img, (3, 2, 1, 0))
    target_img = np.transpose(target_img, (3, 2, 1, 0))
    pbd.save(save_target_path, target_img.astype('uint8'))
    pbd.save(save_input_path, input_img.astype('uint8'))