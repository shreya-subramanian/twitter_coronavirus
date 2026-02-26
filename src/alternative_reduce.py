#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--hashes',nargs='+',required=True)
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
fm.fontManager.addfont('/home/shsubramanian/.fonts/NanumGothic-Regular.ttf')
plt.rcParams['font.family'] = 'NanumGothic'
from collections import Counter,defaultdict

#for each input file we open search for a hash and add the sum of the hash in that file to the dictionary that stores {hash:{date:sum}} withe the date of that file.

hash_dict={}
for hashtag in args.hashes:
    hash_dict[hashtag]={}
for path in args.input_paths:
    if not (path.endswith(".country_code")):
        continue
    filename = os.path.basename(path)
    date = filename.replace('geoTwitter', '').replace('.country_code','')
    with open(path) as f:
        temp=json.load(f)
    for hashtag in args.hashes:
        if hashtag in temp:
            hash_dict[hashtag][date]=sum(temp[hashtag].values())
        else:
            hash_dict[hashtag][date]=0
for hashtag,counts in hash_dict.items():
    dates=sorted(counts.keys())
    values=[counts[d] for d in dates]
    plt.plot(dates,values,label=hashtag)
plt.xlabel('date')
plt.ylabel('total number of tweets')
plt.title('line graph showing tweet trend per hashtag per day')
plt.legend()
step=len(dates)//12
plt.xticks(range(0, len(dates), step), dates[::step], rotation=45)
plt.savefig('alternative_reduce.png',bbox_inches='tight')
