# oh-mysql
方便的使用 mysql

Example:
<pre>
    from oh_mysql import OhMysql
    mysql = OhMysql(host = 'localhost',db = 'amazon_us',user = 'root',passwd = '123')
    mysql.table('category').filter(age=18).group_by('level').column('level','count(\*) as count').having('count(*)>100','level>3')
    res = mysql.fetchall()
    print 'res : ',res
    mysql.disconnect()
</pre>
<h3>table</h3>
函数定义：table(self,*tables)

参数说明：    
<ul>
<li>
    tables: 多个 table_name 的列表    
</li>
</ul>


例：
<pre>
    table('tb')
    table('tb1','tb2')
</pre>

<h3>filter</h3>
函数定义：filter(self,**cond_dic)

参数说明：    
<ul>
<li>
    cond_dic: 多个条件的键值对，支持大于和小于。
</li>
</ul>

比较符号同 django:
<pre>
    gt : 大于
    lt : 小于
    gte: 大于等于
    lte: 小于等于
    in : 在某个列表中
</pre>
    

例: 
<pre>
    filter(col1 = v1,col2__lte = v2,col3__in = v3)
</pre>

支持多表连接，需要和 table 方法配合
<pre>
    table('table1 as t1','table2 as t2').filter(t1.id__in = (1,2,3),t2.id__in = (1,2))
</pre>

<h3>update</h3>
函数定义: update(self,dic,cond_dic = None)     

参数说明：    
<ul>
    <li>dic: 字典，需要更新的字段及其值</li>
    <li>cond_dic: 条件字典</li>
</ul>
例:
<pre>
    update({'col1':v1,'col2':v2},{'id':1})
</pre>

<h3>insert</h3>
函数定义: insert(self,dic = None)     

参数说明：    
<ul>
    <li>dic: 字典，需要插入的字段及其值</li>
</ul>
例:
<pre>
    insert({'col1':v1,'col2':v2})
</pre>

<h3>group_by</h3>
函数定义：group_by(self,*columns):    

参数说明：    
<ul>
    <li>columns: 多个列名的列表</li>
</ul>

例：
<pre>
    group_by('col1','col2')
</pre>

<h3>having</h3>
函数定义: having(self,*h_conds)    

参数说明：    
<ul>
    <li>h_conds: 条件列表</li>
</ul>
例：
<pre>
    having('count(*)>n','sum(price)>p')
</pre>
注意，having 中的比较与 filter 中的比较不同，having 中采用原生的大于和小于符号。
