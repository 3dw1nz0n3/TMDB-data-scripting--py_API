import requests # to make TMDB API calls
import locale # to format currency as USD
import tmdbsimple as tmdb
locale.setlocale( locale.LC_ALL, '' )
import pandas as pd
import pickle

api_key = 'Your Key' # get TMDB API key from config.py file

import tmdbsimple as tmdb
tmdb.API_KEY = api_key #This sets the API key setting for the tmdb object
search = tmdb.Search() #this instantiates a tmdb "search" object which allows your to search for the movie
import os.path

# These functions take in a string movie name !
def grab_poster_tmdb(movie):
    
    response = search.movie(query=movie)
    id=response['results'][0]['id']
    movie = tmdb.Movies(id)
    posterp=movie.info()['poster_path']
    title=movie.info()['original_title']
    
    url='image.tmdb.org/t/p/original'+posterp
    title='_'.join(title.split(' '))
    strcmd='wget -O '+poster_folder+title+'.jpg '+url
    os.system(strcmd)

def get_movie_id_tmdb(movie):
    response = search.movie(query=movie)
    movie_id=response['results'][0]['id']
    return movie_id

def get_movie_info_tmdb(movie):
    response = search.movie(query=movie)
    id=response['results'][0]['id']
    movie = tmdb.Movies(id)
    info=movie.info()
    return info

def get_movie_genres_tmdb(movie):
    response = search.movie(query=movie)
    id=response['results'][0]['id']
    movie = tmdb.Movies(id)
    genres=movie.info()['genres']
    return genres
# Test check 
print (get_movie_genres_tmdb("The Matrix"))

info=get_movie_info_tmdb("The Matrix")
print ('All the Movie information from TMDB gets stored in a dictionary with the following keys for easy access -')
info.keys()

all_movies=tmdb.Movies()
top_movies=all_movies.popular()

# This is a dictionary, and to access results we use the key 'results' which returns info on 20 movies
len(top_movies['results'])
top10000_movs=top_movies['results']

# Comment out this cell once the data is saved into pickle file.
all_movies=tmdb.Movies()
top10000_movies=[]
print('Pulling movie list, Please wait...')
for i in range(0,501):
    if i%15==0:
        time.sleep(7)
    movies_on_this_page=all_movies.popular(page=i)['results']
    top10000_movies.extend(movies_on_this_page)
len(top10000_movies)
f3=open('movie_list_full.pckl','wb')
pickle.dump(top10000_movies,f3)
f3.close()
print('Done!')
# Now we got the top 10000 movie by popularity
columns = ['film', 'revenue', 'budget', 'release_date','genres','production_companies','original_language','adult','runtime','tagline','vote_average','vote_count','popularity']
highest_revenue_ever_df = pd.DataFrame(columns=columns)

for film in top10000_movies:
    # print(film['title'])

    film_popular = requests.get('https://api.themoviedb.org/3/movie/'+ str(film['id']) +'?api_key='+ api_key+'&language=en-US')
    film_popular = film_popular.json()
    film_popular_df.loc[len(film_popular_df)]=[film['title'],film_popular['revenue'],(film_popular['budget']),film_popular['release_date'],film_popular['genres'],film_popular['production_companies'],film_popular['original_language'],film_popular['adult'],film_popular['runtime'],film_popular['tagline'],film_popular['vote_average'],film_popular['vote_count'],film_popular['popularity']]
    
film_popular_df.head()    
film_popular_df.to_csv('movie_10K.csv')
