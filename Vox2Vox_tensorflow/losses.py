import tensorflow as tf

def diceLoss(y_true, y_pred, class_weights):
    y_true = tf.convert_to_tensor(y_true, 'float32')
    y_pred = tf.convert_to_tensor(y_pred, y_true.dtype)

    num = tf.math.reduce_sum(tf.math.multiply(class_weights, tf.math.reduce_sum(tf.math.multiply(y_true, y_pred), axis=[0,1,2,3])))
    den = tf.math.reduce_sum(tf.math.multiply(class_weights, tf.math.reduce_sum(tf.math.add(y_true, y_pred), axis=[0,1,2,3])))+1e-5

    return 1-2*num/den

def l1Loss(y_true, y_pred, mask):
    y_true = tf.convert_to_tensor(y_true, 'float32')
    y_pred = tf.convert_to_tensor(y_pred, y_true.dtype)
    # if tf.reduce_all(tf.equal(mask, False)):
    #     return tf.constant(0, dtype=tf.float32)
    # return tf.reduce_mean(tf.abs(y_true[mask] - y_pred[mask]))
    return tf.reduce_mean(tf.abs(y_true - y_pred))

def l2Loss(y_true, y_pred):
    y_true = tf.convert_to_tensor(y_true, 'float32')
    y_pred = tf.convert_to_tensor(y_pred, y_true.dtype)
    return tf.reduce_mean(tf.square(y_true - y_pred))

def discriminator_loss(disc_real_output, disc_fake_output):
    real_loss = tf.math.reduce_mean(tf.math.pow(tf.ones_like(disc_real_output) - disc_real_output, 2))
    fake_loss = tf.math.reduce_mean(tf.math.pow(tf.zeros_like(disc_fake_output) - disc_fake_output, 2))

    disc_loss = 0.5*(real_loss + fake_loss)

    return disc_loss


def generator_loss(target, gen_output, disc_fake_output, class_weights, alpha, mask):
    
    # # generalized dice loss
    # dice_loss = diceLoss(target, gen_output, class_weights)
    # L1 重建损失 (生成的图像和目标图像的像素差异)
    l1 = l1Loss(target, gen_output, mask)
    
    # disc loss
    disc_loss = tf.math.reduce_mean(tf.math.pow(tf.ones_like(disc_fake_output) - disc_fake_output, 2))
       
    # total loss
    # gen_loss = alpha*l1 + disc_loss
    gen_loss = alpha * l1

    return gen_loss, l1, disc_loss
