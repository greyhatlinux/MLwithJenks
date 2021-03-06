#loading all required modules

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.datasets import mnist
from keras.utils import np_utils
from keras.optimizers import RMSprop
import keras

# this loads the MNIST dataset
(x_train, y_train), (x_test, y_test)  = mnist.load_data()


image_r = x_train[0].shape[0]
image_c = x_train[1].shape[0]

# Resizing data to the right shape with keras
x_train = x_train.reshape(x_train.shape[0], image_r, image_c, 1)
x_test = x_test.reshape(x_test.shape[0], image_r, image_c, 1)

# store the shape of a single image 
input_shape = (image_r, image_c, 1)

# change our image type to float32 data type
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# Normalize our data by changing the range from (0 to 255) to (0 to 1)
x_train /= 255
x_test /= 255

# Now we one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

num_classes = y_test.shape[1]
num_pixels = x_train.shape[1] * x_train.shape[2]



# createing our model
model = Sequential()

# (Convolution, RELU, Pooling)
model.add(Conv2D(5, (3, 3),
                  
input_shape = input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (5,5), strides = (3, 3)))


# Fully connected layers (w/ RELU)
model.add(Flatten())
model.add(Dense(units=5, input_dim=28*28, activation='relu'))


# Softmax (for classification)
model.add(Dense(units=10, activation='softmax'))

       
model.compile(optimizer=RMSprop(), loss='categorical_crossentropy', 
             metrics=['accuracy'])
                 
print(model.summary())


# Providing Training Parameters
batch_size = 128


# setting epoch = 3
ep = 3

history = model.fit(x_train, y_train,
          batch_size=batch_size,
          ep=ep,
          validation_data=(x_test, y_test),
          shuffle=True)

model.save("mnist_model.h5")

# Evaluate the performance of our trained model
scores = model.evaluate(x_test, y_test, verbose=1)
accuracy_score=scores[1]
f=open("output.txt","w")
f.write(str(100*accuracy_score))
print('Test loss is :', scores[0])
print('Test accuracy is :', scores[1])