# %%
from numpy.core.arrayprint import array2string
import pandas as pd
import numpy as np
from twython import Twython
import matplotlib.pyplot as plt
import json

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
texts = [status['full_text'] for status in statuses]

# Create a dataframe with three columns: trump, pelosi, and mcconnell
bitcoin = [text.lower().count('bitcoin') for text in texts]
dogecoin = [text.lower().count('doge') for text in texts]
ethereum = [text.lower().count('ethereum') for text in texts]
litecoin = [text.lower().count('litecoin') for text in texts]
binance = [text.lower().count('binance') for text in texts]
d = {'bitcoin':bitcoin, 'dogecoin':dogecoin, 'ethereum':ethereum, 'litecoin':litecoin, 'binance':binance}
df = pd.DataFrame(data=d)

df.head()

# %%
# trying out MTG to see what I can do

from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
import pandas as pd
import numpy as np
from twython import Twython
import matplotlib.pyplot as plt

# untap = Card.where(text='untap step').all()
cards = Card.all()
# firstMain = Card.where(text='first main').all()
# combat = Card.where(text='combat').all()
# secondMain = Card.where(text='second main').all()
# endStep = Card.where(text='end step').all()
# cleanUp = Card.where(text='cleanup').all()

cardsWithUpkeep = ['upkeep' in card.text for card in cards]

for card in cardsWithUpkeep:
    print(card.name)

# %%
rows = []
columns = []

upkeepCount = 0

for row in upkeep:
    for column in row:
        value = all(column)
        columns.append(value)
        upkeepCount += 1
    columns = []
    rows.append(columns)

titles = ['untap', 'upkeep', 'firstMain',
    'combat', 'secondMain', 'endStep', 'cleanUp']

df = pd.DataFrame(data=rows, columns=titles)
# df = df.iloc[:-3]
display(df.head())
display(df.tail())

# print(untap)
print(upkeepCount)
# print(firstMain)
# print(combat)
# print(secondMain)
# print(endStep)
# print(cleanUp)

# %%