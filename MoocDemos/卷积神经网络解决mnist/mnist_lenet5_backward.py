import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_lenet5_forward_bak
import os
import numpy as np

BATCH_SIZE = 100
LEARNING_RATE_BASE =  0.005 
LEARNING_RATE_DECAY = 0.99 
REGULARIZER = 0.0001 
STEPS = 50000 
MOVING_AVERAGE_DECAY = 0.99 
MODEL_SAVE_PATH="/home/ma/PycharmProjects/lenet5_MNIST_models"
MODEL_NAME="mnist_model" 

def backward(mnist):
    x = tf.placeholder(tf.float32, [
	BATCH_SIZE, # 每轮喂入多少张图片
	mnist_lenet5_forward_bak.IMAGE_SIZE, # 行分辨率
	mnist_lenet5_forward_bak.IMAGE_SIZE, # 列分辨率
	mnist_lenet5_forward_bak.NUM_CHANNELS]) # 输入的通道数
    y_ = tf.placeholder(tf.float32, [None, mnist_lenet5_forward_bak.OUTPUT_NODE])
    # 训练时参数给True, 使用dropout
    y = mnist_lenet5_forward_bak.forward(x, True, REGULARIZER)
    global_step = tf.Variable(0, trainable=False) 

    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cem = tf.reduce_mean(ce) 
    loss = cem + tf.add_n(tf.get_collection('losses')) 

    learning_rate = tf.train.exponential_decay( 
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATCH_SIZE, 
		LEARNING_RATE_DECAY,
        staircase=True) 
    
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    ema = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    ema_op = ema.apply(tf.trainable_variables())
    with tf.control_dependencies([train_step, ema_op]): 
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver() 

    with tf.Session() as sess: 
        init_op = tf.global_variables_initializer() 
        sess.run(init_op) 

        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH) 
        if ckpt and ckpt.model_checkpoint_path:
        	saver.restore(sess, ckpt.model_checkpoint_path) 

        for i in range(STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE) 
            # 对数据集中取出的数据进行reshape操作.
            reshaped_xs = np.reshape(xs, (
                BATCH_SIZE,
                mnist_lenet5_forward_bak.IMAGE_SIZE,
                mnist_lenet5_forward_bak.IMAGE_SIZE,
                mnist_lenet5_forward_bak.NUM_CHANNELS))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys}) 
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

def main():
    mnist = input_data.read_data_sets("/home/ma/PycharmProjects/MNIST_data", one_hot=True) 
    backward(mnist)

if __name__ == '__main__':
    main()


