# %%
from numpy.core.arrayprint import array2string
import pandas as pd
import numpy as np
from twython import Twython
import matplotlib.pyplot as plt
import json
import seaborn as sns
import statistics

# -- README --
#  Run this cell and then a dataframe will be produced.
#  The dataframe has the DeckName, the Price, the Colors, the Format,
#  and DeckData which is a nested dataframe containing cards and their counts.
#  (DeckData does not print pretty :[ )  
#
#  Add the links to each format in the urls list below, and then run the cell!
#  The output dataframe is stored in the variable 'total'. 

# v CHANGE ME v
urls =[
    # "https://www.mtggoldfish.com/metagame/standard#paper",
    "https://www.mtggoldfish.com/metagame/pioneer#paper",
    #"https://www.mtggoldfish.com/metagame/modern#paper",
    # "https://www.mtggoldfish.com/metagame/legacy#paper",
    # "https://www.mtggoldfish.com/metagame/vintage#paper"
]

import pandas as pd
d = {'DeckName':[], 'Price':[], 'Colors':[], 'Format': []}

total = pd.DataFrame(data=d)

import requests

domain = "https://www.mtggoldfish.com"

# %%

for url in urls:

    # get the format name automatically
    formatName=url[len("https://www.mtggoldfish.com/metagame/"):-len("#paper")].capitalize()

    html = requests.get(url)

    from bs4 import BeautifulSoup

    # Build a tree, or nested data structure, from the webpage
    soup = BeautifulSoup(html.text, 'html5lib')

    # Extract the legacy table of decks from the page
    legacydecks = soup.find(id='metagame-decks-container')

    # Extract the budge table of decks from the page
    budgetdecks = soup.find('div', {'class':'budget-decks-container'})

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
    # Get deck colors
    colors = []

    legacycolors = legacydecks.find_all('span', {'class':'manacost'})
    budgetcolors = budgetdecks.find_all('span', {'class':'manacost'})
    for color in legacycolors+budgetcolors:
        thiscolor = color['aria-label'][8:] #after 'colors: '
        colors.append(str(thiscolor.split(' ')))
        # if thiscolor
        print(thiscolor)
    


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
        # print(thisdeckdata.head())

    # Now put it all into a pandas dataframe
    d = {'DeckName':decknames, 'Price':prices, 'Colors':colors, 'Format': deckformat} #, 'DeckData': deckdata}
    df = pd.DataFrame(data=d)
    df.head(100)

    # RUNNING TOTAL
    total = pd.concat([total, df])

print(total.head())
print(total.head(100))


# %%
standardPrice = total[total.Format == 'Standard']
pioneerPrice = total[total.Format == 'Pioneer']
modernPrice = total[total.Format == 'Modern']
legacyPrice = total[total.Format == 'Legacy']


# %%
priceByDeck = sns.scatterplot(y=colors, x=prices)
priceByDeck.set_title('Prices by Deck Color in order of % Meta - ')
priceByDeck.set_ylabel('Color of Deck')
priceByDeck.set_xlabel('Price of Deck in $')
# priceByDeck.set_xlim(0,8000)
display(priceByDeck)

standardPriceMean = statistics.mean(prices)
standardPriceSTD = np.std(prices)

print("Mean = " + str(standardPriceMean))
# print("Average = " + standardPriceAverage)
print("STD = " + str(standardPriceSTD))


# %%


# %%
