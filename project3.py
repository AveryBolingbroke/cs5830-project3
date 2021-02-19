# %%
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
statuses = twitter.search(q='magic')['statuses']
for status in statuses:
     print(status['user']['screen_name'])
     print(status['created_at'])
if 'retweeted_status' in status:
    print(status["retweeted_status"]['full_text'])
if 'full_text' in status['retweeted_status']:
    status['full_text'] = status["retweeted_status"]['full_text']
else:
    print(status['full_text'])
    # print()


#%%
texts = [status['full_text'] for status in statuses]

# Create a dataframe with three columns: trump, pelosi, and mcconnell
uro = [text.lower().count('uro') for text in texts]
wildernessRec = [text.lower().count('wilderness') for text in texts]
oko = [text.lower().count('oko') for text in texts]
astrolabe = [text.lower().count('astrolabe') for text in texts]
lurrus = [text.lower().count('lurrus') for text in texts]
d = {'uro':uro, 'oko':oko, 'wildernessRec':wildernessRec, 'astrolabe':astrolabe, 'lurrus':lurrus}
df = pd.DataFrame(data=d)

df.head()

#%%
