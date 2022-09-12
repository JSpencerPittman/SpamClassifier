from sklearn.preprocessing import StandardScaler
from model.EmailQuantify import EmailWordCounter, EmailQuantifier
import numpy as np


class DataPreparer:
    def prepareTrainData(self, x, y):
        ewc = EmailWordCounter(x, y)
        ewc.calcKeySpamWordsDict()
        self.keySpamWordsDict = ewc.keySpamWordsDict
        self.stdScal = StandardScaler()
        y_prep = self.prepareY(y)
        x_prep = self.prepareX(x, True)
        return x_prep, y_prep

    def prepareY(self, y):
        y_prep = []
        for i in range(len(y)):
            y_prep.append(int(y[i]))
        return y_prep

    def prepareX(self, x, train=False):
        eq = EmailQuantifier(self.keySpamWordsDict)
        nrs = eq.quantifyBatchEmails(x)
        x_quantified = np.array(nrs)
        if train:
            self.stdScal.fit(x_quantified)
        x_prep = self.stdScal.transform(x_quantified)
        return x_prep

    def prepareTestData(self, x):
        return self.prepareX(x)