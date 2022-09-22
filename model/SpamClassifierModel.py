from model.DataPrep import DataPreparer
from sklearn.ensemble import RandomForestClassifier
from model.EmailFormat import SimplifiedEmail
from joblib import dump


# This class is responsible for proving an interface for
# the program to create/save a model but also use a pickled
# model
# x_group should be a numpy array of model.EmailFormat.SimplifiedEmail
# x should be a single model.EmailFormat.SimplifiedEmail
# y should be a numpy array of floats or ints
class SpamClassifierModel:
    def __init__(self):
        self.dp = None
        self.model = RandomForestClassifier()

    def train(self, x_group, y):
        self.dp = DataPreparer()
        x_prep, y_prep = self.dp.prepare_train_data(x_group, y)
        self.model.fit(x_prep, y_prep)

    # returns predicted class
    def predict(self, x):
        x = SpamClassifierModel.ensure_2d_array(x)
        x_prep = self.dp.prepare_test_data(x)
        return self.model.predict(x_prep)[0]

    # Returns the prediction probability for each class as an array
    # [chance of class 0, ..., chance of class n]
    def predict_proba(self, x):
        x = SpamClassifierModel.ensure_2d_array(x)
        x_prep = self.dp.prepare_test_data(x)
        return self.model.predict_proba(x_prep)[0]

    # Returns the prediction probability for the
    # predicted class
    def certainty(self, x):
        probs = self.predict_proba(x)
        return max(probs)

    # Ensures that all training set(s) passed in
    # are in 2D form for the sklearn classes
    @staticmethod
    def ensure_2d_array(ts):
        if type(ts) == SimplifiedEmail:
            ts = [ts]
        return ts

    # Utilize joblib to store(pickle) the model
    def store_model(self, filename="classifierModel.pkl"):
        dump(self, filename)
