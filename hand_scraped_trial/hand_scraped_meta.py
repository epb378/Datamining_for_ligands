import ligandfinder as lf
import chemicalfilters as cf
import os
from tqdm import tqdm
import json
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.scrape import Selector
from chemdataextractor.scrape.pub.rsc import RscHtmlDocument

column_names = ["id", "title", "doi", "firstauthor","lastauthor","year","journal"]
all_meta = []
ident=0
for filename in tqdm(os.listdir('hand_scraped_reviews')):
	if filename.endswith(".html"):
				
		path=os.path.join('hand_scraped_reviews/', filename) 
		htmlstring = open(path).read()
		sel = Selector.from_text(htmlstring)
		scrape = RscHtmlDocument(sel)
		title=scrape.title 
		doi=scrape.doi 
		firstauthor=scrape.authors[0] 
		lastauthor=scrape.authors[-1]  
		published_date=scrape.published_date.strftime("%Y") 
		journal=scrape.journal 
		
		#print([title,doi,firstauthor,lastauthor,published_date,journal])
		data={'id': ident, 'title': title, 'doi': doi, 'firstauthor': firstauthor, 'lastauthor': lastauthor, 'published_date': published_date, 'journal': journal}
		all_meta.append(data)
		#print(all_meta)
		ident+=1
all_meta_df=pd.DataFrame(all_meta)
all_meta_df.to_csv('meta.csv', index=False)
