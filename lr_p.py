# Author: Rushikesh Nalla
# Date: 21st July, 2017

from sklearn.linear_model import LinearRegression
import csv
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, KFold
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed
import multiprocessing
import matplotlib.pyplot as plt
import statistics


def machine(k, temp1, temp2):
    X_train, X_test, y_train, y_test = train_test_split(temp1, temp2, test_size=0.2, random_state=k)
    X_train = [[float(j) for j in i] for i in X_train]
    X_test = [[float(j) for j in i] for i in X_test]
    y_train = [int(i) for i in y_train]
    y_test = [int(i) for i in y_test]
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    #parameters = {'solver': ('lbfgs', 'sgd', 'adam'), 'hidden_layer_sizes': [(16,), (32,)], 'alpha':
    #    [1e-1, 1e-3, 1e-5, 1e-7]}

    clf = LinearRegression()
    #grid = GridSearchCV(clf, parameters)
    #cv = KFold(n_splits=10)
    #scores = cross_val_score(clf, X_train, y_train, cv=cv)
    #print(scores)
    #print(statistics.mean(scores))
    print(statistics.mean(y_test))
    clf.fit(X_train, y_train)
    print(clf.predict(X_test))
    print(clf.coef_, clf.intercept_)
    accuracy = clf.score(X_test, y_test)

    #print(accuracy)
    #return accuracy

if __name__ == '__main__':
    dataPath = "/home/geospacial2/PycharmProjects/BTP/"
    with open(os.path.join(dataPath, "rain2014_1.csv"), 'rt') as csvfile:
        reader = csv.reader(csvfile)
        temp1 = []
        temp2 = []
        next(reader, None)
        for row in reader:
            temp1.append(row[9:17])
            temp2.append(row[22])

    temp1 = StandardScaler().fit_transform(temp1)
    niter = 1
    ans = 0.
    inputs = range(niter)
    num_cores = multiprocessing.cpu_count()
    ans = Parallel(n_jobs=num_cores)(delayed(machine)(l, temp1, temp2) for l in inputs)
    #print(statistics.mean(ans))
    #print(statistics.stdev(ans))
    #plt.hist(ans, normed=True, bins=30)
    #plt.xlabel('Accuracy')
    #plt.show()