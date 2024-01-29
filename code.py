from flask import Flask, render_template, request, jsonify
from googletrans import Translator  # You need to install the 'googletrans' library

app = Flask(__name__)

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text_to_translate = data.get('text', '')
    target_language = data.get('language', 'en')

    translation = translator.translate(text_to_translate, dest=target_language)
    
    return jsonify({'translation': translation.text})

if __name__ == '__main__':
    app.run(debug=True)
