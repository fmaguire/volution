
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import seaborn as sns
import os
import pickle

# ### Parse data
#
# - X and y generated manually by downloading swissprot TM-annotated sequences for Archaea, Eukaryotes and Bacteria (NR database was too big to acquire Bacteria easily).
#
# - Additionally, acquire the full archaea and euk Nr database to increase data.
#
# - Get bac from ensembl ftp
#
# - Cluster at 100% identity to remove any redundancy and run TMHMM on these sequences (TMHMM validation analysis in another notebook)
#
# - Parse tmhmm results and get TM_seqs +/- 3 residues using ```get_tm_seqs.py```

# In[2]:

def create_X_Y(data_locs):
    """
    Parse data_locs to create X and y lists
    """
    X, Y = [], []
    for label, path in data_locs.items():
        with open(path) as fh:
            for line in fh.readlines():
                X.append(line.strip())
                Y.append(label)
    return X, Y

def balance_classes(X, y):
    """
    Resample classes to balance
    """
    label_ranges = {}
    index = 0
    for label in y:
        if label not in label_ranges:
            label_ranges.update({label: [1, index, index]})
        else:
            label_ranges[label][0] = label_ranges[label][0]+1
            label_ranges[label][2] = label_ranges[label][2]+1
        index += 1

    size = min([x[0] for x in label_ranges.values()])

    print("Resampling classes to |{}|".format(size))

    Y_resample = []
    X_resample = []

    for label, ranges in label_ranges.items():
        # exclusive top range therefore the +1
        indices = np.random.randint(ranges[1], ranges[2]+1, size)

        X_resample = X_resample + list(operator.itemgetter(*indices)(X))
        Y_resample = Y_resample + [label] * size

    return X_resample, Y_resample

def y_encode(Y):
    """
    Encode list of labels into Nx3 matrix
    """
    mapping = {'archaea': [1.0,0.0,0.0],
               'bacteria': [0.0,1.0,0.0],
               "eukaryote":[0.0,0.0,1.0]}
    return np.array([mapping[y] for y in Y])

def y_encode2(Y):
    """
    Encode list of labels into Nx3 matrix
    """
    mapping = {'archaea': [1.0,0.0],
                 "eukaryote":[0.0,1.0]}
    return np.array([mapping[y] for y in Y])

def x_encode(X):
    """
    Onehot encoder of sequences in X list
    """
    X_encoding_dict = {'*': 0}

    X_enc = []

    for vec in X:
        enc_vec = []
        for aa in vec:
            if aa not in X_encoding_dict:
                max_val = max(X_encoding_dict.values())
                X_encoding_dict.update({aa: max_val+1})
            enc_vec.append(X_encoding_dict[aa])
        X_enc.append(enc_vec)

    return X_enc, X_encoding_dict

def pad_X(X, maxsize):
    """
    Pad Xs out to same length
    """
    X_padded = []
    X_lengths = []
    for x in X:
        diff = len(x) - maxsize
        X_lengths.append(len(x))
        if diff < 0:
            X_padded.append(list(x) + ["*"]*np.abs(diff))
        elif diff > 0:
            X_padded.append(list(x)[:size])
        else:
            X_padded.append(list(x))
    return X_padded, X_lengths

def test_train(X, Y, X_lengths, testprop=0.2, CV=False):
    """
    Calculate test_train split
    """
    train_mask = np.random.rand(len(X)) < (1-testprop)
    test_mask = np.invert(train_mask)

    if CV:
        X_train = X[train_mask]
        X_test = X[test_mask]
    else:
        X_train = np.expand_dims(X[train_mask], -1)
        X_test = np.expand_dims(X[test_mask], -1)

    train = (sklearn.utils.shuffle(X_train,
                                   Y[train_mask],
                                   X_lengths[train_mask]))
    test = (sklearn.utils.shuffle(X_test,
                                  Y[test_mask],
                                  X_lengths[test_mask]))

    return train, test

if __name__=='__main__':

    data_locs = {'archaea': "../tm_prediction/full_data/tmhmm/tm_seqs/archaea_data.txt",
                 'bacteria': "../tm_prediction/validation/tmhmm/tm_seqs/bacteria_seqs.txt",
                 'eukaryote': "../tm_prediction/full_data/tmhmm/tm_seqs/eukaryote_data.txt"}

    X_raw, Y_raw = create_X_Y(data_locs)
    print("Raw X y parsed")

    X_resample, Y_resample = balance_classes(X_raw, Y_raw)
    print("X y resampled")

    X_resample, X_lengths = pad_X(X_resample, 40)
    print("X y padded")

    X, encoding_dict = x_encode(X_resample)
    with open('x_encoding_dict.pkl', 'wb') as fh:
        pickle.dump(encoding_dict, fh)

    Y = y_encode(Y_resample)
    X = np.array(X)
    X_lengths = np.array(X_lengths)
    print("X y encoded")

    Train, Test = test_train(X, Y, X_lengths)
    Test, CV = test_train(*Test, testprop=0.5, CV=True)
    #print("X y test/train split")

    train_data, train_labels, train_lengths = Train
    cv_data, cv_label, cv_seqlen = CV

