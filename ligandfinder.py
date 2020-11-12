import chemdataextractor as cde
from chemdataextractor import Document
import pandas as pd
import chemicalfilters as cf
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
						if chemical.text not in found_chems and chemical.text not in cf.element_filter:
							found_chems.append((chemical.text,index)) #'''add ligand names to chem_records_df'''
	return found_chems

#'''return chem_records_df'''
