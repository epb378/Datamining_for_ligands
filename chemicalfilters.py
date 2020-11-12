import mendeleev
elements=mendeleev.element(list(range(1,100)))
element_filter=[]
for i in range(0,99):
  element_filter.append(elements[i].name)
  element_filter.append(elements[i].name.lower())
  element_filter.append(elements[i].symbol)
  element_filter.append(elements[i].symbol.lower())
