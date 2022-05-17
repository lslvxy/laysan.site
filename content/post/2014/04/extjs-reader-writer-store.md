---
title:  ExtJs4之Store、Reader和Writer
date: 2014-04-04
comments: on
categories:  [ExtJs]
tags: [extjs,store,reader,writer]
id: 201404040930
---

ExtJs4中的Store是最常用的组件了，本文对store以及reader和writer做了详细的说明。
<!-- more -->
## 1.Reader数据读取器

数据读取器主要用于将数据代理读取到的原始数据按照不同的规则进行解析，将解析后的数据保存在Model模型对象中。数据读取器相当于原始数据格式与Extjs标准数据格式之间的桥梁，它屏蔽了原始数据格式不同对程序开发造成的影响。在Extjs中提供的数据解析器主要有如下3种：

Ext.data.reader.Json  JSON数据读取器

Ext.data.reader.Xml  XML数据读取器

Ext.data.reader.Array&nbsp; 数组数据读取器

### 1.1 Ext.data.reader.Reader

Ext.data.reader.Reader是读取器的父类，主要用于从数据源读取结构化数据，它有两个子类分别是JsonReader和XmlReader。下表列出了它的主要配置项和方法。

表1-1 Ext.data.reader.Reader主要配置项

|配置项|参数类型|说明|
|:---|---|
|idProperty|String|设置作为数据唯一表示的字段名，默认为Model模型的id字段|
|implicitIncludes|Boolean|设置是否级联读取数据，默认为true|
|messageProperty|String|设置获取响应信息的属性名|
|root|String|设置返回信息的根名称，为必选项|
|successProperty|String|设置获取成功状态的属性名，默认为success|
|totalProperty|String|设置获取记录总数的属性名，默认为total|

表1-2 Ext.data.reader.Reader主要方法

|方法|说明|
|:---|---|
|read(Object response):Ext.data.ResultSet|读取响应对象，返回结果集response：可以是一个XMLHttpRequest对象，可以是一个普通的Json对象|

Ext.data.reader.Reader支持嵌套数据的读取，它会根据实体模型Model中关系API简历关联关系遍历响应数据。

### 1.2 Ext.data.reader.Json

Ext.data.reader.Json 是读取Json数据的数据读取器，它根据实体模型Model中字段定义的映射关系解析原始数据，形成记录集。

表 1-3 Ext.data.reader.Json 主要配置项


|配置项|参数类型|说明|
|:---|---|---|
|record|String|定位在Json响应信息中发现记录数据的位置，一般情况下不需要该配置项|
|useSimpleAccessors|Boolean|设置是否使用简单是陪方式，默认为false.如属性foo.bar.baz在默认情况下会从root中找foo属性,然后在foo中找bar属性,在bar中找baz属性.在简单模式下会最为一个整体处理,不会拆分.|

表1-4 Ext.data.reader.Json 主要方法

|方法 |说明|
|:---|---|
|readRecords(Object data):Ext.data.ResultSet|从json对象中读取信息,返回结果集data:数据对象,在该对象中包含与配置项root和titalProperty对应的属性,分别表示包含记录信息的数组和总记录数|

### 1.3 Ext.data.reader.Xml

Ext.data.reader.Xml 是读取xml文档格式信息的数据读取器，它根据实体模型Model中字段定义的映射关系解析原始信息，形成记录集。

注意：为了使浏览器可以正确的解析xml文档，必须设置相应的content-type类型为`text/xml`

表1-5 Ext.data.reader.Xml 主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|record|String|包含记录信息元素的DomQuery路径|

表 1-6 Ext.data.reader.Xml 主要方法

|方法|说明|
|:---|---|
|getData(Object date):Object readRecords(Object doc): Ext.data.ResultSet|获取标准化的数据对象            
从xml数据文档中读取信息，形成记录集doc：xml数据文档对象|

### 1.4 Ext.data.reader.Array

Ext.data.reader.Array继承自Ext.data.reader.Json，是读取二维数据信息的读取器，内层数组是一个包含字段数据的数据行，如果字段映射存在字段将根据它的下标取值到model中，如果字段映射不存在则字段按字段的原始位置进行取值。Ext.data.reader.Array的主要配置项和方法请参考Ext.data.reader.Json相关说明。

## 2.Writer数据写入器

数据写入器主要用于将数据代理提交到服务器的数据进行编码，相当于Extjs标准数据格式与服务器数据格式之间的桥梁，他屏蔽了服务器端数据格式不同对程序开发造成的影响。在Extjs中提供的数据写入器有：

Ext.data.writer.Json => Json写入器

Ext.data.writer.Xml => xml写入器

### 2.1 Ext.data.writer.Writer

Ext.data.writer.Writer 是数据写入器的父类，它负责处理请求对象，将数据转换为指定格式，对于客户端代理是不需要指定Writer 写入器的。

表2-1 Ext.data.writer.Writer 主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|nameProperty|String|设置发送到服务器数据的键值属性名|
|writerAllFields|Boolean|设置是否向服务器写入所有字段，false则指包含被修改的字段，默认为true|

表2-2 Ext.data.writer.Writer&nbsp; 主要方法

|方法|说明|
|:---|---|
|getRecordData(Object record)：Object|获取格式化之后的数据;record；需要发送的服务器记录对象|

### 2.2 Ext.data.writer.Json

JSON格式的数据写入器，它会将实体模型model中的数据转化为json格式发送到服务器。

```js
wirter：{
    type:'json'
}
```

发往服务器的数据为：`{"id":1,"name":"tom","age":24}`.

### 2.3Ext.data.writer.Xml

XML格式的数据写入器，它会将Model中的数据转换为xml发送到服务器。

表2-2 Ext.data.writer.Xml 主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|defaultDocumentRoot|String|设置当documentRoot为空时的默认根标签名称|
|documentRoot|String|设置xml文档的根标签名称，默认为xmlData|
|header|String|设置xml文档的头属性，如encoding编码或version版本，默认为""|
|record|String|设置记录节点的标签名称，默认为rocord|

## 3. Store数据集

Store数据集是一个客户端模型对象Model的缓存，它可以为Extjs组件提供数据输入，store通过数据代理夹在数据，也可以手工调用lodaData等方法加载数据，解析后的数据对象缓存在Store数据集中，并通过存取函数进行访问。

在Extjs提供的数据集类主要包括：

`Ext.data.AbstractStore`、`Ext.data.Store`、`Ext.data.ArrayStore`、`Ext.data.DirectStore`、`Ext.data.JsonPStore`、`Ext.data.JsonStore`、`Ext.data.XmlStore`。

### 3.1 Ext.data.AbstractStore

Ext.data.AbstractStore是Ext.data.Store 和Ext.data.TreeStore的父类，它不能被直接实例化，但提供了大量的方法供子类使用，除非需要创建新的Store类，否则在大多数情况下应该使用Ext.data.Store类。

表3-1 Ext.data.AbstractStore 主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|autoLoad|Boolean/Object|设置数据集是否自动加载数据，如果设置为true或提供了加载的配置对象则数据集在创建后后自动调用load方法加载数据，默认为false。|
|autoSync|Boolean|设置是否在数据修改后自动通过数据代理进行同步|
|fields|Array|设置应用于模型的字段定义，store或自动根据fields定义创建模型类|
|proxy|String/Ext.data.proxy.Proxy/Object |设置代理，可以是字符串，配置对象或者代理实例|
|storeId|String|设置数据集id，这个id将被注册到Ext.data.StoreManager中|

表3-2 Ext.data.AbstractStore 主要方法

|方法|说明|
|:---|---|
|getNewRecords：Array|获取所有新增但未调用代理进行数据同步的记录数组|
|getProxy：Ext.data.proxy.Proxy|获取数据代理|
|getUpdatedRecords：Array|获取被修改但是未调用代理进行数据同步的记录数组|
|isLoading：Boolean|获取当前store是否处于加载状态|
|load(Object options):void|加载数据，options：传到代理中的Ext.data.Operation操作参数配置对象|
|sync：Void|同步数据|

### 3.2 Ext.data.Store

Ext.data.Store 是一个基本的数据集类，它通过数据代理读取数据，提供了排序、过滤、查找等基本功能。

表3-3 Ext.data.Store主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|buffered|Boolean|设置是否允许Store缓存之前读取的数据|
|clearOnPageLoad|Boolean|设置在分页查询中是否请求当前页面数据，默认为true，设置为false则允许在一页中显示大量数据|
|data|Array|内置数据对象组成的数组，在数据集初始化之后该数组会读入数据集|
|model|String|设置store关联的Model模型|
|proxy|String/Ext.data.proxy.Proxy/Object|设置数据代理|
|purgePageCount|Number|设置在更新缓存数据之前,缓存数据的最大页数,设置为0则不更新缓存数据,该配置项只在buffered设置为true时生效|
|remotrFilter|Boolean|设置是否使用远程过滤,默认为fakse|
|remoteGroup|Boolean|设置是否使用远程分组,默认为fakse|
|remoteSort|Boolean|设置是否使用远程排序,默认为fakse|
|sortOnFilter|Boolean|设置在过滤数据时是否同时进行排序,默认为true,该配置项只在客户端过滤时生效|

表3-4 Ext.data.Store主要方法

|方法名|说明|
|:---|---|
|Store(Object config)|创建一个新的数据集对象,config:一个包含数据集必要信息的配置对象|
|add(Object data):Array|增加数据记录到数据集中,data:一个数据对象的数组|
|aggregate(Function fn,[Object scope],Boolean grouped,[Array args]):void|允许在数据集上聚合函数fn:聚合函数,分组后的记录数是唯一的参数;scope:聚合函数的执行范围;grouped:设置是否对Store中的每一组调用聚合函数,该参数只在具有一个分组字段groupFiled时生效;args:传递到聚合函数中的任何其他参数|
|average(String field,Boolean grouped):void|获取指定字段的平均值,field:计算平均值的字段名;grouped:设置是否对Store中的每一组调用聚合函数,该参数只在具有一个分组字段groupFiled时生效|
|clearFilter(Boolean suppressEvent):void|清除过滤器;suppressEvent：设置是否压制事件，如果为true则在清空过滤器时不会触发datachanged事件|
|clearGrouping：void|清除分组|
|collect(String dataIndex，[Boolean allowNull],[Boolean bypassFilter]):void|收集数据集中指定索引的唯一值集;dataindex:索引属性名;allownull:true则允许为空/undefined或者空字符串;bypassFIlter:true则收集所有记录,false则收集过滤后的数据|
|count(Boolean grouped) :void|获取Store中的记录数;grouped:true则以分组的方式计算记录数,该参数只在具有一个分组字段groupFiled时生效|
|each(Function fn,[Object scope]):void|遍历数据集中的记录对象,并将数据记录对象传入指定的函数中;fn:遍历数据集调用的函数,当前数据记录对象作为第一个参数传递到该函数中,返回false则终止循环;scope:函数作用域|
|filter(Mixed filters，String value)：void|过滤数据集;filter：过滤器集合;value：过滤值，当第一个参数为字段名时生效|
|filterBy(Function fn,[Object scope]):void|通过特殊函数过滤数据集.数据集中的每一个数据记录对象都会传入该函数,如果函数返回true则记录被保留,否则记录会被过滤掉;fn:过滤函数,一下2个参数将被传递到该函数中;Record:当前传入过滤函数的记录对象;id:数据记录的id;scope:过滤函数的作用域|
|find(String fieldName,String/RegExp value,[Number startIndex],[Boolean anyMatch],[Boolean caseSensitive],Boolean exactMatch):Number|在数据集中查询匹配字段值的第一个记录,该记录的索引值将被返回(匹配失败返回-1);fieldName:要查找的字段名;value:任意一个匹配字段值的字符串或者正则表达式;startInde:开始查找的索引位置;anyMatch:true则匹配字段值的全部,否则从开头进行匹配;caseSensitive:true表示区分大小写;exactMatch:true表示执行精确匹配,默认为false|
|findBy(Function fn,[Object scope],[Number startIndex]):Number|通过调用查询函数匹配数据集中第一个满足要求的记录,该记录的索引值将被返回,失败返回-1.fn:查询函数,一下2个参数将被传递到该函数中;Record:当前传入过滤函数的数据记录对象,可以通过调用Ext.data.Record.get方法获取字段值;id:数据记录id;scope:作用域;startIndex:开始查询的索引位置|
|fineExact(String fieldName,Mixed value,[Number startIndex]):Number|通过指定字段名和匹配值查询数据集第一个满足要求的记录,该记录的索引值将被返回,失败返回-1.fieldName:字段名;value:匹配值;startIndex:开始查询的索引位置|
|findRecord()|参考find方法,返回值为记录对象|
|first(Boolean grouped):Model/undefined|便利函数,用于获取Store中的第一条记录;grouped:true则返回所有分组的第一条记录,该参数只在具有一个分组字段groupFiled时生效|
|getAt(Number index):Model|取得指定索引位置的数据记录对象;index:数据记录对象在数据集中的索引位置|
|getById(String Id):Model|取得指定id的数据记录对象|
|getCount():Number|取得数据集中缓存的数据记录总数.如果使用了分页则该值可能不是数据的总数量,如果被解析的数据对象中包含了数据的总数量则可以通过getTotalCaout方法得到|
|getGroupString(Model instance):void|取得指定模型实例的分组字符串|
|getGroups:Array|取得分组的数据对象|
|getPageFromRecordIndex(Number index):Number|获取指定索引记录所在的页号|
|getRange([Number startindex],[Number endIndex]):Model[]|取得指定范围的数据记录数组,index默认为0到最后一个记录的索引|
|getTotalCount():Number|取得从服务器返回的数据记录总数.如果使用分页则该值必须包含咋服务器返回的数据对象中,当客户端数据集内容发生变化时不会更新该值|
|group(String/Array groupers,String direction):void|分组数据;groupers:一个字段名,或分组器配置对象组成的数组;direction:排序方式,默认为ASC|
|hasPendingRequests:number|获取未完成的请求数量|
|indexOf(Model record):number|取得数据记录对象在数据集缓存中的索引位置,如果数据记录对象不在缓存中则返回-1|
|indexOfId(String id):Number|取得指定Id的数据记录对象在数据集缓存中的索引位置,如果数据记录对象不在缓存中则返回-1|
|ndexOfTatal(Model record):number|取得数据记录在0到totalCount之间的索引位置|
|insert(number index, Model[] records):void|插入数据记录到数据集中指定的索引位置,该操作会触发数据集的add事件|
|isFiltered():Boolean|返回当期数据集中的数据是否经过过滤|
|isGrouped():Boolean|返回当期数据集中的数据是否经过分组|
|last(Boolean grouped):Model/undefined|获取Store中的最后一条记录|
|load(object/Function options):void|使用数据代理加载数据|
|loadData(Array data,[Boolean append]):void|直接加载数组数据到Store中,append:true表示将数据追加到缓存中,false表示用新数据替换旧数据|
|loadPage(Number page):void|读取指定页码的数据,会根据page参数计算出start和limit参数进行传递|
|loadRecords( Array reocrds,object options):void|加载数组数据到store中,会触发datachanged事件,该方法通常被数据代理内部使用|
|max(String field,Boolean grouped):Mixed/undefined|取得指定字段的最大值|
|min(String field,Boolean grouped):Mixed/undefined|获取指定字段的最小值|
|nextPage：void|读取当前数据集的下一页数据|
|prefetch（Number page，Object options）:void|预读指定页码的数据|
|previousPage：void|读取当前数据集的上一页数据|
|queryBy（Function fn,[Object scope]）:MixedCollection|通过调用过滤函数来查询满足要求的记录,如果过滤函数返回true则当前数据记录对象将包含在查询结果中|
|remove(Model/Array records)|从数据集中删除数据记录对象,该操作会触发数据集的remove事件,在remove事件之后触发datachanged事件|
|removeAll（Boolean silent）：void|从数据集中删除所有数据,silent为true则不触发事件|
|removeAt（Number index)：void|从数据集中删除指定索引位置的数据|
|sum(String field,Boolean grouped):Number|获取指定字段的和值|

### 3.3 Ext.data.ArrayStore、Ext.data.JsonStore和Ext.data.XmlStore

为了方便使用Store读取各类数据,Extjs提供了内置数据读取器的辅助Store类来加速程序的开发过程,

Ext.data.JsonStore:内置了Ext.data.reader.Json

Ext.data.XmlStore:内置了Ext.data.reader.Xml

Ext.data.ArrayStore:内置了Ext.data.reader.Array

详细使用同Store类似,就不再详细说明

### 3.4 Ext.data.DirectStore和Ext.data.JsonPStore

extjs还提供了内置不同代理以及数据读取器的辅助类

Ext.data.DirectStore:内置了Ext.data.proxy.Direct代理和Ext.data.reader.Json读取器

Ext.data.JsonPStore:内置了Ext.data.proxy.JsonP代理和Ext.data.reader.Json读取器

详细也不再详细说明.

--本篇完--
