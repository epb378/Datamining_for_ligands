from tqdm import tqdm
import time
import urllib
import urllib.request
import json
import re
import ast
url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/JSON'
url_head='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
url_tail='/cids/json?name_type=word' #THIS IS FOR PARTIAL MATCHES_returns a list of CIDS
#info about this here https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest-tutorial
#with urllib.request.urlopen(url) as response:
#  data = json.load(response)
wait_time=0.1
chems_list_canonical_smiles=[]
chems_list_isomeric_smiles=[]
cids_list=[]

myfile = open('/home/littleneddyb/scrapextract/ned_scrape/semi-hand-scrape/concatenate_chems_and_doi.txt', 'r')
mybiglist = [line for line in myfile.readlines()]


CIDS=[]
meta_list=[]
i=0
for item in tqdm(mybiglist):
	res=re.findall(r"'(.*?)'", item)
	chem_url=url_head+res[0]+url_tail
	try:
		with urllib.request.urlopen(chem_url) as response:
			data=json.load(response)
		CIDS.append(data['IdentifierList']['CID'][0])
		meta_list.append(res[1])
	except:
		pass
	time.sleep(wait_time)
	i+=1
	if 1%100==0:
		print(CIDS[-1],meta_list[-1])
		
CIDS_meta=list(zip(CIDS,meta_list))
with open('meta_CIDSlist.txt', 'w') as filehandle:
	for listitem in CIDS_meta:
		filehandle.write('%s\n' % str(listitem))
