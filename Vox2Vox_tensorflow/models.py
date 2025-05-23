import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Conv3D, Conv3DTranspose, Dropout, ReLU, LeakyReLU, Concatenate, ZeroPadding3D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

import tensorflow_addons as tfa
from tensorflow_addons.layers import InstanceNormalization
from v3dpy.loaders.pbd import PBD


def Generator():
    '''
    Generator model
    '''
    def encoder_step(layer, Nf, ks, norm=True):
        x = Conv3D(Nf, kernel_size=ks, strides=2, kernel_initializer='he_normal', padding='same')(layer)
        if norm:
            x = InstanceNormalization()(x)
        x = LeakyReLU()(x)
        x = Dropout(0.2)(x)

        return x

    def bottlenek(layer, Nf, ks):
        x = Conv3D(Nf, kernel_size=ks, strides=2, kernel_initializer='he_normal', padding='same')(layer)
        x = InstanceNormalization()(x)
        x = LeakyReLU()(x)
        for i in range(4):
            y = Conv3D(Nf, kernel_size=ks, strides=1, kernel_initializer='he_normal', padding='same')(x)
            x = InstanceNormalization()(y)
            x = LeakyReLU()(x)
            x = Concatenate()([x, y])

        return x

    def decoder_step(layer, layer_to_concatenate, Nf, ks):
        x = Conv3DTranspose(Nf, kernel_size=ks, strides=2, padding='same', kernel_initializer='he_normal')(layer)
        x = InstanceNormalization()(x)
        x = LeakyReLU()(x)
        x = Concatenate()([x, layer_to_concatenate])
        x = Dropout(0.2)(x)
        return x

    layers_to_concatenate = []
    inputs = Input((256,256,128,1), name='input_image')
    Nfilter_start = 64
    depth = 4
    ks = 4
    x = inputs

    # encoder
    for d in range(depth-1):
        if d==0:
            x = encoder_step(x, Nfilter_start*np.power(2,d), ks, False)
        else:
            x = encoder_step(x, Nfilter_start*np.power(2,d), ks)
        layers_to_concatenate.append(x)

    # bottlenek
    x = bottlenek(x, Nfilter_start*np.power(2,depth-1), ks)

    # decoder
    for d in range(depth-2, -1, -1): 
        x = decoder_step(x, layers_to_concatenate.pop(), Nfilter_start*np.power(2,d), ks)

    # classifier
    # last = Conv3DTranspose(1, kernel_size=ks, strides=2, padding='same', kernel_initializer='he_normal', activation='softmax', name='output_generator')(x)
    last = Conv3DTranspose(1, kernel_size=ks, strides=2, padding='same', kernel_initializer='he_normal', activation='sigmoid', name='output_generator')(x)
   
    return Model(inputs=inputs, outputs=last, name='Generator')

def Discriminator():
    '''
    Discriminator model
    '''

    inputs = Input((256,256,128,1), name='input_image')
    targets = Input((256,256,128,1), name='target_image')
    Nfilter_start = 64
    depth = 3
    ks = 4

    def encoder_step(layer, Nf, norm=True):
        x = Conv3D(Nf, kernel_size=ks, strides=2, kernel_initializer='he_normal', padding='same')(layer)
        if norm:
            x = InstanceNormalization()(x)
        x = LeakyReLU()(x)
        x = Dropout(0.2)(x)
        
        return x

    x = Concatenate()([inputs, targets])

    for d in range(depth):
        if d==0:
            x = encoder_step(x, Nfilter_start*np.power(2,d), False)
        else:
            x = encoder_step(x, Nfilter_start*np.power(2,d))

    # 这里padding = 'valid'会减小尺寸，需要加一圈全0的padding
    # x = ZeroPadding3D()(x)
    x = Conv3D(Nfilter_start*(2**depth), ks, strides=2, padding='same', kernel_initializer='he_normal')(x)
    x = InstanceNormalization()(x)
    x = LeakyReLU()(x)
      
    # x = ZeroPadding3D()(x)
    last = Conv3D(1, ks, strides=1, padding='same', kernel_initializer='he_normal', name='output_discriminator')(x)

    return Model(inputs=[targets, inputs], outputs=last, name='Discriminator')

def ensembler():

    start = Input((128,128,128,40))
    fin = Conv3D(4, kernel_size=3, kernel_initializer='he_normal', padding='same', activation='softmax')(start)

    return Model(inputs=start, outputs=fin, name='Ensembler')

if __name__ == '__main__':
    G = Generator()
    D = Discriminator()
    G.summary()
    D.summary()
    # input_image_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\sample\input_image\02456_P025_T02_-S019_LTL_R0613_YW-20230204_YS\x_0_y_2.v3dpbd'
    # pbd = PBD()
    # input_img = pbd.load(input_image_path)
    # X = np.transpose(input_img, (3, 2, 1, 0)).astype('float32')
    # X = np.expand_dims(X, 0)
    # print(X.shape)
    # output = G.predict(X)
    # print(output)