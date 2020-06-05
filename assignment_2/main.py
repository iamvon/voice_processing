import ast
from flask import Flask, request, render_template, Response
import pickle
import librosa
import math
import numpy as np
from sklearn.cluster import KMeans
from flask import jsonify

app = Flask(__name__)

def get_mfcc(file_path):
    y, sr = librosa.load(file_path) # read .wav file
    hop_length = math.floor(sr*0.010) # 10ms hop
    win_length = math.floor(sr*0.025) # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    # substract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1,1)) 
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0) # O^r
    # return T x 36 (transpose of X)
    return X.T # hmmlearn use T x N matrix

# Kmeans
def clustering(X, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, n_init=50, random_state=0, verbose=0)
    kmeans.fit(X)
    return kmeans  

@app.route('/', methods=['GET'])    
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    file_name = 'record/af5812b0-1702-44c0-8fee-36da31f72313.wav'
    # file_name = request.get_json()['file_name']
    sound_mfcc = get_mfcc(file_name)
    kmeans = clustering(sound_mfcc)
    sound_mfcc = kmeans.predict(sound_mfcc).reshape(-1,1)

    models = pickle.load(open('model/m.pkl', 'rb'))
    score = {cname : model.score(sound_mfcc, [len(sound_mfcc)]) for cname, model in models.items()}
    predict = max(score.keys(), key=(lambda k: score[k]))
    # return jsonify(score)
    return predict

    # sound_mfcc = get_mfcc(file_name)
    # models = pickle.load(open("model/models.pkl", "rb"))
    # score = {cname : model.score(sound_mfcc, [len(sound_mfcc)]) for cname, model in models.items()}
    # predict = max(score, key=score.get)
    # return jsonify(score)
    # return predict

if __name__ == "__main__":
    app.run(debug=True)
