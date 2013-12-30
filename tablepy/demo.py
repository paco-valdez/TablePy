from tablepy.table import Table

def main():
    table = Table(['ID','name'])
    table.append({'ID':2,'name':'a'})
    table.append({'ID':1,'name':'b'})
    print """ This is a simple Table:
    table = Table(['ID','name'])
    table.append({'ID':2,'name':'a'})
    table.append({'ID':1,'name':'b'})
    print table
    """
    print table,'\n'
    
    print """it supports len, iteration and indexing
    print len(table), not table
    print iter(table)
    print table[0]
    """
    print len(table), not table
    print iter(table)
    print table[0],'\n'
    
    print """ We can add a column with a constant value:
    table.addColumn('constant',3)
    print table
    """
    table.addColumn('constant',3)
    print table,'\n'
    
    print """ Also we can add a column with a interable arg (must be the same size as our table):
    table.addColumn('iterable arg',[4,5])
    print table
    """
    table.addColumn('iterable arg',[4,5])
    print table,'\n'
    
    print """ There are methods to get a row by a column-value pair, get the table schema, \nconvert a column to List, and rename columns!
    print table.getRowsByKey('name','a')
    print table.getSchema()
    print table.colToList('name')
    table.renameCol('iterable arg','new name')
    print table
    """
    print table.getRowsByKey('name','a')
    print table.getSchema()
    print table.colToList('name')
    table.renameCol('iterable arg','new name')
    print table,'\n'
    
    print """ it supports vertical concatenation (same schema!), \nand horizontal concatenation with SQL-like joins!
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
    """
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
    table3.append({'name': 'c','age':2})
    table3.append({'name': 'b','age':1})
    table.hConcat(table3, join='name')
    print table,'\n'
    
    print """ And of course, you can sort(cmp,key,reverse) it **in place**:
    table.sort(key=lambda x:x['age'],reverse =True)
    print table
    table.sort(key=lambda x:(x['constant'],x['ID']))
    print table
    """
    table.sort(key=lambda x:x['age'],reverse =True)
    print table
    table.sort(key=lambda x:(x['constant'],x['ID']))
    print table,'\n'
    
    print """ You can filter it like this (returns a new table):
    tableFiltered = table.filter(lambda age: age>2,['age'])
    print tableFiltered
    tableFiltered2 = table.filter(lambda name,constant: name == 'a' and constant==3 ,['name','constant'])
    print tableFiltered2
    """
    tableFiltered = table.filter(lambda age: age>2,['age'])
    print tableFiltered
    tableFiltered2 = table.filter(lambda name,constant: name == 'a' and constant==3 ,['name','constant'])
    print tableFiltered2,'\n'
    
    print """ It also supports group by:
    table.append({'new name': 4, 'constant': 4, 'name': 'a', 'age': 5, 'ID': 2, 'another column!': 'x'})
    table.append({'new name': 5, 'constant': 4, 'name': 'a', 'age': 6, 'ID': 2, 'another column!': 'x'})
    table.append({'new name': 6, 'constant': 4, 'name': 'a', 'age': 8, 'ID': 2, 'another column!': 'x'})
    print table
    print table.groupBy(['new name'], lambda args: float(sum([i[0] for i in args]))/len(args),['age'])
    print table.groupBy(['new name', 'constant' ], lambda args: sum([i[0]+i[1] for i in args]),['age','constant'])
    """
    table.append({'new name': 4, 'constant': 4, 'name': 'a', 'age': 5, 'ID': 2, 'another column!': 'x'})
    table.append({'new name': 5, 'constant': 4, 'name': 'a', 'age': 6, 'ID': 2, 'another column!': 'x'})
    table.append({'new name': 6, 'constant': 4, 'name': 'a', 'age': 8, 'ID': 2, 'another column!': 'x'})
    print table
    print table.groupBy(['new name'], lambda args: float(sum([i[0] for i in args]))/len(args),['age'])
    print table.groupBy(['new name', 'constant' ], lambda args: sum([i[0]+i[1] for i in args]),['age','constant'])

if __name__ == '__main__':
    main()
