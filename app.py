from flask import Flask, request, jsonify, render_template
import pickle
import requests
import pandas as pd
import os

app = Flask(__name__)

# Load the model and data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

@app.route('/')
def home():
    template_dir = os.path.join(os.getcwd(), 'templates')
    print(f"Template Directory: {template_dir}")
    print(f"Files in Template Directory: {os.listdir(template_dir)}")
    return render_template('index.html', movies=movies['title'].values)

# @app.route('/')
# def home():
#     return render_template('index.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie_name = request.form.get('movie_name')
    recommended_movie_names, recommended_movie_posters = recommend(movie_name)
    return render_template('recommend.html', 
                           movie_names=recommended_movie_names, 
                           movie_posters=recommended_movie_posters, zip = zip)

if __name__ == '__main__':
    app.run(debug=True)
