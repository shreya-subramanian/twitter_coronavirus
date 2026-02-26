#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--output_path_country',required=True)
parser.add_argument('--output_path_lang',required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# load each of the input paths
total_country = defaultdict(lambda: Counter())
total_lang = defaultdict(lambda: Counter())
for path in args.input_paths:
    with open(path) as f:
        tmp = json.load(f)
        if path.endswith(".country_code"):
            for k in tmp:
                total_country[k] += tmp[k]
        else:
             for k in tmp:
                total_lang[k] += tmp[k]

# write the output path
with open(args.output_path_country,'w') as f:
    f.write(json.dumps(total_country))
# write the output path
with open(args.output_path_lang,'w') as f:
    f.write(json.dumps(total_lang))
