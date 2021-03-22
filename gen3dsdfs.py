import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import PandasTools
from tqdm import tqdm


def gen3dsdf(mol):
	m3 = Chem.AddHs(mol)
	AllChem.EmbedMolecule(m3,randomSeed=0xf00d)
	return Chem.MolToMolBlock(m3)
	
dec18=open('SMILESlist_december18_finished.txt', 'r')
dec18_list = [line for line in dec18.readlines()]
dec19=open('SMILESlist_december19.txt', 'r')
dec19_list = [line for line in dec19.readlines()]
dec22=open('SMILESlist_december22.txt', 'r')
dec22_list = [line for line in dec22.readlines()]
all_lists=dec18_list+dec19_list+dec22_list
unique_list=[]
for x in all_lists:
	if x in unique_list:
		pass
	else:
		unique_list.append(x)
mol_list=[]
sdf_list=[]
smiles_list=[]
for x in tqdm(unique_list):
	try:
		#print(x)
		mol=Chem.MolFromSmiles(x)
		sdf=gen3dsdf(mol)
		#print(sdf)
		mol_list.append(mol)
		sdf_list.append(sdf)
		smiles_list.append(x)
	except:
		pass
		
with open('sdf_list.txt', 'w') as f:
	for x in unique_list:
		f.write(x+'\n')
		
with open('mysdfs_only.txt', 'w') as f:
	for i in tqdm(range(0,len(sdf_list))):
		f.write(sdf_list[i] + '\n $$$$ \n')
		
w = Chem.SDWriter('mysdfs_written.sdf')
for x in tqdm(mol_list):
	w.write(x)
