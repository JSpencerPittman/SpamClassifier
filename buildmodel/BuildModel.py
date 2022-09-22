from buildmodel.DataDownload import download_corpus
from model.EmailFormat import get_emails_and_labels
from sklearn.model_selection import StratifiedShuffleSplit
from model.SpamClassifierModel import SpamClassifierModel

DATASETS_DIR = "datasets"


# This method downloads from https://spamassassin.apache.org/old/publiccorpus/
# The current datasets being used are easy_hpam and spam
def build_model(filename):
    download_corpus(DATASETS_DIR)
    emails, labels = get_emails_and_labels('datasets/ham', 'datasets/spam')
    split = StratifiedShuffleSplit(test_size=0.2, random_state=42)
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    for train_index, test_index in split.split(emails, labels):
        x_train, x_test = emails[train_index], emails[test_index]
        y_train, y_test = labels[train_index], labels[test_index]
    cml = SpamClassifierModel()
    cml.train(x_train, y_train)
    cml.store_model(filename)
