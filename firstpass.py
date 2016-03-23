"""
First pass at the Santander competition

By Ryan Gooch
March, 2016
"""

import numpy as np
import keras
import theano

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from sklearn import cross_validation, preprocessing, metrics
from keras.layers.advanced_activations import PReLU

# Get the data in, skip header row
train = np.genfromtxt('train.csv',delimiter=',',skip_header=1)

# Normalize since mostly zeroes, may have difficulty centering
train_norm = preprocessing.normalize(train)

# Split into data and target
X = train_norm[:,:-1]
y = train_norm[:,-1]

# Random state for repeatability, split into training and validation sets
rs = 19683
X_train, X_test, y_train, y_test = \
		cross_validation.train_test_split(X, y, \
			test_size=0.25, random_state=rs)

model = Sequential()
# Trying various NN configurations, see what sticks
model.add(Dense(64, input_dim=X.shape[1], init='he_normal'))#, W_regularizer=l2(0.1)))
model.add(PReLU()) # Prelu works well I have found in the past
model.add(Dropout(0.5)) # Reduce overfitting
model.add(Dense(128, init='he_normal',input_dim=64))
model.add(PReLU())
model.add(Dropout(0.5))
model.add(Dense(64, init='he_normal',input_dim=128))
model.add(PReLU())
model.add(Dropout(0.5))
model.add(Dense(2, init='he_normal',input_dim=64))
model.add(Activation('softmax')) # classification softmax, regression tanh or sigmoid

# Stochastic gradient descent to train
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)

# Use categorical cross_entropy for now for classification
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

# Fit the model. Training on small number of epochs to start with.
f = model.fit(X_train, y_train, nb_epoch=25, shuffle=True,
	batch_size=1000, validation_split=0.15,
	show_accuracy=True, verbose=1)

print("Making predictions on validation set")
# Make predictions on validation data
predictions = clf2.predict(X_test, batch_size=100, verbose=1)

# Compute and print accuracy to screen
print("Classifier Accuracy = %d"%(metrics.accuracy_score(y_test,predictions)))