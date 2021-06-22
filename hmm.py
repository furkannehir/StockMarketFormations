from Label import getStockNameList, labelDataAsDataFrameObj
from hmmlearn import hmm
import numpy as np
import lstm
from matplotlib import pyplot as plt
import os
import warnings
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pickle

PLOT_SHOW = False
PLOT_SAVE = True
PLOT_TYPE = False


#TODO ValueError: rows of transmat_ must sum to 1.0 (got [1. 1. 1. 0.])


NUM_TEST = 100
K = 50
NUM_ITERS=10000
# datadir = '../dataset'
# files = os.listdir(datadir)
# datadir += '/'
# STOCKS = getStockNameList(files, datadir)
STOCKS = [('LVMH', './dataset_CAC40/LVMH_labeled.csv')]
labels = ['Open','High','Label','Close']
likelihood_vect = np.empty([0,1])
aic_vect = np.empty([0,1])
bic_vect = np.empty([0,1])
save_path = '../models/hmm/hmm.pkl'

# Possible number of states in Markov Model
STATE_SPACE = range(2,15)

# Calculating Mean Absolute Percentage Error of predictions
def calc_mape(predicted_data, true_data):
	return np.divide(np.sum(np.divide(np.absolute(predicted_data - true_data), true_data), 0), true_data.shape[0])

def train(filepath, n_iter, split, cols, labeled=False, saved_model=False):
	stock_name = filepath.split('/')[-1]
	stock_name = stock_name.split('.')[0]
	stock_name = stock_name.split('_')[0]
	stock_file = filepath
	result_imgs = []
	if labeled:
		dataset, _ = lstm.createFromCsv(split, cols, stock_file)
	else: 
		dataFrameObj = labelDataAsDataFrameObj(filepath)
		dataset, _ = lstm.createFromDataFrameObj(split, cols, dataFrameObj)
	if len(dataset) > 50:
		predicted_stock_data = np.empty([0,dataset.shape[1]])
		likelihood_vect = np.empty([0,1])
		aic_vect = np.empty([0,1])
		bic_vect = np.empty([0,1])
		for states in STATE_SPACE:
			num_params = states**2 + states
			dirichlet_params_states = np.random.randint(1,50,states)
			#model = hmm.GaussianHMM(n_components=states, covariance_type='full', startprob_prior=dirichlet_params_states, transmat_prior=dirichlet_params_states, tol=0.0001, n_iter=n_iter, init_params='mc')
			model = hmm.GaussianHMM(n_components=states, covariance_type='diag', tol=0.0001, n_iter=n_iter)
			model.fit(dataset[NUM_TEST:,:])
			if model.monitor_.iter == n_iter:
				print('Increase number of iterations')
				sys.exit(1)
			likelihood_vect = np.vstack((likelihood_vect, model.score(dataset)))
			aic_vect = np.vstack((aic_vect, -2 * model.score(dataset) + 2 * num_params))
			bic_vect = np.vstack((bic_vect, -2 * model.score(dataset) +  num_params * np.log(dataset.shape[0])))
		
		opt_states = np.argmin(bic_vect) + 2
		print('Optimum number of states are {}'.format(opt_states))

		for idx in reversed(range(NUM_TEST)):
			train_dataset = dataset[idx + 1:,:]
			test_data = dataset[idx,:] 
			num_examples = train_dataset.shape[0]
			#model = hmm.GaussianHMM(n_components=opt_states, covariance_type='full', startprob_prior=dirichlet_params, transmat_prior=dirichlet_params, tol=0.0001, n_iter=n_iter, init_params='mc')
			if idx == NUM_TEST - 1:
				model = hmm.GaussianHMM(n_components=opt_states, covariance_type='diag', tol=0.0001, n_iter=n_iter, init_params='stmc')
			else:
				# Retune the model by using the HMM paramters from the previous iterations as the prior
				model = hmm.GaussianHMM(n_components=opt_states, covariance_type='diag', tol=0.0001, n_iter=n_iter, init_params='')
				model.transmat_ = transmat_retune_prior 
				model.startprob_ = startprob_retune_prior
				model.means_ = means_retune_prior
				model.covars_ = np.array([np.diag(i) for i in covars_retune_prior])

			model.fit(np.flipud(train_dataset))

			transmat_retune_prior = model.transmat_
			startprob_retune_prior = model.startprob_
			means_retune_prior = model.means_
			covars_retune_prior = model.covars_

			if model.monitor_.iter == n_iter:
				print('Increase number of iterations')
				sys.exit(1)

			iters = 1
			past_likelihood = []
			curr_likelihood = model.score(np.flipud(train_dataset[0:K - 1, :]))
			while iters < num_examples / K - 1:
				past_likelihood = np.append(past_likelihood, model.score(np.flipud(train_dataset[iters:iters + K - 1, :])))
				iters = iters + 1
			likelihood_diff_idx = np.argmin(np.absolute(past_likelihood - curr_likelihood))
			predicted_change = train_dataset[likelihood_diff_idx,:] - train_dataset[likelihood_diff_idx + 1,:]
			predicted_stock_data = np.vstack((predicted_stock_data, dataset[idx + 1,:] + predicted_change))
		
		
		mape = lstm.mean_absolute_percentage_error(predicted_stock_data, np.flipud(dataset[range(100),:]))

		print('mape:', mape)

		with open(save_path, "wb") as file: 
			pickle.dump(model, file)

		for i in range(4):
			plt.figure()
			plt.plot(range(100), predicted_stock_data[:,i],'k-', label = 'Predicted '+cols[i]+' price')
			plt.plot(range(100),np.flipud(dataset[range(100),i]),'r--', label = 'Actual '+cols[i]+' price')
			plt.xlabel('Time steps')
			plt.ylabel('Price')
			plt.title(cols[i]+' price')
			plt.grid(True)
			plt.legend(loc = 'upper left')
			if not os.path.isdir('results'):
				os.makedirs('results')
			img_file = 'results/' + stock_name + '_' + cols[i] + '.png'
			result_imgs.append(img_file)
			plt.savefig(img_file)
		# plt.show()
		plt.close()

	else: 
		print('This is just too little')
	return mape, predicted_stock_data, result_imgs

def test(filepath, cols, labeled=False):
	result_imgs = []
	stock_name = filepath.split('/')[-1]
	stock_name = stock_name.split('.')[0]
	stock_name = stock_name.split('_')[0]
	stock_file = filepath
	if labeled:
		dataset, _ = lstm.createFromCsv(1, cols, stock_file)
	else: 
		dataFrameObj = labelDataAsDataFrameObj(filepath)
		dataset, _ = lstm.createFromDataFrameObj(1, cols, dataFrameObj)
	predicted_stock_data = np.empty([0,dataset.shape[1]])
	with open(save_path, "rb") as file: 
		model = pickle.load(file)
		for idx in reversed(range(NUM_TEST)):
			train_dataset = dataset[idx + 1:,:]
			test_data = dataset[idx,:] 
			num_examples = train_dataset.shape[0]

			iters = 1
			past_likelihood = []
			curr_likelihood = model.score(np.flipud(train_dataset[0:K - 1, :]))
			while iters < num_examples / K - 1:
				past_likelihood = np.append(past_likelihood, model.score(np.flipud(train_dataset[iters:iters + K - 1, :])))
				iters = iters + 1
			likelihood_diff_idx = np.argmin(np.absolute(past_likelihood - curr_likelihood))
			predicted_change = train_dataset[likelihood_diff_idx,:] - train_dataset[likelihood_diff_idx + 1,:]
			predicted_stock_data = np.vstack((predicted_stock_data, dataset[idx + 1,:] + predicted_change))
		
		mape = lstm.mean_absolute_percentage_error(predicted_stock_data, np.flipud(dataset[range(100),:]))

		print('mape:', mape)
		for i in range(4):
			plt.figure()
			plt.plot(range(100), predicted_stock_data[:,i],'k-', label = 'Predicted '+cols[i]+' price')
			plt.plot(range(100),np.flipud(dataset[range(100),i]),'r--', label = 'Actual '+cols[i]+' price')
			plt.xlabel('Time steps')
			plt.ylabel('Price')
			plt.title(cols[i]+' price')
			plt.grid(True)
			plt.legend(loc = 'upper left')
			if not os.path.isdir('results'):
				os.makedirs('results')
			img_file = 'results/' + stock_name + '_' + cols[i] + '.png'
			result_imgs.append(img_file)
			plt.savefig(img_file)
		plt.show()
		plt.close()

	return mape, predicted_stock_data, result_imgs
		
if __name__ == '__main__':
	train('dataset_CAC40/Michelin_labeled.csv', 10000, 0.8, labels, labeled=True)
	# test('dataset_CAC40/LVMH_labeled.csv', labels, labeled=True)