#coding:utf-8

import MySQLdb

SPLIT_WORD = '__'
OPERATORS = {
    'lt'   :   '<',
    'gt'   :   '>',
    'lte'  :   '<=',
    'gte'  :   '>=',
    'in'   :   'in'
}

def get_op(word):
    words = word.split(SPLIT_WORD)
    if len(words) == 1:
        return '='
    op = OPERATORS.get(words[1],'=')
    return op

def get_key(word):
    return word.split(SPLIT_WORD)[0]


class OhMysql(object):
    def __init__(self,**kwargs):
        self.host = kwargs.get('host','')
        self.db = kwargs.get('db','')
        self.user = kwargs.get('user','')
        self.passwd = kwargs.get('passwd','')
        self.tables = None
        self.columns = '*'
        self._connect()

    def __del__(self):
        if hasattr(self,'cursor'):
            self.cursor.close()
        if hasattr(self,'conn'):
            self.conn.close()

    def _connect(self):
        try:
            self.conn = MySQLdb.connect(host = self.host,db = self.db,user = self.user,passwd = self.passwd)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception,e:
            raise Exception('Failed to connect to database,please check settings.')

    def _execute_select(self):
        if not self.table:
            raise Exception('Error,you should choose a table with function table()')
        self._test()
        sql = 'select %s from %s ' % (self.columns,self.table)
        if self.where:
            sql = sql+' where '+self.where
        if self.group_cond:
            sql = sql + ' group by '+self.group_cond
        if self.having_cond:
            sql = sql + ' having '+self.having_cond
        self.cursor.execute(sql,tuple(self.condition))

    def disconnect(self):
        self.__del__()

    def fetchone(self):
        self._execute_select()
        return self.cursor.fetchone()

    def fetchall(self):
        self._execute_select()
        return self.cursor.fetchall()

    def _get_columns(self,table):
        self.cursor.execute('show columns from %s' % table)
        res = self.cursor.fetchall()
        columns = [r['Field'] for r in res]
        return columns

    def _test(self):
        try:
            self.cursor.ping()
        except Exception,e:
            self._connect()

    def table(self,*tables):
        '''
        语法: table('t1','t2')
        '''
        self._reset()
        if not self.tables or set(tables).issubset(set(self.tables)):
            self.cursor.execute('show tables')
            res = self.cursor.fetchall()
            self.tables = [r.values()[0] for r in res]
        if set(tables).issubset(set(self.tables)):
            self.table = ','.join(tables)
        else:
            raise Exception('Error : please make sure tables %s all exist' % str(tables))
        return self

    def _reset(self):
        self.table = ''
        self.columns = '*'
        self.where = ''
        self.having_cond = ''
        self.group_cond = ''
        self.condition = []

    def column(self,*columns):
        '''
        指定需要的列
        语法:column('col1','col2')
        '''
        if columns:
            self.columns = ','.join(columns)
        return self

    def filter(self,**cond_dic):
        '''
        支持多表连接
        语法: filter(col1 = v1,col2__lte = v2,col3__in = v3)
        '''
        if cond_dic and not isinstance(cond_dic,dict):
            raise Exception('Error,condition should be type of dict')
        if cond_dic:
            self.where = ' and '.join([get_key(k)+' '+get_op(k)+' %s ' for k in cond_dic])
            self.condition = [cond_dic[k] for k in cond_dic]
        return self
        
    def group_by(self,*columns):
        '''
        语法：group_by('col1','col2')
        '''
        if columns:
            self.group_cond = ','.join(columns) if columns else ''
        return self

    def having(self,*h_conds):
        '''
        语法: having('count(*)>n','sum(price)>p')
        '''
        if h_conds:
            self.having_cond = ' and '.join(h_conds)
        return self

    def update(self,dic,cond_dic = None):
        '''
        语法: update({'col1':v1,'col2':v2},{'id':1})
        '''
        if not (dic and isinstance(dic,dict)):
            return 0
        columns = self._get_columns(self.table)
        keys = [k for k in dic.keys() if k in columns]
        if not keys:
            return 0
        values = [dic[k] for k in keys]
        cd = [v for v in values]
        sql = 'update '+self.table+' set '+','.join([str(k)+'=%s' for k in keys])
        if cond_dic:
            sql = sql + ' where '+' and '.join([str(k)+'=%s' for k in cond_dic])
            cd += [cond_dic[k] for k in cond_dic]
        x = self.cursor.execute(sql,tuple(cd))
        return x

    def insert(self,dic = None):
        '''
        语法: insert({'col1':v1,'col2':v2})
        '''
        if not (dic and isinstance(dic,dict)):
            return 0
        columns = self._get_columns(self.table)
        keys = [k for k in dic.keys() if k in columns]
        if not keys:
            return 0
        values = [dic[k] for k in keys]
        cond = [v for v in values]
        sql = 'insert into '+self.table+' ('+','.join([str(k) for k in keys])+') values ('+','.join(['%s']*len(keys))+')'
        x = self.cursor.execute(sql,tuple(cond))
        return x



if __name__ == '__main__':
    mysql = OhMysql(host = 'localhost',db = 'amazon_us',user = 'root',passwd = 'zhy')
    mysql.table('category').group_by('level').column('level','count(*) as count').having('count(*)>100 and level>3')
    res = mysql.fetchall()
    print 'res : ',res
    mysql.disconnect()
    


