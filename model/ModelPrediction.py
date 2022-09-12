from joblib import load

def predict(modelFilename, email):
    model = load(modelFilename)
    prediction = [0,0]
    prediction[0] = model.predict(email)[0]
    prediction[1] = int(model.certainty(email)*100)
    return prediction