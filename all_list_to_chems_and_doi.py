from tqdm import tqdm
import json
import re
import ast
myfile=open('all_list_december2020.txt', 'r')
mybiglist = [line for line in myfile.readlines()]
chems_and_meta=[]
for text in tqdm(mybiglist):
  try:
    list_results=re.findall(r'}(.*?)\n', text)
    doi_results=re.findall(r"'doi': '(.*?)',", text)
    res=ast.literal_eval(list_results[0][2:-1])
    for item in res:
      if (item[0],doi_results[0]) not in chems_and_meta:
        chems_and_meta.append((item[0],doi_results[0]))
      else:
        pass
  except:
    pass

with open('all_chems_and_doi.txt', 'w') as filehandle:
    for listitem in chems_and_meta:
	    filehandle.write('%s\n' % str(listitem))
