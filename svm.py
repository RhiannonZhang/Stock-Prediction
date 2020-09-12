import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score
from sklearn.model_selection import train_test_split
from sklearn import svm
import os

import warnings
warnings.filterwarnings("ignore")

# Load the dataset

filedir = '/Users/xiaoxiao/dataset/final_data/'
outfiledir = '/Users/xiaoxiao/dataset/test_result/'

#, 'AAPL'
filelist = ['AAPL','VZ', 'AGN', 'PFE', 'CBS', 'PEP', 'UPS', 'JCP', 'MA',
         'HD', 'LMT', 'JNJ', 'TGT', 'S', 'CMG', 'IBM', 'NDAQ',
         'SBUX', 'KR', 'NVDA', 'KSS', 'BMY', 'NKE', 'LUV', 'AMZN',
         'CMCSA', 'GOOG', 'MS', 'WMT', 'INTC', 'GS', 'BLK', 'BAC', 'FB',
         'MSFT', 'NFLX', 'F', 'XOM', 'BA', 'GE', 'DIS', 'M', 'C', 'JPM']
# for each in filelist:
#     dataframe = dataframe.append(pd.read_csv(filedir+each+'.csv',header=0))
acc = []
f1 = []
pre = []
recall = []
for each in filelist:
    print(each)
    file = filedir + each + '.csv'
    dataframe = pd.read_csv(file, header=0)
    dataset = dataframe.iloc[:, list(range(1,109))].values
    dataset = dataset.astype('float32')
    filesize = len(dataset)
    print('Length of dataset:', filesize)


    x, y = np.split(dataset, (107,), axis=1) #
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.85)

        # 开始训练
    time_2 = time.time()
    print('Start training...')
    clf = svm.SVC(C=1, kernel='linear', gamma='auto', decision_function_shape='ovr')
    clf.fit(x_train, y_train.ravel())
    time_3 = time.time()
    print('training cost %f seconds' % (time_3 - time_2))


    print('Start predicting...')
    y_hat_tr = clf.predict(x_train)

    tr_score = accuracy_score(y_train, y_hat_tr)
    trf1 = f1_score(y_train, y_hat_tr, average='macro')

    y_hat_te = clf.predict(x_test)
    time_4 = time.time()
    print('predicting cost %f seconds' % (time_4 - time_3))

    te_score = accuracy_score(y_test, y_hat_te)
    tef1 = f1_score(y_test, y_hat_te, average='macro')
    tere = recall_score(y_test, y_hat_te, average='macro')
    tepe = precision_score(y_test, y_hat_te, average='macro')

    print('Accuracy of testing set', te_score)
    acc.append(te_score)
    print('F1 of testing set', tef1)
    f1.append(tef1)
    print('recall of testing set', tere)
    recall.append(tere)
    print('precision of testing set', tepe)
    pre.append(tepe)

    y_test = y_test.reshape((1,-1))[0]

    df = pd.DataFrame({'y_test': y_test, 'y_test_pre': y_hat_te})
    df.to_csv(outfiledir + each + '_test_pre.csv', index=False, sep=',')

df2 = pd.DataFrame({'comp': filelist, 'Accuracy': acc, 'F1_score': f1, 'recall': recall, 'precision': pre})
df2.to_csv(outfiledir + 'scores.csv', index=False, sep=',')

