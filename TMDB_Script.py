import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import tmdbsimple as tmdb # import tmdbsimple to make the request
import json # import json to read the result in json 
import time
import pandas as pd
import pickle # import pickle to open the search result in pickle 

api_key = 'Your key' # enter your API key

import tmdbsimple as tmdb
tmdb.API_KEY = api_key #This sets the API key setting for the tmdb object
search = tmdb.Search() #this instantiates a tmdb "search" object which allows your to search for the movie

# These functions take in a string movie name i.e. like "The Matrix" or "Interstellar"
# What they return is pretty much clear in the name - Poster, ID , Info or genre of the Movie!
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

# Test run 
print (get_movie_genres_tmdb("The Matrix"))

# To check what info can be capture
info=get_movie_info_tmdb("The Matrix")
print ('All the Movie information from TMDB gets stored in a dictionary with the following keys for easy access -')
info.keys()

all_movies=tmdb.Movies()
top_movies=all_movies.popular()
# This is a dictionary, and to access results we use the key 'results' which returns info on 10000 movies
len(top_movies['results'])
top10000_movs=top_movies['results']

# To print the top 10,000 popular movie , api capicity is 500 page which is 10,000 movie
all_movies=tmdb.Movies()
top10000_movies=[]
print('Pulling movie list, Please wait...')
for i in range(1,501):
    if i%15==0:
        time.sleep(7)
    movies_on_this_page=all_movies.popular(page=i)['results']
    top10000_movies.extend(movies_on_this_page)
len(top10000_movies)
f3=open('movie_list_top_10K.pckl','wb')
pickle.dump(top10000_movies,f3)
f3.close()
print('Done!')

# To check the search results
f3=open('movie_list_top_10K.pckl','rb')
top1000_movies=pickle.load(f3)
f3.close()
# Now we got the top 10000 movie by popularity
df = pd.read_pickle('movie_list_top_10K.pckl')
print(df)

# Based on 'All the Movie information from TMDB gets stored in a dictionary with the following keys for easy access -' we can modify our search result
columns = ['film', 'revenue', 'budget', 'release_date','genres','production_companies','original_language','adult','runtime','tagline','vote_average','vote_count','popularity']
film_popular_df = pd.DataFrame(columns=columns)

for film in top10000_movies:
    # print(film['title'])

    film_popular = requests.get('https://api.themoviedb.org/3/movie/'+ str(film['id']) +'?api_key='+ api_key+'&language=en-US')
    film_popular = film_popular.json()
    film_popular_df.loc[len(film_popular_df)]=[film['title'],film_popular['revenue'],(film_popular['budget']),film_popular['release_date'],film_popular['genres'],film_popular['production_companies'],film_popular['original_language'],film_popular['adult'],film_popular['runtime'],film_popular['tagline'],film_popular['vote_average'],film_popular['vote_count'],film_popular['popularity']]
    
film_popular_df.head()    

#df save to csv file 
film_popular_df.to_csv('movie_10K.csv')

# Based on 'All the Movie information from TMDB gets stored in a dictionary with the following keys for easy access -' we can modify our search result
columns = ['film', 'keywords'] ## we can also search the Keywords , basically we can change ever seach targe as long as we have the link for the search
film_popular_df = pd.DataFrame(columns=columns)

for film in top10000_movies:
    # print(film['title'])

    film_popular = requests.get('https://api.themoviedb.org/3/movie/'+ str(film['id']) +'/keywords'+'?api_key='+ api_key)
    film_popular = film_popular.json()
    film_popular_df.loc[len(film_popular_df)]=[film['title'],film_popular['keywords']]
    
film_popular_df.head(80)    
