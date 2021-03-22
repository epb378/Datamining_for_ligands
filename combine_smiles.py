dec18=open('SMILESlist_december7.txt', 'r')
dec18_list = [line for line in dec18.readlines()]
dec19=open('SMILESlist_december15.txt', 'r')
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

with open('unique_SMILES.txt', 'w') as f:
	for x in unique_list:
		f.write(x+'\n')
