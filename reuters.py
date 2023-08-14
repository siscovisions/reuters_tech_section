# Import the necessary modules for scraping and pandas for our dataframe
from bs4 import BeautifulSoup
import requests
import pandas as pd



# Assign the headers

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://google.com',
        'DNT': '1',
    }

# Assign the home URL

url = 'https://www.reuters.com'

# Scrape the Reuters home tech section

r = requests.get('https://www.reuters.com/technology', headers=HEADERS)
soup = BeautifulSoup(r.content, 'html.parser')
articles = soup.find_all('h3', class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P')

# Loop over the article links to pull the direct article links

news_links = []
for x in articles:
    for link in x.find_all('a', href=True):
        news_links.append(url + link['href'])

# Another for loop to inspecgt each artile, pulling the headlines and dates posted

story_links = []
for story in news_links:
    r = requests.get(story, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'lxml')
    headline = soup.find('h1', class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_3__1kDhc heading__base__2T28j heading__heading_3__3aL54 article-header__title__3Y2hh').text
    date_posted = soup.find('span', class_='date-line__date__23Ge-').text

# Assign our column labels and their values to a dictionary that we will use to build or dataframe

    article_links = {
        'headline': headline,
        'date_posted': date_posted,
        'link': story
    }

    story_links.append(article_links)

# Finally, save the results to our CSV file

df = pd.DataFrame(story_links)
df.to_csv('reuters_technology.csv', index=False)