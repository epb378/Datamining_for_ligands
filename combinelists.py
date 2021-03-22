dec18=open('listfile_december7.txt', 'r')
dec18_list = [line for line in dec18.readlines()]
dec19=open('listfile_december15.txt', 'r')
dec19_list = [line for line in dec19.readlines()]
dec22=open('listfile_december22.txt', 'r')
dec22_list = [line for line in dec22.readlines()]
all_lists=dec18_list+dec19_list+dec22_list

with open('all_list_december2020.txt', 'w') as filehandle:
    for listitem in all_lists:
	    filehandle.write('%s\n' % str(listitem))
