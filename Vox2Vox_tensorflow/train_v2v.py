import os
import numpy as np
import pytest
import tensorflow as tf
from models import *
from losses import *
import matplotlib.image as mpim
from sys import stdout
from v3dpy.loaders import PBD

# class weights
class_weights = np.load('class_weights.npy')

# Models
G = Generator()
D = Discriminator()

# Optimizers
generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4, beta_1=0.5)

@tf.function
def train_step(image, target, alpha):
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

        gen_output = G(image, training=True)

        disc_real_output = D([image, target], training=True)
        disc_fake_output = D([image, gen_output], training=True)
        disc_loss = discriminator_loss(disc_real_output, disc_fake_output)

        mask = tf.cast(image, dtype=tf.bool)
        gen_loss, l1_loss, disc_loss_gen = generator_loss(target, gen_output, disc_fake_output, class_weights, alpha, mask)

    generator_gradients = gen_tape.gradient(gen_loss, G.trainable_variables)
    discriminator_gradients = disc_tape.gradient(disc_loss, D.trainable_variables)
        
    return gen_loss, l1_loss, disc_loss_gen, disc_loss, generator_gradients, discriminator_gradients
        
@tf.function
def test_step(image, target, alpha):
    gen_output = G(image, training=False)

    disc_real_output = D([image, target], training=False)
    disc_fake_output = D([image, gen_output], training=False)
    disc_loss = discriminator_loss(disc_real_output, disc_fake_output)

    mask = tf.cast(image, dtype=tf.bool)
    gen_loss, l1_loss, disc_loss_gen = generator_loss(target, gen_output, disc_fake_output, class_weights, alpha, mask)
        
    return gen_loss, l1_loss, disc_loss_gen, disc_loss

def predict_step(image):
    gen_output = G.predict(image)
    for i in range(len(image)):
        gen_output[i] = gen_output[i] * 255.0
    return gen_output

def fit(train_gen, valid_gen, alpha, epochs):
    
    path = './RESULTS' 
    if os.path.exists(path)==False:
        os.mkdir(path)

    if os.path.exists(os.path.join(path, 'Generator.h5')):
        G.load_weights(os.path.join(path, 'Generator.h5'))
        print('load pre Generator')
    if os.path.exists(os.path.join(path, 'Discriminator.h5')):
        D.load_weights(os.path.join(path, 'Discriminator.h5'))
        print('load pre Discriminator')
        
    Nt = len(train_gen)
    history = {'train': [], 'valid': []}
    prev_loss = np.inf
    
    epoch_v2v_loss = tf.keras.metrics.Mean()
    epoch_l1_loss = tf.keras.metrics.Mean()
    epoch_disc_gen_loss = tf.keras.metrics.Mean()
    epoch_disc_loss = tf.keras.metrics.Mean()
    epoch_v2v_loss_val = tf.keras.metrics.Mean()
    epoch_l1_loss_val = tf.keras.metrics.Mean()
    epoch_disc_gen_loss_val = tf.keras.metrics.Mean()
    epoch_disc_loss_val = tf.keras.metrics.Mean()
    
    for e in range(epochs):
        print('Epoch {}/{}'.format(e+1,epochs))
        b = 0
        for Xb, yb in train_gen:
            b += 1
            vals = train_step(Xb, yb, alpha)
            generator_gradients = vals[4]
            discriminator_gradients = vals[5]
            generator_optimizer.apply_gradients(zip(generator_gradients, G.trainable_variables))

            if b % 5 == 0:
                discriminator_optimizer.apply_gradients(zip(discriminator_gradients, D.trainable_variables))

            epoch_v2v_loss.update_state(vals[0])
            epoch_l1_loss.update_state(vals[1])
            epoch_disc_gen_loss.update_state(vals[2])
            epoch_disc_loss.update_state(vals[3])
            
            stdout.write('\nBatch: {}/{} - loss: {:.4f} - l1_loss: {:.4f} - disc_gen_loss: {:.4f} - disc_loss: {:.4f}'
                         .format(b, Nt, epoch_v2v_loss.result(), epoch_l1_loss.result(), epoch_disc_gen_loss.result(), epoch_disc_loss.result()))
            stdout.flush()
        history['train'].append([epoch_v2v_loss.result(), epoch_l1_loss.result(), epoch_disc_gen_loss.result(), epoch_disc_loss.result()])

        y_pred = G.predict(Xb)
        y_true = yb
        idxs = np.random.randint(len(Xb), size=1)

        for i in range(len(idxs)):
            pred_fname = (path + '/pred_train_{}@epoch_{:03d}.v3dpbd').format(i+1, e+1)
            true_fname = (path + '/true_train_{}@epoch_{:03d}.v3dpbd').format(i+1, e+1)
            y_pred[idxs[i]] = y_pred[idxs[i]] * 255.0
            y_true[idxs[i]] = y_true[idxs[i]] * 255.0
            pbd = PBD()
            pbd.save(pred_fname, np.transpose(y_pred[idxs[i]], (3, 2, 1, 0)).astype(np.uint8))
            pbd.save(true_fname, np.transpose(y_true[idxs[i]], (3, 2, 1, 0)).astype(np.uint8))

        for Xb, yb in valid_gen:
            losses_val = test_step(Xb, yb, alpha)
            epoch_v2v_loss_val.update_state(losses_val[0])
            epoch_l1_loss_val.update_state(losses_val[1])
            epoch_disc_gen_loss_val.update_state(losses_val[2])
            epoch_disc_loss_val.update_state(losses_val[3])
            
        stdout.write('\n               loss_val: {:.4f} - l1_loss_val: {:.4f} - disc_gen_loss_val: {:.4f} - disc_loss_val: {:.4f}'
                     .format(epoch_v2v_loss_val.result(), epoch_l1_loss_val.result(), epoch_disc_gen_loss_val.result(), epoch_disc_loss_val.result()))
        stdout.flush()
        history['valid'].append([epoch_v2v_loss_val.result(), epoch_l1_loss_val.result(), epoch_disc_gen_loss_val.result(), epoch_disc_loss_val.result()])
        
        # save pred image at epoch e 
        # y_pred = G.predict(Xb)
        # y_true = np.argmax(yb, axis=-1)
        # y_pred = np.argmax(y_pred, axis=-1)
        y_pred = G.predict(Xb)
        y_true = yb

        # canvas = np.zeros((128, 128*3))
        idxs = np.random.randint(len(Xb), size=1)
        
        # x = Xb[idx,:,:,64,2]
        # canvas[0:128, 0:128] = (x - np.min(x))/(np.max(x)-np.min(x)+1e-6)
        # canvas[0:128, 128:2*128] = y_true[idx,:,:,64]/3
        # canvas[0:128, 2*128:3*128] = y_pred[idx,:,:,64]/3

        for i in range(len(idxs)):
            pred_fname = (path + '/pred_val_{}@epoch_{:03d}.v3dpbd').format(i+1, e+1)
            true_fname = (path + '/true_val_{}@epoch_{:03d}.v3dpbd').format(i+1, e+1)
            y_pred[idxs[i]] = y_pred[idxs[i]] * 255.0
            y_true[idxs[i]] = y_true[idxs[i]] * 255.0
            pbd = PBD()
            pbd.save(pred_fname, np.transpose(y_pred[idxs[i]], (3, 2, 1, 0)).astype(np.uint8))
            pbd.save(true_fname, np.transpose(y_true[idxs[i]], (3, 2, 1, 0)).astype(np.uint8))

        # mpim.imsave(fname, canvas, cmap='gray')
        
        # save models
        print(' ')
        if epoch_v2v_loss_val.result() < prev_loss:    
            G.save_weights(path + '/Generator.h5') 
            D.save_weights(path + '/Discriminator.h5')
            print("Validation loss decresaed from {:.4f} to {:.4f}. Models' weights are now saved.".format(prev_loss, epoch_v2v_loss_val.result()))
            prev_loss = epoch_v2v_loss_val.result()
        else:
            print("Validation loss did not decrese from {:.4f}.".format(prev_loss))
        print(' ')
        
        # resets losses states
        epoch_v2v_loss.reset_states()
        epoch_l1_loss.reset_states()
        epoch_disc_gen_loss.reset_states()
        epoch_disc_loss.reset_states()
        epoch_v2v_loss_val.reset_states()
        epoch_l1_loss_val.reset_states()
        epoch_disc_gen_loss_val.reset_states()
        epoch_disc_loss_val.reset_states()
        
        del Xb, yb, y_pred, y_true, idxs
        
    return history

def predict(predict_gen):
    path = './RESULTS'
    if os.path.exists(path) == False:
        os.mkdir(path)

    if os.path.join(path, 'Generator.h5'):
        G.load_weights(os.path.join(path, 'Generator.h5'))
        print('load pre Generator')
    if os.path.join(path, 'Discriminator.h5'):
        D.load_weights(os.path.join(path, 'Discriminator.h5'))
        print('load pre Discriminator')

    pbd = PBD()
    for Xb, path_list in predict_gen:
        output = predict_step(Xb)
        for i in range(len(output)):
            dirpath = os.path.dirname(path_list[i])
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            pbd.save(path_list[i], np.transpose(output[i], (3, 2, 1, 0)).astype(np.uint8))