from sklearn.preprocessing import StandardScaler
from typing import Tuple, Any, List

from model.EmailQuantify import EmailWordCounter, EmailQuantifier
import numpy as np


class DataPreparer:
    def __init__(self):
        self.keySpamWordsDict = None
        self.stdScal = None

    def prepare_train_data(self, x,y):
        ewc = EmailWordCounter(x, y)
        ewc.calc_key_spam_words_dict()
        self.keySpamWordsDict = ewc.key_spam_words_dict
        self.stdScal = StandardScaler()
        y_prep = self.prepare_y(y)
        x_prep = self.prepare_x(x, True)
        return x_prep, y_prep

    @staticmethod
    def prepare_y(y):
        y_prep = []
        for i in range(len(y)):
            y_prep.append(int(y[i]))
        return y_prep

    def prepare_x(self, x, train=False):
        eq = EmailQuantifier(self.keySpamWordsDict)
        nrs = eq.quantify_batch_emails(x)
        x_quantified = np.array(nrs)
        if train:
            self.stdScal.fit(x_quantified)
        x_prep = self.stdScal.transform(x_quantified)
        return x_prep

    def prepare_test_data(self, x):
        return self.prepare_x(x)
