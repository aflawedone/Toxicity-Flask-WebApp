from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd

app = Flask(__name__)

# Get absolute paths for model and vectorizer
base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, 'toxicity_model.pkl')
vectorizer_path = os.path.join(base_path, 'count_tf_idf.pkl')

# Load the model and vectorizer
model = pickle.load(open(model_path, 'rb'))
tfidf_vectorizer = pickle.load(open(vectorizer_path, 'rb'))
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page

# Fit the tfidf_vectorizer to a larger corpus of text
"""ob_pf_txtpath = os.path.join(base_path, 'en.txt')
corpus = [line.strip() for line in open(ob_pf_txtpath, 'r')]"""  # list of text documents

ob_pf_path = os.path.join(os.getcwd(), r'C:\TweetProject2\FinalBalancedDataset.csv')
df = pd.read_csv(ob_pf_path)
corpus = df['tweet'].tolist()

# Save the fitted tfidf_vectorizer to a file
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)

def check_toxicity(text):
    try:
        # Transform the input text using the tfidf_vectorizer
        transformed_text = tfidf_vectorizer.transform([text])[:, :len(tfidf_vectorizer.vocabulary_)]
        print(f"Transformed text: {transformed_text}")
        # Predict the toxicity
        prediction = model.predict_proba(transformed_text)[0][1]
        print(f"Prediction: {prediction}")
        if prediction > 0.5:  # If prediction is less than the threshold
            is_toxic = True
        else:
            is_toxic = False
        
        print(f"Is toxic: {is_toxic}")
        return is_toxic
    except Exception as e:
        print(f"Error during toxicity check: {e}")
        return None


# In the check_toxicity function, load the fitted tfidf_vectorizer and use it to transform the input text
@app.route('/check_toxicity', methods=['POST'])
def api_check_toxicity():
    try:
        data = request.get_json()
        text = data['text']
        print(f"Received text: {text}")
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        is_toxic = check_toxicity(text)

        if is_toxic is None:
            return jsonify({'error': 'Error during toxicity check'}), 500

        return jsonify({'isToxic': str(is_toxic)})
    except Exception as e:
        print(f"Error during API request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)