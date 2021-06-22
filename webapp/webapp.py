import sys
sys.path.append('/home/furkan/myworkspace/CSE-495/StockMarketFormations')
from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from numpy.lib.index_tricks import fill_diagonal
from Label import labelDataAsDataFrameObjForWeb
import lstm
import hmm
import os
app = Flask(__name__,static_folder='/')

global log
global result_list
cols = ['High', 'Low', 'Close', 'Label']
epoch = 100

@app.route('/')
@app.route('/home')
def home():
    global result_list
    global log
    return render_template('webapp.html', results=result_list, log=log)

@app.route('/submit_form',methods = ['POST'])
def submit_form():
    global log
    global result_list
    result_list = []
    labeled = False
    train = False
    _file = request.files['file']
    split = int(request.form.get('split')) / 100
    if request.form.getlist('labeled'):
        labeled = True
    if request.form.getlist('train'):
        train = True
    model = request.form.get('model')
    if not _file:
        return redirect(url_for('home'))
    filepath = 'tmp/' + _file.filename
    _file.save(filepath)
    if model == 'LSTM':
        if train:
            mape, predicted_data, result_list = lstm.train(filepath, epoch, split, cols, labeled)
        else:
            mape, predicted_data, result_list = lstm.test(filepath, labeled)
    else:
        if train:
            mape, predicted_data, result_list = hmm.train(filepath, epoch*100, split, cols, labeled)
        else:
            mape, predicted_data, result_list = hmm.test(filepath, labeled)
    log = 'mape: ' + str(mape)
    return redirect(url_for('home'))

@app.route('/go_home', methods = ['GET'])
def go_home():
    global result_list
    global log
    log = ""
    result_list = []
    # exec('cd results && rm -f *')
    return redirect(url_for('home'))

if __name__=='__main__':
    log = ""
    result_list = []
    app.run(debug=True)