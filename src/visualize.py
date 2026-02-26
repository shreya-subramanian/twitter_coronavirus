#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
fm.fontManager.addfont('/home/shsubramanian/.fonts/NanumGothic-Regular.ttf')
plt.rcParams['font.family'] = 'NanumGothic'
# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]),reverse=True)
new_items=items[:10]
x_axis=[]
y_axis=[]
for k,v in new_items[::-1]:
    x_axis.append(k)
    y_axis.append(v)
plt.bar(x_axis,y_axis)
plt.xlabel('Keys')
plt.ylabel('Counts')
plt.title('for the hashtag'+args.key)
plt.savefig(args.key.replace('#','')+'_'+ args.input_path+'.png', bbox_inches='tight')
