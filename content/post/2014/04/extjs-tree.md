---
title:  ExtJs4之树组件
date: 2014-04-04
comments: on
categories:  [ExtJs]
tags: [extjs,extjs4,tree,树]
id: 201404041730
---

`TreePanel`是ExtJS中最多能的组件之一，它非常适合用于展示分层的数据。`TreePanel`和`GridPanel`继承自相同的基类，所以所有从`GridPanel`能获得到的特性、扩展、插件等带来的好处，在`TreePanel`中也同样可以获得。列、列宽调整、拖拽、渲染器、排序、过滤等特性，在两种组件中都是差不多的工作方式。
<!-- more -->
让我们开始创建一个简单的树组件

首先创建Store:

```js
var treeStore = Ext.create('Ext.data.TreeStore', {
    proxy: {
	    type: 'ajax',
	    url: 'grade.htm?getAllGrades'
    },
    root: {
	    text: 'name',
	    id: 'id',
	    expanded: true,
	    leaf:true
    },
    folderSort: true,
    sorters: [{
	    property: 'id',
	    direction: 'ASC'
    }]
});
```

表1 Ext.data.TreeStore主要配置项

|配置项|参数类型|说明|
|---|---|---|
|clearOnLoad|Boolean|设置加加载节点数据时,是否清楚前一次加载的数据,默认为true|
|defaultRootId|String|设置默认的根节点id,默认为root|
|defaultRootProperty|String|设置默认的根属性|
|nodeParam|String|异步加载节点时的参数名称,默认为node|


创建TreePane:

```js
var gradeTree=Ext.create('Ext.tree.Panel', {
   store: treeStore,
    id:'gradeTree',
    bodyStyle: 'background-color:#DEEBF7',
    height: 300,
    width: 250,
    useArrows: true,
    root: {
	text:'我的班级',
	id:'0'
    },
    rootVisible : true,
    tbar:new Ext.Toolbar({
	style:'border-top:0px;border-left:0px',
	items:[{
	    iconCls: 'icon-expand-all',
	    text:'展开',
	    tooltip: '展开所有',
	    handler: function(){
             gradeTree.getRootNode().expand(true);
        },
	    scope: this
	},'-',{
	    iconCls: 'icon-collapse-all',
	    text:'折叠',
	    tooltip: '折叠所有',
	    handler: function(){
           gradeTree.getRootNode().collapse(true);
        },
	    scope: this
	}]
    })
});
```


Tree节点点击事件:

```js
gradeTree.on('itemclick',function(view,record,item,index,e,opts){  
    //获取当前点击的节点  
    var treeNode=record.raw;  
    var id = treeNode.id;  
    var text=treeNode.text;  
    studentStore.loadPage(1,{params:{gradeId:id}});
});
```



表2 Ext.tree.Panel主要配置项


|配置项|参数类型|说明|
|---|---|---|
|animate|Boolean|设置在展开和收缩节点的时候是否启用动画效果,默认为Ext.enableFx|
|displayField|String|设置节点标题的字段名,默认为text|
|hideHearers|Boolean|设置为true则隐藏标题|
|lines|Boolean|设置是否显示节点前的虚线,默认为true|
|root|Object|允许不为tree.Panel指定Store而通过预读数据创建简单的树结构|
|rootVisible|Boolean|设置根节点是否可见,默认为true|
|singleExpland|Boolean|设置是否单一展开节点,默认为false|
|useArrows|Boolean|设置为true则使用Vista风格的箭头,默认为false|

表3 Ext.tree.Panel主要方法

|方法名|说明|
|:---|---|
|collpaseAll([Function callback],[Object scope]):void|收缩所有展开的节点;参数说明:callback:收缩完毕后的回调函数 ;scope:回调函数执行的作用域|
|expandAll([Function callback],[Object scope]):void|展开所有展开的节点;参数说明:callback:展开完毕后的回调函数;scope:回调函数执行的作用域|
|expandPath(String path,[String field],[String separator],[Function callback],[Object scope]):void|展开树节点到指定的路径;参数说明:path:路径字符串;filed(可选):获取数据的字段名,默认为id属性;separator:路径风格符,默认为'/';callback:当节点展开后的回调函数,传入函数的参数包括:success:表示是否展开成功; lastNode:展开的最后一个节点scope:回调函数执行的作用域|
|getChecked():Array|得到一个已选节点的数组|
|selectPath(String path,[String field],[String separator],[Function callback],[Object scope]):void|选择特定路径的树节点参数说明:同expandPath方法.|


代码示例1:多列树

```js
Ext.onReady(function(){
	var tree = Ext.create('Ext.tree.Panel', {
	    ---
title:  'TreeGrid（多列树示例）',
	    renderTo: Ext.getBody(),
	    width : 200,
	    height : 120,
	    fields: ['name', 'description'],
	    columns: [{
		xtype:'treecolumn',//树状表格列
		text: '名称',
		dataIndex: 'name',
		width: 100,
		sortable: true
	    }, {
		text: '描述',
		dataIndex: 'description',
		flex: 1,
		sortable: true
	    }],
	    root: {
		name: '树根',
		no_image: https://source.unsplash.com/random/800x600
description: '树根的描述',
		expanded: true,
		children: [{
		    name: '节点一',
		    no_image: https://source.unsplash.com/random/800x600
description: '节点一的描述',
		    leaf: true
		}, {
		    name: '节点二',
		    no_image: https://source.unsplash.com/random/800x600
description: '节点二的描述',
		    leaf: true
		}]
	    }
	});
});
```

代码示例2:带复选框的树

```js
Ext.onReady(function(){
	var tree = Ext.create('Ext.tree.Panel', {
	    ---
title:  '复选框示例',
	    width : 150,
	    height : 100,
	    renderTo: Ext.getBody(),
	    root: {
		text: '树根',//节点名称
		expanded: true,//默认展开根节点
		children: [{
		    text: '节点一',//节点名称
		    checked : true,//默认选中
		    leaf: true//true说明为叶子节点
		}, {
		    text: '节点二',//节点名称
		    checked:false,//默认不选中
		    leaf: true//true说明为叶子节点
		}]
	    }
	});
});
```

代码示例3:树面板之间的拖拽

```js
Ext.onReady(function(){
        //创建树面板一
        Ext.create('Ext.tree.Panel', {
            ---
title:  '树一',
            width: 200,
            height: 150,
            renderTo: 'tree1',
            root: {
                text: '树根',//节点名称
                expanded: true,//默认展开根节点
                children: [{
                    text: '节点一',//节点名称
                    leaf: true//true说明为叶子节点
                }, {
                    text: '节点二',//节点名称
                    leaf: true//true说明为叶子节点
                }]
            },
            viewConfig: {
		plugins: {
		allowContainerDrop : true,
		ptype: 'treeviewdragdrop',
		nodeHighlightOnRepair : true } }
	    });

        //创建树面板二
        Ext.create('Ext.tree.Panel', {
            ---
title:  '树二',
            width: 200,
            height: 150,
            renderTo: 'tree2',
            root: {
                text: '树根',
                expanded: true
            },
           viewConfig: {
	       plugins: {
		   allowContainerDrop : true,
		   ptype: 'treeviewdragdrop'
	     }
	   }
   });
});
```
