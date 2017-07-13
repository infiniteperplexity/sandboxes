from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np

base_model = VGG16(weights="imagenet", include_top=True)
for i, layer in enumerate(base_model.layers):
	print (i, layer.name, layer.output_shape)

model = Mode(input=base_model.input, output=base_model.get_layer("block4_pool").output)




from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K

base_model = InceptionV3(weights="imagenet", include_top=False)

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(200, activation="softmax")(x)
model = Model(input=base_model.input, output=predictions)

for layer in base_model.layers: layer.trainable = False

model.compile(optimizer="rmsprop", loss="categorical_crossentropy")

from keras.datasets import cifar10

model.fit(X_train)

from keras.preprocessing.image import ImageDataGenerator
import numpy as np
NUM_TO_AUGMENT=5
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
datagen = ImageDataGenerator()