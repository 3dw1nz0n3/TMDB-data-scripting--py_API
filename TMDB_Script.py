import config # to hide TMDB API keys
import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import os
import pandas as pd
import tmdbsimple as tmdb
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # to format currency on charts axis

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
# Now we got the top 500 movie by popularity
columns = ['film', 'revenue', 'budget', 'release_date','genres','production_companies','original_language','adult','runtime','tagline','vote_average','vote_count','popularity']
highest_revenue_ever_df = pd.DataFrame(columns=columns)

for film in top1000_movies:
    # print(film['title'])

    film_revenue = requests.get('https://api.themoviedb.org/3/movie/'+ str(film['id']) +'?api_key='+ api_key+'&language=en-US')
    film_revenue = film_revenue.json()
    # print(film_revenue)

    # print(locale.currency(film_revenue['revenue'], grouping=True ))

    # Lord of the Rings duplicate w/ bad data was being returned  https://www.themoviedb.org/movie/454499-the-lord-of-the-rings

        # print(film_revenue['budget'])
        # add film title, revenue, budget and release date to the dataframe
    highest_revenue_ever_df.loc[len(highest_revenue_ever_df)]=[film['title'],film_revenue['revenue'],(film_revenue['budget']),film_revenue['release_date'],film_revenue['genres'],film_revenue['production_companies'],film_revenue['original_language'],film_revenue['adult'],film_revenue['runtime'],film_revenue['tagline'],film_revenue['vote_average'],film_revenue['vote_count'],film_revenue['popularity']]
    
highest_revenue_ever_df.head()    
highest_revenue_ever_df.to_csv('movie_10K.csv')
