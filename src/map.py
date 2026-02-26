#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--output_folder',default='outputs')
args = parser.parse_args()

# imports
import os
import zipfile
import datetime 
import json
from collections import Counter,defaultdict

# load keywords
hashtags = [
    '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
    ]

# initialize counters
counter_lang = defaultdict(lambda: Counter())
country_code_counter=defaultdict(lambda: Counter())
# open the zipfile
with zipfile.ZipFile(args.input_path) as archive:

    # loop over every file within the zip file
    for i,filename in enumerate(archive.namelist()):
        print(datetime.datetime.now(),args.input_path,filename)

        # open the inner file
        with archive.open(filename) as f:

            # loop over each line in the inner file
            for line in f:

                # load the tweet as a python dictionary
                tweet = json.loads(line)

                # convert text to lower case
                text = tweet['text'].lower()

                # search hashtags
                for hashtag in hashtags:
                    lang = tweet['lang']
                    if tweet.get('place') is not None and tweet['place'].get('country_code') is not None:
                        country_code=tweet['place']['country_code']
                    else:
                        country_code="overseas"

                    if tweet['place'] is None or country_code is None:
                        country_code="Overseas/space station"
                    if hashtag in text:
                        counter_lang[hashtag][lang] += 1
                        country_code_counter[hashtag][country_code]+=1
                counter_lang['_all'][lang] += 1
                country_code_counter['_all'][country_code]+=1


# open the outputfile
try:
    os.makedirs(args.output_folder)
except FileExistsError:
    pass
output_path_base = os.path.join(args.output_folder,os.path.basename(args.input_path))

output_path_lang = output_path_base+'.lang'
output_path_country_code=output_path_base+'.country_code'
print('saving',output_path_lang,output_path_country_code)
with open(output_path_lang,'w') as f:
    f.write(json.dumps(counter_lang))
with open(output_path_country_code,'w') as f:
    f.write(json.dumps(country_code_counter))

