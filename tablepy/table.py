import copy
 
class Table(object):
    '''
        TODO:
            - In place row delete.
            - create tableviews with only the specified columns (a.k.a. Project)
            - unit tests
            - Make it a python package
    '''
    def __init__(self, schema = [], data=None, indexed=True):
        self.__rows =  []# list of row objects (dicts)
        self.indexes = {} # for faster direct lookup for row by column
        if not schema and data:
            schema = data[0].keys()
        if indexed:
            for col in schema:
                self.indexes[col] = {}
            if data:
                self.__rows = data
                for row in data:
                    for k in row.keys():
                        self.indexes[k][row[k]] = row
            
    def __iter__(self):
        return iter(self.__rows)
        
    def __getitem__(self,key):
        return self.__rows[key]
        
    def __len__(self):
        return len(self.__rows)
        
    def __nonzero__(self):
        return bool(self.__rows)
        
    def __repr__(self):
        return repr(self.__rows)
        
    def sort(self,cmp=None,key=None,reverse=False):
        self.__rows.sort(cmp=cmp,key=key,reverse=reverse)
        
    def addColumn(self,col,default=None):
        if col not in self.indexes:
            self.indexes[col] = {}
            defaultIterable = False
            try:
                iter(default)
                defaultIterable = True
            except TypeError,ex:
                pass
            if defaultIterable and len(default) == len(self):
                for i in xrange(0,len(self)):
                    self[i][col] = default[i]
                    tmp = self.indexes[col].get(default[i],[])
                    tmp.append(self[i])
                    self.indexes[col][default[i]] = tmp
            elif not defaultIterable:
                for row in self:
                    row[col] = default
                if self:
                    self.indexes[col][default]= list(self)#[row for row in self]
            else:
                raise ValueError('Default values length didn\'t match table\'s length')
        else:
            raise ValueError('Column Name already exists')
            
    def checkSchema(self,keys):
        if set(self.getSchema()) != set(keys):
            return False
        return True
        
    def getSchema(self):
        return self.indexes.keys()
        
    def append(self, row):
        if not self.checkSchema(row.keys()):
            raise ValueError('Schema doesn\'t match')
        self.__rows.append(row)
        for k,v in row.iteritems():
            tmp = self.indexes[k].get(v,[])
            tmp.append(row)
            self.indexes[k][v] = tmp
 
    def getRowsByKey(self, col,key,noneDict = False):
        if key in self.indexes[col]:
            return self.indexes[col][key]
        elif noneDict:
            return [dict(zip(self.getSchema(),len(self.getSchema())*[None]))]
        else:
            return []
        
    def renameCol(self,old,new):
        if old not in self.indexes:
            raise ValueError('Column %s doesn\'t exists' % (old,))
        elif new in self.indexes:
            raise ValueError('Column %s already exists' % (new,))
        for row in self:
            row[new] = row.pop(old)
        self.indexes[new] = self.indexes.pop(old)
        
    def vConcat(self,table):
        if not self.checkSchema(table.getSchema()):
            raise ValueError('Schema doesn\'t match')
        for row in table:
            self.__rows.append(row)
            for k in table.getSchema():
                tmp = self.indexes[k].get(row[k],[])
                tmp.append(row)
                self.indexes[k][row[k]] = tmp
    
    def hConcat(self,table,join = None):
        diff = set(self.getSchema()) & set(table.getSchema())
        if (diff and join is None) or len(diff) > 1:
            raise ValueError('Schemas can\'t have columns with the same name')
        elif join not in diff and join is not None:
            raise ValueError('The column %s must exists in both tables' % (join,))
        elif len(self) != len(table) and join is None:
            raise ValueError('Tables must have the same size')
        for k in table.getSchema():
            if k not in self.indexes:
                self.indexes[k] = {}
                
        extrarows = []
        for i in xrange(0,len(self)):
            row = self[i]
            if join:
                match =  table.getRowsByKey(join, row[join],True)
                if len(match) > 1:
                    newExtraRows = []
                    for r in match[1:]:
                        newRow = copy.deepcopy(row)
                        newRow.update(r)
                        newExtraRows.append(newRow)
                    extrarows += newExtraRows
                match[0][join] = row[join]
                row.update(match[0])
            else:
                row.update(table[i])
            for k in table.getSchema():
                if join != k:
                    tmp = self.indexes[k].get(row[k],[])
                    tmp.append(row)
                    self.indexes[k][row[k]] = tmp
        for row in extrarows:
            self.append(row)
         
    def colToList(self,col):
        if col not in self.getSchema():
            raise ValueError('Column %s doesn\'t exists' % (col,))
        return [row[col] for row in self]            
        
    def filter(self,func,keys=[]):
        return TableView(schema=self.getSchema(), data=[row for row in self if func(*[row[k] for k in keys])], indexed = True)
    
    def addIndex(self,cols):
        key = tuple(cols)
        if len(key) == 1:
            key = key[0]
        self.indexes[key] = {}
        for row in self:
            value = None
            if isinstance(key,str):
                value = row[key]
            else:
                value = tuple([row[k] for k in key])
            tmp = self.indexes[key].get(value,[])
            tmp.append(row)
            self.indexes[key][value] = tmp

    def groupBy(self,cols,func,args):
        key = tuple(cols)
        if len(key) == 1:
            key = key[0]
        if key not in self.indexes:
            self.addIndex(cols)
        data = []
        newschema = copy.deepcopy(cols)
        newschema.append('__result')
        for value,rows in self.indexes[key].iteritems():
            func_args = [[row[col] for col in args] for row in rows]
            result = []
            if isinstance(value,tuple):
                result = list(value)
            else:
                result = [value]
            result.append(func(func_args))
            data.append(dict(zip(newschema, result)))
        return TableView(schema=newschema, data=data, indexed = True)
        
class TableView(Table):
    '''
    Unmaterialized view of a table, altering the content of a view 
    will also alter the content in the original table, use copy.deepcopy
    to create a new copy from a table view.
    
    '''
    
    def __init__(self, schema = [], data=None, indexed = False):
        super(self.__class__, self).__init__(schema = schema , data=data, indexed=indexed)
