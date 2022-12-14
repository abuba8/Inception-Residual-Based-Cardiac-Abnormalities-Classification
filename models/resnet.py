from keras.layers import Input, Dense, Dropout, Activation, BatchNormalization, Add
from keras.layers import Conv1D, GlobalAveragePooling1D
from keras.models import Model
import tensorflow as tf
from keras.layers import LeakyReLU

def identity_block(X, f, filters):
    F1, F2, F3 = filters
    
    X_shortcut = X
    
    X = Conv1D(filters = F1, kernel_size = 1, activation='relu', strides = 1, padding = 'valid')(X)
    X = BatchNormalization()(X)
    
    X = Conv1D(filters = F2, kernel_size = f, activation='relu', strides = 1, padding = 'same')(X)
    X = BatchNormalization()(X)

    X = Conv1D(filters = F3, kernel_size = 1, activation='relu', strides = 1, padding = 'valid')(X)
    X = BatchNormalization()(X)

    X = Add()([X,X_shortcut])
    X = Activation('relu')(X)
    
    return X

def convolutional_block(X, f, filters, s = 2):
    F1, F2, F3 = filters
    
    X_shortcut = X

    X = Conv1D(F1, 1, activation='relu', strides = s)(X)
    X = BatchNormalization()(X)
    
    X = Conv1D(F2, f, activation='relu', strides = 1,padding = 'same')(X)
    X = BatchNormalization()(X)

    X = Conv1D(F3, 1, strides = 1)(X)
    X = BatchNormalization()(X)

    X_shortcut = Conv1D(F3, 1, strides = s)(X_shortcut)
    X_shortcut = BatchNormalization()(X_shortcut)
    
    X = Add()([X,X_shortcut])
    X = Activation('relu')(X)
    
    return X

def ResNet50(input_shape):
    
    X_input = Input(input_shape)

    # X = ZeroPadding1D(3)(X_input)
    
    X = Conv1D(64, 7, strides = 2)(X_input)
    X = BatchNormalization()(X)
    # tf.keras.layers.LeakyReLU(alpha=0.01)
    # X = Activation('relu')(X)
    X = LeakyReLU(alpha=0.01)(X)
    # X = MaxPool1D(pool_size=2, strides=2, padding='same')(X)

    X = convolutional_block(X, f = 3, filters = [64, 64, 256], s = 1)
    # X = identity_block(X, 3, [64, 64, 256])
    # X = identity_block(X, 3, [64, 64, 256])

    X = convolutional_block(X, f = 3, filters = [128,128,512], s = 2)
    # X = identity_block(X, 3, [128,128,512])
    # X = identity_block(X, 3, [128,128,512])
    # X = identity_block(X, 3, [128,128,512])

    X = convolutional_block(X, f = 3, filters = [256, 256, 1024], s = 2)
    # X = identity_block(X, 3, [256, 256, 1024])
    # X = identity_block(X, 3, [256, 256, 1024])
    # X = identity_block(X, 3, [256, 256, 1024])
    # X = identity_block(X, 3, [256, 256, 1024])
    # X = identity_block(X, 3, [256, 256, 1024])

    X = convolutional_block(X, f = 3, filters = [512, 512, 2048], s = 2)
    # X = identity_block(X, 3, [512, 512, 2048])
    # X = identity_block(X, 3, [512, 512, 2048])

    X = convolutional_block(X, f = 3, filters = [512, 512, 2048], s = 2)
    X = convolutional_block(X, f = 3, filters = [512, 512, 2048], s = 2)
    X = Dropout(0.2)


    # X = GlobalMaxPool1D(pool_size=2, strides=2, padding='same')(X)
    
    X = GlobalAveragePooling1D()(X)
    X = Dense(27,activation='sigmoid')(X)
    
    model = Model(inputs = X_input, outputs = X, name='ResNet50')

    return model



