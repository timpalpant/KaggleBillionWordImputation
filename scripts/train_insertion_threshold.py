#!/usr/bin/env python

import argparse
import numpy as np
from itertools import izip
from sklearn.metrics import make_scorer
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

class Prediction(object):
    def __init__(self, loc, ll_loc, word, ll_word, score_none, score_space, score_word):
        self.loc = loc
        self.ll_loc = ll_loc
        self.word = word
        self.ll_word = ll_word
        self.score_none = score_none
        self.score_space = score_space
        self.score_word = score_word
        self.scores = [self.score_none, self.score_space, self.score_word]
        
    @classmethod
    def parse(cls, line):
        entry = line.rstrip().split('\t')
        entry[0] = int(entry[0])
        entry[1] = float(entry[1])
        entry[3] = float(entry[3])
        entry[4] = int(entry[4])
        entry[5] = int(entry[5])
        entry[6] = int(entry[6])
        return cls(*entry)
        
def score(golden, predictions):
    golden_score = np.asarray([s[yi] for s, yi in izip(scores, golden)])
    p_score = np.asarray([s[yi] for s, yi in izip(scores, predictions)])
    return p_score.mean()
    return (p_score - golden_score).mean()

def opts():
    parser = argparse.ArgumentParser(
        description='Find optimal threshold for inserting words')
    parser.add_argument('results', type=argparse.FileType('r'),
        help='File with prediction results')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print "Loading results"
    results = map(Prediction.parse, args.results)
    
    print "Making data frames"
    X = np.array([[p.loc, p.ll_loc, len(p.word), p.ll_word] 
                  for p in results])
    y = np.asarray([np.argmin(p.scores) for p in results])
    scores = np.array([p.scores for p in results])
    scorer = make_scorer(score, greater_is_better=False, scores=scores)
    scorer = 'accuracy'
    
    d = np.asarray([s[yi] for s, yi in izip(scores, y)])
    print "Best achievable Levenshtein distance = %s" % d[len(d)/2:].mean()
    
    print "Making LogisticRegression model"
    clf = LogisticRegression(C=1.)
    cv = GridSearchCV(clf, param_grid={'C': [0.1, 0.5, 1., 5., 10.]}, 
                      cv=3, scoring=scorer, n_jobs=4, verbose=10)
    print "Fitting LogisticRegression model"
    cv.fit(X, y)
    print cv.grid_scores_
    print cv.best_estimator_
    print cv.best_params_
    print cv.best_score_
    clf = cv.best_estimator_
    clf.fit(X[:len(X)/2], y[:len(X)/2])
    y_pred = clf.predict(X[len(X)/2:])
    d = np.asarray([s[yi] for s, yi in izip(scores[len(X)/2:], y_pred)])
    print "Achieved Levenshtein distance = %s" % d.mean()
    
    print "Making DecisionTree model"
    clf = DecisionTreeClassifier()
    cv = GridSearchCV(clf, param_grid={'min_samples_split': [1, 2, 5, 10]}, 
                      cv=3, scoring=scorer, n_jobs=4, verbose=10)
    print "Fitting DecisionTree model"
    cv.fit(X, y)
    print cv.grid_scores_
    print cv.best_estimator_
    print cv.best_params_
    print cv.best_score_
    clf = cv.best_estimator_
    clf.fit(X[:len(X)/2], y[:len(X)/2])
    y_pred = clf.predict(X[len(X)/2:])
    d = np.asarray([s[yi] for s, yi in izip(scores[len(X)/2:], y_pred)])
    print "Achieved Levenshtein distance = %s" % d.mean()
    
    print "Making RandomForest model"
    clf = RandomForestClassifier(n_estimators=100)
    cv = GridSearchCV(clf, param_grid={'min_samples_split': [1, 2, 5, 10]}, 
                      cv=3, scoring=scorer, n_jobs=4, verbose=10)
    print "Fitting RandomForest model"
    cv.fit(X, y)
    print cv.grid_scores_
    print cv.best_estimator_
    print cv.best_params_
    print cv.best_score_
    clf = cv.best_estimator_
    clf.fit(X[:len(X)/2], y[:len(X)/2])
    y_pred = clf.predict(X[len(X)/2:])
    d = np.asarray([s[yi] for s, yi in izip(scores[len(X)/2:], y_pred)])
    print "Achieved Levenshtein distance = %s" % d.mean()
    
    print "Making LinearSVM model"
    clf = LinearSVC()
    cv = GridSearchCV(clf, param_grid={'C': [0.1, 0.5, 1., 5., 10.]}, 
                      cv=3, scoring=scorer, n_jobs=4, verbose=10)
    print "Fitting LinearSVM model"
    cv.fit(X, y)
    print cv.grid_scores_
    print cv.best_estimator_
    print cv.best_params_
    print cv.best_score_
    clf = cv.best_estimator_
    clf.fit(X[:len(X)/2], y[:len(X)/2])
    y_pred = clf.predict(X[len(X)/2:])
    d = np.asarray([s[yi] for s, yi in izip(scores[len(X)/2:], y_pred)])
    print "Achieved Levenshtein distance = %s" % d.mean()
    