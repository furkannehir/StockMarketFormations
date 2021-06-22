import numpy
import matplotlib.pyplot as plt
import pandas
import math
import pandas as pd
from scipy.sparse import data
from tensorflow.python.keras.layers.core import Dropout
import Label
from keras.models import Sequential, Model
from keras.layers import Dense, Bidirectional, Flatten
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import Dropout, Input
from keras.optimizers import RMSprop
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from tensorflow.keras.callbacks import TensorBoard, CSVLogger, EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import time
from sklearn.metrics import mean_absolute_error
from tensorflow.python import keras
import numpy as np
import math
import seaborn as sn
import os

#TODO input_dim zımbırtıları

save_path = '../models/lstm'
gCols = ['High', 'Low', 'Close', 'Label']

def create_model(seq_size):
	model = Sequential()
	model.add(LSTM(100, input_shape=(seq_size, 4), return_sequences = True))
	model.add(LSTM(16))
	model.add(Dropout(0.2))
	model.add(Dense(4))
	model.add(Activation('linear'))
	model.compile(loss='mean_absolute_error', optimizer='adam')
	return model


def createFromCsv(split, cols, filename):
	dataframe = pd.read_csv(filename)
	i_split = int(len(dataframe) * split)
	corrMatrix = dataframe.corr()
	sn.heatmap(corrMatrix, annot=True)
	plt.savefig('LVMH_corr_matrix.png')
	plt.close()
	data_train = dataframe.get(cols).values[:i_split]
	data_test  = dataframe.get(cols).values[i_split:]
	return data_train, data_test

def createFromDataFrameObj(split, cols, dataFrameObj):
	i_split = int(len(dataFrameObj) * split)
	data_train = dataFrameObj.get(cols).values[:i_split]
	data_test  = dataFrameObj.get(cols).values[i_split:]
	return data_train, data_test

def get_train_data(dataset, step_size=1):
	step_size = 1
	data_X = []
	data_Y = []
	for i in range(len(dataset)-step_size-1):
		a = dataset[i:(i+step_size)]
		data_X.append(a)
		data_Y.append(dataset[i + step_size])
	return np.array(data_X), np.array(data_Y)

def get_model(filepath):
	model = keras.models.load_model(filepath)
	return model

def normalize_dataset(dataset):
	scaler = MinMaxScaler(feature_range=(0, 1))
	_dataset = scaler.fit_transform(dataset)
	return _dataset

def plot_results(predicted_data, true_data, cols, stock_name=''):
	imgs = []
	for i in range(len(cols)):
		plt.figure()
		plt.plot(true_data[:, i], 'r--', label = 'original dataset')
		plt.plot(predicted_data[:, i], 'k-', label = 'predicted stock price/test set')
		plt.xlabel('Time in Days')
		plt.ylabel(str(cols[i]) + ' Value')
		plt.grid(True)
		plt.legend(loc = 'upper right')
		img_file = 'results/' + stock_name + '_' + cols[i] + '.png'
		imgs.append(img_file)
		plt.savefig(img_file)
	# plt.show()
	plt.close()
	return imgs


def predict_sequence_full(model, data, window_size=3):
	#Shift the window by 1 new prediction each time, re-run predictions on new window
	print('[Model] Predicting Sequences Full...')
	curr_frame = data[0]
	predicted = []
	for i in range(len(data)):
		predicted.append(model.predict(curr_frame[np.newaxis,:,:])[0,0])
	return predicted

def mean_absolute_percentage_error(y_true, y_pred): 
	y_true, y_pred = np.array(y_true), np.array(y_pred)
	return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
	# mape = np.mean(np.abs((y_true - y_pred)/y_true))*100
	# return mape
	# return mean_absolute_error(y_true, y_pred)*100

def train(filepath, epoch, split, cols, labeled=False, saved_model=False):
	stock_name = filepath.split('/')[-1]
	stock_name = stock_name.split('.')[0]
	stock_name = stock_name.split('_')[0]
	print('train:', filepath)
	if saved_model:
		model = keras.models.load_model(save_path)
	else: 
		model = create_model(1)
	if labeled:
		train_data, test_data = createFromCsv(split, cols, filepath)
	else:
		dataFrameObj = Label.labelDataAsDataFrameObj(filepath)
		train_data, test_data = createFromDataFrameObj(split, cols, dataFrameObj)

	train_x, train_y = get_train_data(train_data)
	test_x, test_y = get_train_data(test_data)
	model.compile(loss='mean_absolute_error', optimizer='adam')
	model.fit(train_x, train_y, epochs=epoch, batch_size=1, verbose=2)
	model.save(save_path)
	predictions = model.predict(test_x)
	train_predictions = model.predict(train_x)
	trainScore = mean_absolute_percentage_error(test_x, train_predictions)
	testScore = mean_absolute_percentage_error(test_y, predictions)
	print('Test MAPE: %.2f' % (trainScore))
	print('Test MAPE: %.2f' % (testScore))
	result_imgs = plot_results(predictions, test_y, cols, stock_name=stock_name)
	return testScore, predictions, result_imgs

def test(filepath, labeled):
	stock_name = filepath.split('/')[-1]
	stock_name = stock_name.split('.')[0]
	stock_name = stock_name.split('_')[0]
	model = keras.models.load_model(save_path)
	if labeled:
		test_data, _ = createFromCsv(1, gCols, filepath)
	else:
		dataFrameObj = Label.labelDataAsDataFrameObj(filepath)
		test_data, _ = createFromDataFrameObj(1, gCols, dataFrameObj)
	test_x, test_y = get_train_data(test_data)
	predictions = model.predict(test_x)
	testScore = mean_absolute_percentage_error(test_y, predictions)
	print('Test MAPE: %.2f' % (testScore))
	result_imgs = plot_results(predictions, test_y, gCols, stock_name=stock_name)
	return testScore, predictions, result_imgs


if __name__ == '__main__':
	test('dataset_CAC40/LVMH_labeled.csv', labeled=True)