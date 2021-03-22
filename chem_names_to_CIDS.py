from tqdm import tqdm
import time
import urllib
import urllib.request
import json

url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/JSON'
url_head='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
url_tail='/cids/json?name_type=word' #THIS IS FOR PARTIAL MATCHES_returns a list of CIDS
#info about this here https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest-tutorial
#with urllib.request.urlopen(url) as response:
#  data = json.load(response)
wait_time=0.5
chems_list_canonical_smiles=[]
chems_list_isomeric_smiles=[]
cids_list=[]

myfile = open('/home/littleneddyb/scrapextract/ned_scrape/semi-hand-scrape/unique_chems_december22.txt', 'r')
mystring=myfile.read()
myresult = [line for line in myfile.readlines()]

chems=mystring.splitlines()
chems_list=[]

for x in chems:
  if x is not None:

    if x.lower() not in chems_list and " " not in x:
      chems_list.append(x.lower())

for i in tqdm(range(0,len(chems_list))):
  chem_url=url_head+chems_list[i]+url_tail

  if i%100==0:
    with open('shorter_CIDSlist_december22.txt', 'w') as filehandle:
      for listitem in cids_list:
        filehandle.write('%s\n' % str(listitem))
  try:
    with urllib.request.urlopen(chem_url) as response:
      data=json.load(response)
    cids_list.append(data['IdentifierList']['CID'][0])
    if i%100==0:
      print(data)
    #chems_list_canonical_smiles.append(data['PC_Compounds'][0]['props'][18]['value']['sval'])
    #chems_list_isomeric_smiles.append(data['PC_Compounds'][0]['props'][18]['value']['sval'])
    time.sleep(wait_time)
  except:
    time.sleep(wait_time)
    cids_list.append('')
  i+=1
  
with open('shorter_CIDSlist_december22.txt', 'w') as filehandle:
	for listitem in cids_list:
		filehandle.write('%s\n' % str(listitem))
