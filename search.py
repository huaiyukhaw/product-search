
import pandas as pd
import scipy.spatial

class Search(object):
    def __init__(self, dataframe, embedder,corpus, corpus_embeddings):
        self.df = dataframe
        self.embedder = embedder
        self.corpus = corpus
        self.corpus_embeddings = corpus_embeddings

    def __call__(self, search_term, method):

        if method == 'string':
            new_df = self.df[(self.df['Product Name'].str.contains(search_term, case=False)) | (self.df['Description'].str.contains(search_term, case=False)) | (self.df['Brand'].str.contains(search_term, case=False))].drop_duplicates()
            return new_df.to_json(orient='records')
        
        elif method == 'semantic':
            query_embeddings = self.embedder.encode([search_term])
            query_embedding = query_embeddings[0]

            closest_n = 10
            distances = scipy.spatial.distance.cdist([query_embedding], self.corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
            
            names = []
            for idx, distance in results[0:closest_n]:
                names.append(self.corpus[idx].strip())

            names = list(set(names))
            all_df = []
            for name in names:
                all_df.append(self.df[(self.df['Product Name'].str.contains(name))].drop_duplicates())

            new_df = pd.concat(all_df, ignore_index=True).drop_duplicates()
            return new_df.to_json(orient='records')
