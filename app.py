from flask import Flask, request, render_template
from model.ModelPrediction import predict
from model.EmailFormat import SimplifiedEmail

app = Flask(__name__)

@app.route('/start')
def render_start_page():
    return render_template('start.html')


@app.route('/input')
def render_input_page():
    return render_template('input.html')


@app.route('/results', methods=['POST'])
def render_results_page():
    formattedEmail = SimplifiedEmail(request.form, True)
    predictions = predict('spamClassifier.pkl', formattedEmail)
    return render_template('results.html', pred=predictions)


if __name__ == '__main__':
    app.run()
