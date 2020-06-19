
from search import Search
from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import json
import pickle
from sentence_transformers import SentenceTransformer
import scipy.spatial

app = Flask(__name__)
app.df = pd.read_csv('data/products.csv', index_col=None)
app.embedder = SentenceTransformer('bert-base-nli-mean-tokens')
app.corpus = list(app.df['Product Name'])
# corpus_embeddings = embedder.encode(corpus)
with open("data/corpus_embeddings.pkl", "rb") as fp:
    app.corpus_embeddings = pickle.load(fp)
app.search = Search(app.df, app.embedder, app.corpus, app.corpus_embeddings)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = ''
    result = ''
    method = 'string'
    show_images = 'hideImages'

    if request.method == 'POST':
        search_term = request.form.get('searchTerm', search_term)
        method = request.form.get('method', method)
        show_images = request.form.get('showImages', show_images)
        return redirect(url_for('search', search_term=search_term, method=method, show_images=show_images))

    return render_template('search.html', search_term=search_term, result=result, method=method, show_images=show_images)


@app.route('/<method>/<search_term>/<show_images>', methods=['GET', 'POST'])
def search(search_term, method, show_images):
    if request.method == 'POST':
        search_term = request.form.get('searchTerm', search_term)
        method = request.form.get('method', method)
        show_images = request.form.get('showImages', 'hideImages')
        return redirect(url_for('search', search_term=search_term, method=method, show_images=show_images))
        
    data = json.loads(app.search(search_term, method))
    result = []

    for d in data:
        image_paths = d['Images'].replace('[', '').replace(']', '').split(',')
        new_image_paths = [image.strip('\"') for image in image_paths]

        result.append({
            'URL': d['URL'],
            'Product Name': d['Product Name'],
            'Product ID': d['Product ID'],
            'Listing Price': d['Listing Price'],
            'Sale Price': d['Sale Price'],
            'Discount': d['Discount'],
            'Brand': d['Brand'],
            'Description': d['Description'],
            'Rating': d['Rating'],
            'Reviews': d['Reviews'],
            'Images': new_image_paths,
            'Last Visited': d['Last Visited']
        })

    number_of_results = len(result)
    return render_template('search.html', search_term=search_term, result=result, number_of_results=number_of_results, method=method, show_images=show_images)

@app.errorhandler(404) 
def not_found(e): 
  return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run()

