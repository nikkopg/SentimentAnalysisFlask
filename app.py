from flask import Flask, render_template, request, redirect
import joblib
from preprocessText import *

app = Flask(__name__, template_folder='template')
dicts = {
    0: 'Negative',
    1: 'Positive'
}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        model = joblib.load('review-sentiment_rs-xgboost.pkl')
        input_text = request.form['input_text']
        _, _, preprocessed_text = preprocess_text(input_text)

        prediction_ = model.predict([preprocessed_text])
        sentiment_ = f'\n"{dicts[prediction_[0]]}"'
        return render_template('result.html', prediction=sentiment_)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)