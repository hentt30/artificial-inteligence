from keras.layers import Input, BatchNormalization, Conv2D
from keras.layers import MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.merge import concatenate
from keras.models import Model
import os


# Uncomment this to disable your GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def make_detector_network(img_cols, img_rows):
    """
    Makes the convolutional neural network used in the object detector.

    :param img_cols: number of columns of the input image.
    :param img_rows: number of rows of the input image.
    :return: Keras' model of the neural network.
    """
    # Input layer
    input_image = Input(shape=(img_cols, img_rows, 3))

    # Layer 1
    layer = Conv2D(filters=8, kernel_size=(3, 3), strides=(1, 1), padding='same', name='conv_1', use_bias=False)(input_image)
    layer = BatchNormalization(name='norm_1')(layer)
    layer = LeakyReLU(alpha=0.1, name='leaky_relu_1')(layer)

    # Layer 2
    # para que serve o kernel_size? para que serve o padding? como eu sei a quantidade de filtros?
    layer = Conv2D(filters= 8,kernel_size=(3,3),strides=(1,1),padding='same', name ='conv_2',use_bias=False)(layer)
    layer = BatchNormalization(name = 'norm_2')(layer)
    layer = LeakyReLU(alpha = 0.1, name = 'leaky_relu_2')(layer)
    # Layer 3
    layer = Conv2D(filters= 16,kernel_size=(3,3),strides=(1,1),padding='same', name ='conv_3',use_bias=False)(layer)
    layer = BatchNormalization(name = 'norm_3')(layer)
    layer = LeakyReLU(alpha = 0.1, name = 'leaky_relu_3')(layer)    
    layer = MaxPooling2D(pool_size = (2,2),strides = (2,2), padding = 'same', name = 'max_pool_3')(layer)
    # Layer 4
    layer = Conv2D(filters= 32,kernel_size=(3,3),strides=(1,1),padding='same', name ='conv_4',use_bias=False)(layer)
    layer = BatchNormalization(name = 'norm_4')(layer)
    layer = LeakyReLU(alpha = 0.1, name = 'leaky_relu_4')(layer)    
    layer = MaxPooling2D(pool_size = (2,2),strides = (2,2), padding = 'same', name = 'max_pool_4')(layer)
    # Layer 5 
    layer = Conv2D(filters= 64,kernel_size=(3,3),strides=(1,1),padding='same', name ='conv_5',use_bias=False)(layer)
    layer = BatchNormalization(name = 'norm_5')(layer)
    layer = LeakyReLU(alpha = 0.1, name = 'leaky_relu_5')(layer)    
    layer = MaxPooling2D(pool_size = (2,2),strides = (2,2), padding = 'same', name = 'max_pool_5')(layer)
    # Layer 6
    layer = Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='same', name='conv_6', use_bias=False)(layer)
    layer = BatchNormalization(name='norm_6')(layer)
    layer = LeakyReLU(alpha=0.1, name='leaky_relu_6')(layer)
    layer = MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding='same', name='max_pool_6')(layer)

    skip_connection = layer

    # Layer 7A
    layer = Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1), padding='same', name='conv_7A', use_bias=False)(layer)
    layer = BatchNormalization(name='norm_7A')(layer)
    layer = LeakyReLU(alpha=0.1, name='leaky_relu_7A')(layer)
    # Layer 7B
    skip_connection = Conv2D(filters=128, kernel_size=(1, 1), strides=(1, 1), padding='same', name='conv_7B', use_bias=False)(skip_connection)
    skip_connection = BatchNormalization(name='norm_7B')(skip_connection)
    skip_connection = LeakyReLU(alpha=0.1, name='leaky_relu_7B')(skip_connection)
    # Layer 8
    layer = Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), padding='same', name='conv_8', use_bias=False)(layer)
    layer = BatchNormalization(name='norm_8')(layer)
    layer = LeakyReLU(alpha=0.1, name='leaky_relu_8')(layer)



    # Concatenating layers 7B and 8
    layer = concatenate([skip_connection, layer], name='concat')

    # Layer 9 (last layer)
    layer = Conv2D(filters =10, kernel_size = (1, 1), strides=(1, 1), padding='same', name='conv_9', use_bias=True)(layer)

    model = Model(inputs=input_image, outputs=layer, name='ITA_YOLO')

    return model


model = make_detector_network(120, 160)
model.summary()  # prints the network summary
