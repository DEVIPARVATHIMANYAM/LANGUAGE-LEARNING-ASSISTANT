from flask import Flask, render_template, request
import nltk
from nltk.corpus import wordnet

app = Flask(__name__)

# Download WordNet data (if not already downloaded)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def get_word_data(word):
    synonyms = set()
    antonyms = set()
    definitions = []
    examples = []

    for syn in wordnet.synsets(word):
        definitions.append(syn.definition())
        examples.extend(syn.examples())
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name())
    
    return list(definitions), examples, list(synonyms), list(antonyms)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_word', methods=['POST'])
def process_word():
    word = request.form['word'].strip().lower()
    
    if not word:
        return render_template('index.html', error="Please enter a word to search.")

    definitions, examples, synonyms, antonyms = get_word_data(word)

    return render_template(
        'index.html',
        word=word,
        definitions=definitions,
        examples=examples,
        synonyms=synonyms,
        antonyms=antonyms
    )

if __name__ == "__main__":
    app.run(debug=True)
