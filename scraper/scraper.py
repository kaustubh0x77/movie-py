from requests import get
from bs4 import BeautifulSoup as BS
import pandas as pd

class movies:
    names = []
    years = []
    genres = []
    actors = []
    number_movies = 0
    movie_list = ""

    def __init__(self, number_movies):
        self.number_movies = number_movies

    def connect(self):
        url = 'https://www.imdb.com/search/title?count={}&groups=top_1000&sort=num_votes'.format(self.number_movies)
        response = get(url)
        html_soup = BS(response.text, 'html.parser')
        return html_soup

    def fetch_data(self):
        movie_list = self.connect().find_all('div', class_='lister-item mode-advanced')
        for container in movie_list:
            name = container.h3.a.text
            movies.names.append(name)

            year = container.find('span', class_='lister-item-year text-muted unbold').text
            year = year.strip("()")
            movies.years.append(year)

            genre = container.find('div', class_='lister-item-content').find('p', class_='text-muted').find('span', class_='genre').text
            genre = genre.strip()
            movies.genres.append(genre)

            actor = ""
            for i in range(1, 5):
                actor += (container.find_all('p')[2].find_all('a')[i].text + ", ")
            movies.actors.append(actor)

mov = movies(1000)
mov.connect()
mov.fetch_data()

dataframe_test = pd.DataFrame({'movie': mov.names,
                       'year': mov.years,
                       'genre': mov.genres,
                       'cast': mov.actors})
print(dataframe_test.values)

dataframe_test.to_csv('dump.csv')


