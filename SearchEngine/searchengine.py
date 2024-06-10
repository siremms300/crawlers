from flask import Flask, render_template, request 
import pickle 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import networkx as nx

app = Flask(__name__, template_folder='./static/')

@app.route("/")
def websearch():
    return render_template('websearch.html')  



@app.route("/websearch", methods=['GET', 'POST']) 
def web_search():
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            if query == '':
                return render_template('websearch.html') 
            
            websites = ['https://www.university-directory.eu/USA/Alabama', 
                        'https://www.university-directory.eu/USA/Alaska',
                        'https://www.university-directory.eu/USA/Arizona' 
                        ] 
            
            tokenized_text = load_tokenized_text('tokenized_text.pkl', query)
            return render_template('results.html', data={'query': query, 'results': tokenized_text})
        else:
            # Handle the case when 'query' is not present in the form data
            return render_template('websearch.html') 
    else:
        # Render the initial websearch.html template for GET requests
        return render_template('websearch.html')









def load_tokenized_text(filename, query):
    tokenized_text = pickle.load(open(filename, 'rb')) 
    tfidf = TfidfVectorizer() 
    tfidf_vectors = tfidf.fit_transform(' '.join(tokens) for tokens in tokenized_text) 

    query_vector = tfidf.transform([query])  
    similarities = cosine_similarity(query_vector, tfidf_vectors) 

    if all_zeros(similarities[0]):
        return "No results found for the query: '{}'".format(query)
    
    G = nx.DiGraph 

    for i, link in enumerate(websites):
        G.add_node(link) 
        for j, sim in enumerate(similarities[0]):
            if sim > 0 and i != j:
                G.add_edge(link, websites[j], weight=sim) 

        pagerank = nx.pagerank(G) 

        ranked_result = sorted(pagerank.items(), key=lambda x:x[1]) 
        top_results = [x[0] for x in ranked_result if x[1] >= 0.14] 

        return top_results

    print(similarities)
    return tokenized_text



def all_zeros(l):
    for i in l:
        if i != 0:
            return False 
    return True 


if __name__ == '__main__':
    app.run(debug=True)
