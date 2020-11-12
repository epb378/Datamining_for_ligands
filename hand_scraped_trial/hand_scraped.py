import ligandfinder as lf
import chemicalfilters as cf
import os
from tqdm import tqdm
import json
import pandas as pd
import chemdataextractor

all_chems=[]
ident=0
for filename in tqdm(os.listdir('hand_scraped_reviews')):
	if filename.endswith(".html"):
		path=os.path.join('hand_scraped_reviews/', filename) 
		found_chems=lf.ligandfinder(path,index=ident)
		all_chems.append((found_chems))
		ident+=1
with open('hand_scraped_chems.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(all_chems, filehandle)
