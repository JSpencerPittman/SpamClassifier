from BuildModel.DataDownload import download_corpus
from model.EmailFormat import getEmailsAndLabels
from sklearn.model_selection import StratifiedShuffleSplit
from model.SpamClassifierModel import ClassifierModel

DATASETS_DIR = "datasets"

def buildModel(filename):
    download_corpus(DATASETS_DIR)
    emails, labels = getEmailsAndLabels('datasets/ham', 'datasets/spam')
    split = StratifiedShuffleSplit(test_size=0.2, random_state=42)
    for train_index, test_index in split.split(emails, labels):
        X_train, X_test = emails[train_index], emails[test_index]
        y_train, y_test = labels[train_index], labels[test_index]
    cml = ClassifierModel()
    cml.train(X_train, y_train)
    cml.dumpModel(filename)
