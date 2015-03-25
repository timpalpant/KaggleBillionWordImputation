#!/usr/bin/env python

import argparse
import cPickle as pickle
from itertools import izip
import numpy as np
from util import Prediction
from sklearn.metrics import make_scorer, accuracy_score, \
    average_precision_score, f1_score, roc_auc_score
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, label_binarize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.cross_validation import train_test_split
        
def load(fd):
    d = np.load(args.data)
    return d['X'], d['y'], d['d']

def opts():
    parser = argparse.ArgumentParser(
        description='Find optimal threshold for inserting words')
    parser.add_argument('data', type=argparse.FileType('r'),
        help='npz file with training data')
    parser.add_argument('output', type=argparse.FileType('w'),
        help='Pickle file with trained classifiers')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    results = {}
    
    print "Loading training data"
    X, y, d = load(args.data)
    assert len(X) == len(y)
    assert len(y) == len(d)
    X[np.isinf(X)] = 0
    X[np.isnan(X)] = 0   
 
    print "Splitting into train and test"
    X_train, X_test, y_train, y_test, d_train, d_test = train_test_split(X, y, d,
        test_size=0.2, random_state=123)
    
    print "Scaling features"
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    results['scaler'] = scaler
    
    def test_clf(clf):
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        print "unweighted accuracy = %.3f" % accuracy_score(y_test, y_pred)
        dx = np.mean([s[yi] for s, yi in izip(d_test, y_pred)])
        print "Levenshtein distance = %s" % dx
    
    #print "Training LogisticRegression model"
    #lr = LogisticRegression(C=1.)
    #test_clf(lr)
    #results['lr'] = lr
    
    #print "Training DecisionTree model"
    #dt = DecisionTreeClassifier()
    #test_clf(dt)
    #results['dt'] = dt
    
    print "Training RandomForest model"
    rf = RandomForestClassifier(n_estimators=20*8, n_jobs=8)
    test_clf(rf)
    results['rf'] = rf
    
    #print "Training LinearSVM model"
    #svm = LinearSVC()
    #test_clf(svm)
    #results['svm'] = svm
    
    pickle.dump(results, args.output)
