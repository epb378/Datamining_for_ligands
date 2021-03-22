from tqdm import tqdm
import json
import re
import ast
myfile=open('all_chems_and_doi.txt', 'r')
mybiglist = [line for line in myfile.readlines()]
chems=[]
meta=[]

for text in tqdm(mybiglist):
	res=re.findall(r"'(.*?)'", text)
	if res[0] not in chems:
		chems.append(res[0])
		try:
			meta.append(res[1])
		except:
			meta.append('?')
	else:
		ind=chems.index(res[0])
		try:
			meta[ind]=meta[ind]+'; '+res[1]
		except:
			meta[ind]=meta[ind]+'; ?'
		#print(res[0])
		#print(chems[ind], meta[ind])
		
chems_and_meta=list(zip(chems,meta))


with open('concatenate_chems_and_doi.txt', 'w') as filehandle:
    for listitem in chems_and_meta:
	    filehandle.write('%s\n' % str(listitem))

