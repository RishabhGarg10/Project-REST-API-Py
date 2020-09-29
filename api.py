import requests_with_caching
import json

def get_movies_from_tastedive(title):
    url = 'https://tastedive.com/api/similar'
    param = {}
    param['q']= title
    param['type']= 'movies'
    param['limit']= 5
    
    this_page_cache = requests_with_caching.get(url, params=param)
    return json.loads(this_page_cache.text)

def extract_movie_titles(movie):
    return ([i['Name'] for i in movie['Similar']['Results']])

def get_related_titles(movie_titles):
    listed = []
    for movie in movie_titles:
        listed.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(listed))
def get_movie_data(movie_search):
    baseURL1 = "http://www.omdbapi.com/"
    parameter1 = dict()
    parameter1['t'] = movie_search
    parameter1['r'] = 'json'
    info_movie = requests_with_caching.get(baseURL1,params = parameter1)
    return json.loads(info_movie.text)

def get_movie_rating(result):
    ranking = result["Ratings"]
    for result_item in ranking:
        if result_item['Source'] == 'Rotten Tomatoes':
            return int(result_item['Value'][:-1])
    return 0

def get_sorted_recommendations(movie_title):
    new_movielist = get_related_titles(movie_title)
    sort1 = dict()
    for i in new_movielist:
        ratings = get_movie_rating(get_movie_data(i))
        sort1[i] = ratings
    print(sort1)    
    return [i[0] for i in sorted(sort1.items(), key=lambda item: (item[1], item[0]), reverse=True)]
    
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
