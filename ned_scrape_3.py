'''!pip install chemdataextractor
!pip install mendeleev
!pip install kora -q
!cde data download
!pip install json2html
!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /us
'''

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver

import zipfile
import urllib.request
import json
from tqdm import tqdm
import urllib
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from chemdataextractor.scrape import Selector
from chemdataextractor.scrape.pub.rsc import RscHtmlDocument
#import kora.install.rdkit
import subprocess
import pandas as pd
import rdkit
#from rdkit import Chem
#from rdkit.Chem import AllChem
#from rdkit.Chem import PandasTools
import requests, zipfile, io
#The copied URL goes here ->
r = requests.get( 'https://git.durrantlab.pitt.edu/jdurrant/dimorphite_dl/-/archive/1.2.4/dimorphite_dl-1.2.4.zip' ) 
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
smile='O=C(NCCS)c1ccccc1​'
min_ph=str(4.4)
max_ph=str(8.4)
chemsandmeta=[]

import os
directory = r'/content/'

def article_to_meta(html_file):
  column_names = ["title", "doi", "firstauthor","lastauthor","year","journal"]
  htmlstring = open(html_file).read()
  try:
    sel = Selector.from_text(htmlstring)
    scrape = RscHtmlDocument(sel)
  except: pass
  try:
    title=scrape.title 
  except:
    title='unknown title'
  try:
    doi=scrape.doi 
  except:
    doi='unknown doi'
  try:
    firstauthor=scrape.authors[0]
  except:
    firstauthor='unknown author'
  try: 
    lastauthor=scrape.authors[-1]  
  except:
    lastauthor='unknown author'
  try:
    published_date=scrape.published_date.strftime("%Y") 
  except:
    published_date='unknown date'
  try:
    journal=scrape.journal 
  except:
    journal='unknown journal'
  #print([title,doi,firstauthor,lastauthor,published_date,journal])
  data={'title': title, 'doi': doi, 'firstauthor': firstauthor, 'lastauthor': lastauthor, 'published_date': published_date, 'journal': journal} 
  return data

def article_to_sdfs(html_file, index=0, min_pH=4.4, max_pH=8.4,debug=False):

  chems_list=ligandfinder(html_file,index) #scrape HTML for ligands/surfactant/coordinating solvents etc.
  meta_data=article_to_meta(html_file)
  SMILES_list=chem_names_to_smiles(chems_list) #use pubchem to search for SMILES from chem names (via CIDS)
  extra_smiles=[]
  for smile in SMILES_list:
    if debug==True:
      print(smile)
    extra_smiles= extra_smiles+dimophite_run(smile, min_pH, max_pH) #See if there are any other charged states in the pH range of interest
  SMILES_list=extra_smiles
  #mols = [Chem.MolFromSmiles(smi) for smi in SMILES_list] # use RDkit to convert smiles to mol format
  mols_sdfs=[]
  for smile in SMILES_list:
    meta=meta_data
    try: 
      mol = rdkit.Chem.MolFromSmiles(smile)
      mols_sdfs.append((meta,gen3Dsdf(mol))) #try to turn these mols formats into SDF docs
    except:
      pass  

  return mols_sdfs

def get_articles(page_html, driver):
  search_results=re.findall(r'btn btn--tiny(.*?)onclick', page_html)
  ind=0
  for href in search_results:
    article_url='https://pubs.rsc.org'+href[8:-2]
    print(article_url)
    time.sleep(10)
    response=urllib.request.urlopen(article_url)
    html_string = response.read().decode('utf-8')
    Html_file= open('tempfile'+str(ind)+'.html',"w")
    Html_file.write(html_string[38:])#clip header
    Html_file.close()
    ind+=1

import requests, zipfile, io
r = requests.get( 'https://git.durrantlab.pitt.edu/jdurrant/dimorphite_dl/-/archive/1.2.4/dimorphite_dl-1.2.4.zip' ) 
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
import json2html
import mendeleev
import subprocess
elements=mendeleev.element(list(range(1,100)))
element_filter=[]
for i in range(0,99):
  element_filter.append(elements[i].name)
  element_filter.append(elements[i].name.lower())
  element_filter.append(elements[i].symbol)
  element_filter.append(elements[i].symbol.lower())

def dimophite_run(smile, min_ph, max_ph):
  process = subprocess.run(['python','dimorphite_dl-1.2.4/dimorphite_dl.py', '--smiles', smile, '--min_ph', str(min_ph), '--max_ph', str(max_ph), '--silent'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
  output = process.stdout
  output_list=output.split(sep='\t\n')
  output_list = list(filter(None, output_list))
  return output_list

def gen3Dsdf(mol):
  m3 = rdkit.Chem.AddHs(mol)
  rdkit.AllChem.EmbedMolecule(m3,randomSeed=0xf00d)
  return rdkit.Chem.MolToMolBlock(m3)


def chem_names_to_smiles(chems_list,wait_time=1):
  cids_list=[]
  SMILES_list=[]
  cids_url_head='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
  cids_url_tail='/cids/json?name_type=word' #THIS IS FOR PARTIAL MATCHES_returns a list of CIDS
  #info about this here https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest-tutorial
  SMILES_url_head='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/'
  SMILES_url_tail='/property/CanonicalSMILES/txt'
    ##chemical name to cids to smiles
  for i in range(0,len(chems_list)):
    chem_url=cids_url_head+chems_list[i][0]+cids_url_tail
    try:
      with urllib.request.urlopen(chem_url) as response:
        data=json.load(response)
      cids_list.append(data)
      bare_cid=cids_list[i]['IdentifierList']['CID'][0]
      SMILES_url=SMILES_url_head+str(bare_cid)+SMILES_url_tail
      time.sleep(wait_time)
      try:
        with urllib.request.urlopen(SMILES_url) as response:
          data=response.read().decode("utf-8")
        SMILES_list.append(data)
      except:
        SMILES_list.append('')
      time.sleep(wait_time)
    except:
      time.sleep(wait_time)
      cids_list.append('')

    return SMILES_list

import chemdataextractor as cde
from chemdataextractor import Document
import pandas as pd
from chemdataextractor.nlp.tokenize import ChemSentenceTokenizer 

def ligandfinder(docpath,index): #update to handle list of synonyms
	found_chems=[]
#''' import document'''
	f=open(docpath, 'rb')
	doc=Document.from_file(f)
	no_elements=len(doc.elements)
	for i in range(0,no_elements):
		check=False
		if isinstance(doc.elements[i], cde.doc.text.Paragraph): #will do tables later
			for sentence in doc.elements[i].raw_sentences:
#'''scrape for sentences/paragraphs with ligand synonyms'''
				if 'ligand' or 'ligands' or 'coordinating' or 'surfactant' or 'surfactants' in cwt.tokenize(sentence):
					check=True
			if check:
				if not doc.elements[i].cems == True:
#'''scrape those sentences/paragraphs for ligand names'''
					for chemical in doc.elements[i].cems:
						if chemical.text not in found_chems and chemical.text not in element_filter:
							found_chems.append((chemical.text,index)) #'''add ligand names to chem_records_df'''
	return found_chems

chemsandmeta=[]

import os
def scrape_rsc_search(search_term):

  chemsandmeta=[]
  url='https://pubs.rsc.org/en/results?searchtext='+search_term
  directory = r'/home/littleneddyb/scrapextract/ned_scrape'
  for pages in range(0,20):
    #open page
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.get(url)
    #open page
    for i in range(0,pages):
        time.sleep(4)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/div/div[1]/section[2]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/a')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elem=driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/section[2]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/a')
        elem.click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tabAll']/div[2]/div[2]/div/div[2]/a[2]")))

    page_html=driver.page_source

      #print(driver.page_source)

    article_chems=get_articles(page_html,driver)
    #get html files from page
    
    #get chemicals from each file
    for filename in tqdm(os.listdir(directory)):
      if filename[-4:]=='html':
        if chemsandmeta==[]:
          chemsandmeta=article_to_sdfs(filename)
        else:
          chemsandmeta.append(article_to_sdfs(filename) )
      with open('listfile.txt', 'w') as filehandle:
        for listitem in chemsandmeta:
          filehandle.write('%s\n' % str(listitem))
    #get sdf from each chemical's enumerated smiles
    #go to next page
    driver.close()
    driver.quit()
    del driver

page_htmls=[]
url='https://pubs.rsc.org/en/results?searchtext=nanoparticle'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=chrome_options)
driver.get(url)
for pages in range(0,120):
  #open page
  print(pages)

  time.sleep(4)
  page_htmls.append(driver.page_source)
  search_results=re.findall(r'btn btn--tiny(.*?)onclick', driver.page_source)
  print(search_results[0])
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[2]/div/div[1]/section[2]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/a/img')))
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  elem=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div/div[1]/section[2]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/a/img')
  elem.click()


print('length of list is: '+str(len(page_htmls)))

with open('shortpagehtmlslistfile_December7.txt', 'w') as filehandle:
  for listitem in page_htmls:
    filehandle.write('%s\n' % str(listitem))

def list_article_htmls(list_of_pages):

  list_of_urls=[]
  for page in tqdm(list_of_pages):
    search_results=re.findall(r'btn btn--tiny(.*?)onclick', page)
    for href in search_results:
      article_url='https://pubs.rsc.org'+href[8:-2]
      print(article_url)
      list_of_urls.append(article_url)
  return list_of_urls

list_of_urls=list_article_htmls(page_htmls)
#list_of_urls=list_of_urls[1500:]
chemsandmeta=[]
i=0
for link in tqdm(list_of_urls):
#for i in tqdm(range(1500,5200)):
    print(link)
    try:
	    time.sleep(10)
	    response=urllib.request.urlopen(link)
	    html_string = response.read().decode('utf-8')
	    Html_file= open('tempfileA.html',"w")
	    Html_file.write(html_string[38:])#clip header
	    Html_file.close()
	    #article_to_sdfs('tempfileA.html')
	    meta=article_to_meta('tempfileA.html')
	    print(meta)
	    ligands=ligandfinder('tempfileA.html', index=0)
	    print(ligands)
	    chemsandmeta.append((meta,ligands))
	    print(chemsandmeta)
    except:
        pass
    if i%50==0:
        with open('listfile_december7.txt', 'w') as filehandle:
            for listitem in chemsandmeta:
                filehandle.write('%s\n' % str(listitem))
    i+=1

with open('listfile_december7.txt', 'w') as filehandle:
  for listitem in chemsandmeta:
    filehandle.write('%s\n' % str(listitem))
