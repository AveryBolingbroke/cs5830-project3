# %%
from numpy.core.arrayprint import array2string
import pandas as pd
import numpy as np
from twython import Twython
import matplotlib.pyplot as plt
import json
import seaborn as sns

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