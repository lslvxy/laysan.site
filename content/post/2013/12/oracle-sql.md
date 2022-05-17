---
title:  oracle数据库常用SQL语句
date: 2013-12-03
comments: on
categories:  [DataBase]
tags: [oracle,数据库,sql]
id: 201312031830
---


日常工作中常用到的sql语句，现总结如下，留作日后查看。
<!-- more -->
#### 1、按照两列中的最大值取 ，只取两列其中的一列

```sql
SELECT *  FROM t_doc T  ORDER BY GREATEST(T.Load_Count,T.Read_Count) desc
```

#### 2、取两列之和

```sql
select  t.*,(nvl(T.Load_Count,0)+nvl(T.Read_Count,0 )) as c FROM t_doc T   order by c desc
```

#### 3、取两列字符串连接

```sql
select T.Load_Count||T.Read_Count FROM t_doc T
```

#### 4、获取oracle数据库当前用户下所有表名和表名的注释

```sql
select a.TABLE_NAME,b.COMMENTS
from user_tables a,user_tab_comments b
WHERE a.TABLE_NAME=b.TABLE_NAME
order by TABLE_NAME
```

#### 5、两列结果合并为一列输出（两列数据类型必须一样）

```sql
select a from tb
union all
select b from tb
```

#### 6、将一列多行拼接成一行

```sql
select wmsys.wm_concat(name) from table_name
//wmsys.wm_concat()拼接字段 以逗号分开
```

#### 7、 不是 SELECTed 表达式

Oracle 数据库，执行下面语句出现错误“ORA-01791: 不是 SELECTed 表达式”：

```sql
select distinct t.name from auth_employee t order by t.auth_employee_id asc
```

原来：SELECT语句中含有DISTINCT关键字或者有运算符时，排序用字段必须与SELECT语句中的字段相对应。
网上搜到解释如下：
在ORDER BY中指定多个列，结果将先按照子句中的第一列排序，然后第二个，依此类推。
在SELECT中未出现的列名也可用于ORDER BY 子句中，只要TABLE中有就行。
但如果SELECT子句中出现了DISTINCT关键字，则只能用出现过的列名，
而且如果SELECT子句中使用了任何运算符，在ORDER BY 子句中必须保持和SELECT子句中表达式完全一致，否则出现错误：“ORA-01791: 不是 SELECTed 表达式”。

#### 8、查询数据库表的建表时间

```sql
SELECT OBJECT_NAME,CREATED FROM USER_OBJECTS
    WHERE object_type = 'TABLE' ORDER BY  CREATED DESC
```

#### 9、查询序列的当前值

```sql
select ANALYSIS_FIX_SEQ.currval  from dual (注：此sql只能在nextval之后才可以使用)
select last_number from User_Sequences where sequence_name='ANALYSIS_FIX_SEQ'
```

#### 10、恢复误删除的数据

```sql
create table quick as
SELECT * FROM T_LOCATION_ALARM AS  OF TIMESTAMP  
to_timestamp('2013-11-29 11:00:00', 'yyyy-mm-dd hh24:mi:ss');
```

这样可以查询到这个时间点的数据

#### 11、恢复误删除的PL/SQL对象

```sql
SELECT  r.object_name ,r.original_name,r.operation ,r.droptime
FROM user_recyclebin  r order by droptime desc;
```

通过这个sql就可以查询到已经删除的对象。

再通过下面这个sql就可以查询到对象的内容，不过需要管理权限

```sql
SELECT NAME, TEXT FROM DBA_SOURCE AS OF TIMESTAMP
TO_TIMESTAMP('2013-11-29:11:20:15', 'yyyy-mm-dd hh24:mi:ss')
```
