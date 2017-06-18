from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join

from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing
from sklearn.datasets import load_boston

from scipy.stats import linregress
import tensorflow as tf

from keras.layers.core import Dense
from keras.optimizers import SGD
from keras.models import Sequential

def show_result(bias, weights, mse):
	print('Bias  = %s , Coefficients = %s , MSE = %s' % (bias, weights, mse))
	
def show_graph(X, Y, predict, title, xlabel, ylabel):
	plt.scatter(X, Y, color='b', label='data')
	plt.plot(X, predict, color='r', label='predict')
	plt.title(title)
	plt.xlabel('Years')	
	plt.ylabel('Population')
	plt.show()	

def add_one(data_X):
	ones =np.ones((len(data_X),1))	
	# Add 1 vector to frist column
	X = np.append(ones, data_X, axis=1)	 
	# Wrap matrix to X, then you can use operators of the matrix
	X = np.matrix(X)
	return X	
	
# example 1: solve eqation
def predict_example1(data_X, Y):
	X = add_one(data_X)	
	C = (X.T * X).I * (X.T * Y) 			# Answer of coefficients 	
	#Finish training
	
	#Show model
	predict = X * C							# prediction
	mse = mean_squared_error(Y, predict )
	b, w = C[0], C[1:]
	show_result(b, w, mse)	
	return predict

# example 2: use sklearn library
def predict_example2(X, Y):
	regr = linear_model.LinearRegression()
	regr.fit(X, Y)
	#Finish training
	
	#Show model
	predict = regr.predict(X)				# prediction
	mse = mean_squared_error(Y, predict)
	show_result(regr.intercept_, regr.coef_, mse)
	return predict
	
	
# example 3: use tensorflow library
def predict_example3(X, Y):
	# Try to find values for weights and bias that compute FX = W * X + B	
	num_feature = X.shape[1]
	W = tf.Variable(tf.truncated_normal((num_feature, 1)))
	B = tf.Variable(tf.truncated_normal((1, 1)))	
	X = X.astype(np.float32)	
	FX =tf.matmul(X, W) + B	
	
	# Minimize the mean squared errors.
	loss = tf.reduce_mean(tf.square(FX - Y))
	
	# Use gradient descent algorithm for optimizing
	learningRate = 0.01
	optimizer = tf.train.GradientDescentOptimizer(learningRate)	
	train = optimizer.minimize(loss)

	# Before starting, initialize the variables. We will 'run' this first.
	init = tf.global_variables_initializer()

	# Launch the graph.
	sess = tf.Session()
	sess.run(init)

	# Try fit the line
	b, w, mse, predict = (None, None, None, None)
	for step in range(3000):
		_, b, w, mse, predict = sess.run([train, B, W, loss, FX])				
		
	#Show model
	show_result(b, w ,mse )
	return predict

# example 4: use Keras library
def predict_example4(X, Y):
	model = Sequential()
	num_feature = X.shape[1]	
	model.add(Dense(1, input_dim=num_feature, kernel_initializer='normal'))
	model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.01))
	weights = model.layers[0].get_weights()	
	model.fit(X, Y, epochs=3000, verbose=0)
	
	weights = model.layers[0].get_weights()
	w = weights[0]
	b = weights[1][0]
	
	#Show model
	predict = model.predict(X)				# prediction
	mse = mean_squared_error(Y, predict)
	show_result(b, w, mse)
	return predict

# For one input	
# example 6: use numpy module (polyfit)
def predict_example6(X, Y):
	X = X.reshape(-1)
	Y = Y.reshape(-1)
	w1, w0 = np.polyfit(X, Y, 1)
	#Finish training
	
	#Show model
	# use  broadcasting rules in numpy to add matrix
	predict = w1*X + [w0]					# prediction
	mse = mean_squared_error(Y, predict)
	show_result(w0, w1, mse)

# example 7 : use scipy module(linregress)
def predict_example7(X, Y):
	X = X.reshape(1,-1)
	Y = Y.reshape(1,-1)
	slope, intercept, r, p, stderr = linregress(X, Y)		
	#Show model
	predict = intercept + slope*X				# prediction	
	mse = mean_squared_error(Y, predict)
	show_result(intercept, slope, mse)
	
def prepare_dataset(csv_dataset,x_column_name, y_column_name, base_dir  = "" ):
	# read csv file with pandas module	
	df = pd.read_csv(join(base_dir, csv_dataset))
	
	print("First of 5 row in Dataset")
	print(df.head())	
	print("\nTail of 5 row in Dataset")
	print(df.tail())
	
	train_X = df[x_column_name].values.reshape(-1,1)		# X (Input) training set
	train_Y = df[y_column_name].values.reshape(-1,1)		# Y (Output) training set	
	return train_X, train_Y

######################	
#### for test only ####
def test_one_input(X, train_Y ,title, xlabel, ylabel):	
	# Preprocessing data
	scaler_X = preprocessing.StandardScaler().fit(X)
	scaler_Y = preprocessing.StandardScaler().fit(train_Y)
	train_X = scaler_X.transform(X)
	train_Y = scaler_Y.transform(train_Y)	
	#print(X__[0:5])
	#print(train_Y[0:5])
	
	assert train_X.shape == train_Y.shape
		
	print("\n+++++ Example 1++++")
	predict = predict_example1(train_X, train_Y)
	show_graph(X, 
			scaler_Y.inverse_transform(train_Y), 
			scaler_Y.inverse_transform(predict) 
			,title, xlabel, ylabel) 	

	print("\n+++++ Example 2++++")	
	predict = predict_example2(train_X, train_Y)
		
	print("\n+++++ Example 3++++")
	predict = predict_example3(train_X, train_Y)
	
	print("\n+++++ Example 4++++")
	predict = predict_example4(train_X, train_Y)		
	
	print("\n+++++ Example 6++++")
	predict = predict_example6(train_X, train_Y)		
	
	print("\n+++++ Example 7++++")
	predict = predict_example7(train_X, train_Y)		
	
def test_polynomial(X, train_Y ,title, xlabel, ylabel):	
	# Preprocessing data
	scaler_X = preprocessing.StandardScaler().fit(X)
	scaler_Y = preprocessing.StandardScaler().fit(train_Y)
	X__ = scaler_X.transform(X)
	train_Y = scaler_Y.transform(train_Y)	
	#print(X__[0:5])
	#print(train_Y[0:5])
	
	# Generate polynomial features (2 degree).
	degree = 2 # You can change to degree 3, 4, 5 ant other at here
	poly = PolynomialFeatures(degree)	
	# output for degree 2 = [1, x, x^2]
	# output for degree 3 = [1, x, x^2, x^3]
	train_X = poly.fit_transform(X__)
	#print(train_X[0:5])
	
	# remove 1 value from array (index 0)
	train_X = np.delete(train_X, [0], 1)	
	#print(train_X[0:5])
	
	assert train_X.shape == (len(train_X), degree)  # (xxx, degree)
	assert train_Y.shape == (len(train_Y), 1) 		# (xxx, 1)
		
	print("\n+++++ Example 1++++")
	predict = predict_example1(train_X, train_Y)
	show_graph(X, 
			scaler_Y.inverse_transform(train_Y), 
			scaler_Y.inverse_transform(predict) 
			,title, xlabel, ylabel) 	

	print("\n+++++ Example 2++++")	
	predict = predict_example2(train_X, train_Y)
		
	print("\n+++++ Example 3++++")
	predict = predict_example3(train_X, train_Y)
	
	print("\n+++++ Example 4++++")
	predict = predict_example4(train_X, train_Y)		
	
def test_many_input(train_X, train_Y):	
	scaler_X = preprocessing.StandardScaler().fit(train_X)
	scaler_Y = preprocessing.StandardScaler().fit(train_Y)
	train_X = scaler_X.transform(train_X)
	train_Y = scaler_Y.transform(train_Y)
	
	print("\n+++++ Example 1++++")
	predict = predict_example1(train_X, train_Y)
	
	print("\n+++++ Example 2++++")	
	predict = predict_example2(train_X, train_Y)
	
	print("\n+++++ Example 3++++")	
	predict = predict_example3(train_X, train_Y)
	
	print("\n+++++ Example 4++++")	
	predict = predict_example4(train_X, train_Y)
	
if __name__ == '__main__':
	print("------- One input (one features) --------")
	print("++++++++ Example from coursera () ++++++++")
	# food_truck.csv is dataset from coursera:
	# https://www.coursera.org/learn/machine-learning teach by Andrew Ng
	X, train_Y = prepare_dataset('food_truck.csv'
									,x_column_name='population'
									,y_column_name='profit')
	test_one_input(X, train_Y, title='Food truck'
									,xlabel='Population', ylabel='Profit')
	
	X, train_Y = prepare_dataset('example_price_house_40_headcolumn.csv'
									,x_column_name='area'
									,y_column_name='price')
	test_one_input(X, train_Y, title='House price'
									,xlabel='Area', ylabel='price')
	
	print("------- One input but many features (polynomial features) --------")
	print("++++++++ Example: Thailand population history ++++++++")
	X, train_Y = prepare_dataset('Thailand_population_history.csv'
									,x_column_name='Year'
									,y_column_name='Population')
	test_polynomial(X, train_Y, title='Thailand population' 
									,xlabel='Years', ylabel='Population')
	
	print("\n+++++++++++++++++++++++++++++++++++++++++++++")	
	print("++++++++ Example: Average income per month per household (B.E 41-58) ++++++++")
	X, train_Y = prepare_dataset('average_income_per_month_per_household_41-58.csv'
									,x_column_name='Years'
									,y_column_name='Average Monthly Income Per Household')
	test_polynomial(X, train_Y, title='Thailand monthly income'
									,xlabel='Years', ylabel='Average Monthly Income Per Household')

	print("\n++++++++++++ Many input ++++++++++++")
	print("++++++++++++ Boston datasets +++++++++")
	boston = load_boston()
	train_X, train_Y = boston.data, boston.target	
	train_Y = np.reshape(train_Y, (len(train_Y),1)) # shape: len(train_Y) x 1	
	test_many_input(train_X, train_Y)
	