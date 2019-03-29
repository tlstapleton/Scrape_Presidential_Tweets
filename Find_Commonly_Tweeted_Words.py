
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')

## Create function to scroll through Twitter feed
def scroll_feed(browser):
        SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

## Function to scrape tweet text and tweet author into Pandas DataFrame
def scrapefeed(url):
    browser=webdriver.Chrome()
    browser.get(url)
    scroll_feed(browser)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    body = soup.find('body')
    feed = body.findAll('li', {'class':'stream-item'})
    print(len(feed))
    author=[]
    text=[]
    for tweet in feed:
        author.append(tweet.find('strong', {'class':'fullname'}).text)
        text.append(tweet.find('p', {'class':'tweet-text'}).text)
    data={'Author':author,'Text':text}
    feed_df=pd.DataFrame(data=data)
    browser.quit()
    return feed_df

## Function returns dictionary of 50 most frequent words and their counts
def author_frequent_words(df, author):
    author_tweets=df[df['Author']==author]
    author_words=[]
    stop_words=set(stopwords.words('english'))
    # stop_words.append('https')
    for index, row in author_tweets.iterrows():
        text_full=(re.sub('[^ a-zA-Z0-9]', '', row['Text']))
        text_tokens=word_tokenize(text_full)
    #     filtered_sentence=[w for w in text_tokens if not w in stop_words
        for w in text_tokens:
            if w.lower() not in stop_words:
                author_words.append(w)
    author_word_count = Counter(author_words).most_common(50)
    return(dict(author_word_count))



trump_df=scrapefeed('https://twitter.com/realDonaldTrump')
trumpwordcloud=WordCloud(width=900, height=500, background_color="white").generate_from_frequencies(author_frequent_words(trump_df, "Donald J. Trump"))
plt.imshow(trumpwordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Donald Trump Tweets", fontdict={'fontsize':20, 'color':'black', 'fontweight':'bold'}, pad=20)
# plt.show()
plt.savefig('Trump_Tweet_Words.png')

obama_df=scrapefeed('https://twitter.com/BarackObama')
obamawordcloud=WordCloud(width=900, height=500, background_color="white",colormap = "plasma").generate_from_frequencies(author_frequent_words(obama_df, "Barack Obama"))
plt.imshow(obamawordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Barack Obama Tweets", fontdict={'fontsize':20, 'color':'black', 'fontweight':'bold'}, pad=20)
# plt.show()
plt.savefig('Obama_Tweet_Words.png')
