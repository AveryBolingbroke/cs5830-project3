# %%
from numpy.core.arrayprint import array2string
import pandas as pd
import numpy as np
from twython import Twython
import matplotlib.pyplot as plt
import json
import seaborn as sns

# -- README --
#  Run the following cells in order and then a dataframe will be produced.
#  The dataframe has the DeckName, the Price, the Colors, the Format,
#  and DeckData which is a nested dataframe containing cards and their counts.  
#
#  After you run a new format, you can add it to the running total dataframe
#  by running the last cell labelled RUNNING TOTAL.
#  
#  When you're ready to start, run this cell first, and only once. On subsequent 
#  runs start in the cell below this, titled SUBSEQUENT RUNS. 
#  Change the 'url' variable to switch which page it draws data from.

# If you get tired of clicking each cell, go down to RUNNING TOTAL
# and use jupyter's 'Run above' option. THIS WILL ERASE ANY DATA STORED IN TOTAL.


import pandas as pd
d = {'DeckName':[], 'Price':[], 'Colors':[], 'Format': []}

total = pd.DataFrame(data=d)

#%%
# SUBSEQUENT RUNS
import requests

domain = "https://www.mtggoldfish.com"

# THIS URL IS THE PAGE TO DRAW TABLE DATA FROM
url ="https://www.mtggoldfish.com/metagame/standard#paper"

# get the format name automatically
formatName=url[len("https://www.mtggoldfish.com/metagame/"):-len("#paper")].capitalize()

html = requests.get(url)

#%%
from bs4 import BeautifulSoup

# Build a tree, or nested data structure, from the webpage
soup = BeautifulSoup(html.text, 'html5lib')

# Extract the legacy table of decks from the page
legacydecks = soup.find(id='metagame-decks-container')

# Extract the budge table of decks from the page
budgetdecks = soup.find('div', {'class':'budget-decks-container'})

#%%
# Get deck names (and the urls for later)
decknames = []
deckformat = []
deckurls = []

legacynames = legacydecks.find_all('span',{'class':"deck-price-paper"})
for deck in legacynames:
    thisname = str(deck.a.contents[0])
    decknames.append(thisname)
    print(thisname)
    deckformat.append(formatName)

    thisurl = domain + str(deck.a['href'])
    deckurls.append(thisurl)

budgetnames = budgetdecks.find_all('span',{'class':'deck-price-paper'})
for deck in budgetnames:
    thisname = str(deck.a.contents[0])
    decknames.append(thisname)
    print(thisname)
    deckformat.append(formatName+' Budget')

    thisurl = domain + str(deck.a['href'])
    deckurls.append(thisurl)

#%%
# Get deck tabletop prices
prices = []

legacyprices = legacydecks.find_all('div',{'class':'archetype-tile-statistic-value'})

# Note that there are three statistic values for each deck: META% + extra, cost, and tix.
# Thus, we need to only take every third value, starting at the second value
i = 0
for price in legacyprices:
    if i % 3 == 1:
        thisprice = float(str(price.contents[0].replace('$','').replace(',','').strip()))
        prices.append(thisprice)
        print(thisprice)
    i+=1
budgetprices=budgetdecks.find_all('div',{'class':'archetype-tile-statistic-value'})
# Note that budget prices only have two stats: cost and tix. Thus, take every other.
i = 0
for price in budgetprices:
    if i % 2 == 0:
        thisprice = float(str(price.contents[0].replace('$','').replace(',','').strip()))
        prices.append(thisprice)
        print(thisprice)
    i+=1

#%%
# Get deck colors
colors = []

legacycolors = legacydecks.find_all('span', {'class':'manacost'})
budgetcolors = budgetdecks.find_all('span', {'class':'manacost'})
for color in legacycolors+budgetcolors:
    thiscolor = color['aria-label'][8:] #after 'colors: '
    colors.append(str(thiscolor.split(' ')))
    print(thiscolor) 

# %%
# Go fetch deck data for each deck
deckdata = []
# for url in deckurls:
for url in deckurls:
    # Get the deck page and soupify it
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html5lib')
    # Get the cards and their counts
    counts = []
    names = []

    table = soup.find('table', {'class':'deck-view-deck-table'})
    for row in table.tbody.find_all('tr'):
        if row.get('class') == None: #skip headers
            cells = row.find_all('td')
            # The count and name are in the first and second cells, respectively
            count = int(str(cells[0].contents[0])) #NavigableString to String to Int
            name = str(cells[1].a.contents[0])
            try:
                index = names.index(name) # throws an error if the name doesn't already exist
                counts[index]+=count
            except:
                counts.append(count)
                names.append(name)
            

    # Create a deck dataframe from the counts, and append it to the deckdata list
    thisdeckdata = pd.DataFrame(data = {'Name': names, 'Count':counts})
    deckdata.append(thisdeckdata)
    print(thisdeckdata.head())


#%%
# Now put it all into a pandas dataframe
d = {'DeckName':decknames, 'Price':prices, 'Colors':colors, 'Format': deckformat, 'DeckData': deckdata}
df = pd.DataFrame(data=d)
df.head(100)

#%%
# RUNNING TOTAL

total = pd.concat([total, df])
print(total.head())



#%%


# ---> CAN WE DELETE THE REST OF THIS CODE? <--- #



#%%
apiKey = 'YkB57idqRrnYd1MEUN8rYRrC9'
apiSecretKey = 'QqvIMZuuEXPnl3V0zu0VCnXuZw0EFc3fwpYPymDZwWEd90Xwxv'
bearerToken = 'AAAAAAAAAAAAAAAAAAAAAP%2BfMwEAAAAA%2BEZ9mF3Lov%2B3b9Tr3GmVGoUa99g%3D7EsosotTTXgxzIL5TgjNRvrkKkijM4160R3juNPH0fXtnSvNcY'

twitter = Twython(app_key=apiKey, app_secret=apiSecretKey)

# search = twitter.search("#BlackLivesMatter")

# %%
statuses = twitter.search(q='crypto OR cryptocurrency OR btc, -winner, -giveaway since:2021-02-13', tweet_mode='extended')['statuses']
for status in statuses:
    #  print(status['user']['screen_name'])
    #  print(status['created_at'])
    if 'retweeted_status' in status:
        # print(status["retweeted_status"]['full_text'])
        status['full_text'] = status["retweeted_status"]['full_text']
# else:
#     print(status['full_text'])
print()

#%%
# Follow the Twitter paging process to get more than 100 tweets:
statuses = []
MAX_ATTEMPTS = 20
COUNT_OF_TWEETS_TO_BE_FETCHED = 500
queryText = "crypto OR cryptocurrency OR btc, -winner, -giveaway, since:2021-02-13"

for i in range(0,MAX_ATTEMPTS):

    # if(COUNT_OF_TWEETS_TO_BE_FETCHED < len(tweets)):
        # break # we got 500 tweets... !!

    #----------------------------------------------------------------#
    # STEP 1: Query Twitter                                          #
    # STEP 2: Save the returned tweets                               #
    # STEP 3: Get the next max_id                                    #
    #----------------------------------------------------------------#

    # STEP 1: Query Twitter
    if(0 == i):
        # Query twitter for data. 
        results = twitter.search(q=queryText,count='100', tweet_mode='extended')
    else:
        # After the first call we should have max_id from result of previous call. Pass it in query.
        results = twitter.search(q=queryText,include_entities='true', tweet_mode='extended',max_id=next_max_id)

    # STEP 2: Save the returned tweets
    for result in results['statuses']:
        # tweet_text = result['text']
        # tweets.append(tweet_text)
        if 'retweeted_status' in result:
            result['full_text'] = result["retweeted_status"]['full_text']
        statuses.append(result)


    # STEP 3: Get the next max_id
    try:
        # Parse the data returned to get max_id to be passed in consequent call.
        next_results_url_params = results['search_metadata']['next_results']
        next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
    except:
        # No more next pages
        break


#%%
texts = [status['full_text'] for status in statuses]

# Create a dataframe with five columns: bitcoin, dogecoin, ethereum, litecoin, binance
bitcoin = [text.lower().count('bitcoin') for text in texts]
dogecoin = [text.lower().count('doge') for text in texts]
ethereum = [text.lower().count('ethereum') for text in texts]
litecoin = [text.lower().count('litecoin') for text in texts]
binance = [text.lower().count('binance') for text in texts]
d = {'bitcoin':bitcoin, 'dogecoin':dogecoin, 'ethereum':ethereum, 'litecoin':litecoin, 'binance':binance}
df = pd.DataFrame(data=d)

# Count the occurences of each word, switch the axes
df = df.aggregate(['sum']).transpose()
df.head()
# This graph is meaningless
sns.barplot(y='sum', x=['bitcoin','dogecoin','ethereum','litecoin','binance'],data=df)

# %%
