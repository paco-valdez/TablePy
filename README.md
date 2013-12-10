TablePy
===========
_____________
A Data Structure for Maintaing Tabular Data in Memory.
_____________

It was created as an exercise but it may be helpful to others, 
It's not recommended to use it in a production environment.
The table is implemented as a list of dicts, it also have value 
indexes for faster direct lookup for a row by column value.

To create a Table:
    
    from tablepy.table import Table
    table = Table(['ID','name'])
    table.append({'ID':2,'name':'a'})
    table.append({'ID':1,'name':'b'})
    print table
    
    
It supports len, iteration and indexing:

    print len(table), not table
    print iter(table)
    print table[0]
    
We can add a column with a constant value:

    table.addColumn('constant',3)
    print table
    
    
Also we can add a column with a interable arg (must be the same size as our table):
    
    table.addColumn('iterable arg',[4,5])
    print table
    
There are methods to get a row by a column-value pair, get the table schema,
convert a column to List, and rename columns!:
    
    print table.getRowsByKey('name','a')
    print table.getSchema()
    print table.colToList('name')
    table.renameCol('iterable arg','new name')
    print table,'\n'
    

It supports vertical concatenation (same schema!), \nand horizontal concatenation with SQL-like joins!:

    table2 = Table(['ID','name','constant','new name'])
    table2.append({'new name': 6, 'constant': 3, 'ID': 3, 'name': 'c'})
    table.vConcat(table2)
    print table
    
    table3 = Table(['another column!'])
    table3.append({'another column!': 'x'})
    table3.append({'another column!': 'y'})
    table3.append({'another column!': 'z'})
    table.hConcat(table3)
    print table
    
    table3 = Table(['name','age'])
    table3.append({'name': 'a','age':3})
    table3.append({'name': 'a','age':2})
    table3.append({'name': 'c','age':1})
    table.hConcat(table3, join='name')
    print table
    


And of course, you can sort(cmp,key,reverse) it **in place**:

    table.sort(key=lambda x:x['age'],reverse =True)
    print table
    table.sort(key=lambda x:(x['constant'],x['ID']))
    print table

    
At last but no least, you can filter it like this (returns a new table):

    tableFiltered = table.filter(lambda age: age>=2,['age'])
    print tableFiltered
    tableFiltered2 = table.filter(lambda name,constant: name == 'a' and constant==3 ,['name','constant'])
    print tableFiltered2
