from tqdm import tqdm
import time
import urllib
import urllib.request
import json
import ast

myfile = open('/home/littleneddyb/scrapextract/ned_scrape/semi-hand-scrape/shorter_CIDSlist_december22.txt', 'r')
#mystring=myfile.read()
#myresult = [line for line in myfile.readlines()]
SMILES_url_head='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/'
SMILES_url_tail='/property/CanonicalSMILES/txt'
#raw_cids_list=mystring.splitlines()
cids_list=[]
j=0
wait_time=1
for line in tqdm(myfile):
	try:
		cids_list.append(line)#ast.literal_eval(line)['IdentifierList']['CID'][0])
	except:
		j+=1
print(str(j) + ' entries in the CIDS list could not be converted')

SMILES_list=[]
i=0
for line in tqdm(cids_list) :
	#print(item)
	bare_cid=line#item['IdentifierList']['CID'][0]
	try:
		print(bare_cid[:-2])
		SMILES_url=SMILES_url_head+str(bare_cid[:-2])+SMILES_url_tail
		with urllib.request.urlopen(SMILES_url) as response:
			data=response.read().decode("utf-8")
		SMILES_list.append(data)
		print(data)
		time.sleep(wait_time)
		i+=1
		if i%50==0:
			with open('SMILESlist_december22.txt', 'w') as filehandle:
				for listitem in SMILES_list:
					filehandle.write('%s\n' % str(listitem))
	except:
		print(bare_cid)

with open('SMILESlist_december22.txt', 'w') as filehandle:
    for listitem in SMILES_list:
	    filehandle.write('%s\n' % str(listitem))
