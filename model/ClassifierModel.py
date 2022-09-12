from model.DataPrep import DataPreparer
from sklearn.ensemble import RandomForestClassifier
from model.EmailFormat import SimplifiedEmail
from joblib import dump


class ClassifierModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, x, y):
        self.dp = DataPreparer()
        x_prep, y_prep = self.dp.prepareTrainData(x, y)
        self.model.fit(x_prep, y_prep)

    def predict(self, x):
        x = self.fixX(x)
        x_prep = self.dp.prepareTestData(x)
        return self.model.predict(x_prep)

    def predict_proba(self, x):
        x = self.fixX(x)
        x_prep = self.dp.prepareTestData(x)
        return self.model.predict_proba(x_prep)

    def certainty(self, x):
        x = self.fixX(x)
        x_prep = self.dp.prepareTestData(x)
        probs = self.model.predict_proba(x_prep)
        return max(probs[0])

    def fixX(self, x):
        if (type(x) == SimplifiedEmail):
            x = [x]
        return x

    def dumpModel(self, filename="classifierModel.pkl"):
        dump(self, filename)
