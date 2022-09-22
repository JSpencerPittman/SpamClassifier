from joblib import load


def predict(model_filename, email):
    model = load(model_filename)
    prediction = [0, 0]
    prediction[0] = model.predict(email)[0]
    prediction[1] = int(model.certainty(email) * 100)
    return prediction
