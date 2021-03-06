import tensorflow as tf
"""这个程序定义了前向传播的过程以及神经网络过程中的参数"""

# 定义神经网络的相关参数
INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500

# 通过tf.get_variable 函数来获取变量. 在训练神经网络时会创建这些变量.
# 在测试时会通过保存的模型加载这些变量的取值, 而且更加方便的是, 因为可以
# 在变量加载时将滑动平均变量重命名, 所以可以直接通过同样的名字在训练时使用变量自身,
# 而在测试时使用变量的滑动平均值, 在这个函数中也会将变量的正则化损失加入损失合集
def get_weight_variable(shape, regularizer):
    weights = tf.get_variable(
        "weights", shape,
        initializer=tf.truncated_normal_initializer(stddev=0.1)
    )

    # 当给出了正则化生成的函数时, 将当前变量的正则化损失加入名为losses的集合.
    # 在这里使用了add_to_collection 函数将一个张量加入一个集合, 而这个集合的名称为losses,
    # 这是自定义集合, 不在tensorflow自动管理的集合列表中
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))
    return weights

# 定义神经网络的前线传播过程
def inference(input_tensor, regularizer):
    # 声明第一层神经网络变量并完成前向传播的过程
    with tf.variable_scope("layer1"):
        # 这里通过tf.get_variable 或 tf.Variable 没有本质区别, 因为在训练或是测试
        # 中没有在同一个程序中多次调用这个函数, 如果在一个函数中多次调用, 在第一次调用
        # 之后需要将reuse参数设置为True
        weights = get_weight_variable(
            [INPUT_NODE, LAYER1_NODE], regularizer
        )
        biases = tf.get_variable(
            "biases", [LAYER1_NODE],
            initializer=tf.constant_initializer(0.0)
        )
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)

        # 类似的生命第二层神经网络的变量并完成前向传播过程
        with tf.variable_scope('layer'):
            weights = get_weight_variable(
                [LAYER1_NODE, OUTPUT_NODE], regularizer
            )
            biases = tf.get_variable(
                "biases", [OUTPUT_NODE],
                initializer = tf.constant_initializer(0.0)
            )
            layer2 = tf.matmul(layer1, weights) + biases

        #　返回最后的前向传播结果
        return layer2




















