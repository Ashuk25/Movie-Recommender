from django.shortcuts import render
from django import forms
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('C:/Course/Moview Recommender Website/movierecommender/movierecommenderapp/templates/myApp/movie.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('C:/Course/Moview Recommender Website/movierecommender/movierecommenderapp/templates/myApp/similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0] #fetch the movie index
    distance = similarity[movie_index] # find the distance of similarity
    movie_list = sorted(enumerate(distance), reverse=True, key=lambda x:x[1])[0:9] # sorted list into descending order with tuple id (movie index). enumerate create the tuple.
    
    recommended_movies = []
    recommended_movies_poster = []
    dict1 = {}
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch movies poster
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    dict1['movies_name'] = recommended_movies
    dict1['movies_poster'] = recommended_movies_poster
    return dict1

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7a73cdf477499a24ab38bdbb2f809f9e'.format(movie_id))
    data = response.json()
    print(data)
    return 'https://image.tmdb.org/t/p/w154/' + data['poster_path']

movies_data = []
for i in range(len(movies['title'])):
    movies_data.append((movies['title'].iloc[i],movies['title'].iloc[i]))

class ExampleForm(forms.Form):
        movies_name = forms.ChoiceField(choices=movies_data)


# Create your views here.
def home(request):
    context = {}
    context['form'] = ExampleForm()
    if request.method == 'POST':
        movie_name = request.POST['movies_name']
        context['Data'] = recommend(movie_name)
        return render(request,"myApp/home.html",context)
    return render(request,"myApp/home.html",context)
