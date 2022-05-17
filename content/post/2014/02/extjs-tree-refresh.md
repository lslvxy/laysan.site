---
title:  ExtJs 刷新后，默认选中刷新前最后一次选中的节点
date: 2014-02-25
comments: on
categories:  [ExtJs]
tags: [extjs,tree,树,checkbox]
id: 201402250930
---

在对树节点进行操作后往往需要进行reload操作刷新一下树，但是很多业务都需要在树形刷新后默认选中最后一次选中的节点。这样就必须先保存前一次选中节点的信息，在reload之后再次通过节点的信息进行expand逐层展开到这个节点上。
<!-- more -->
查询了好久终于找到一个可行的方案，就是通过节点的path来记录节点的位置信息，然后通过path从root节点开始逐层展开，直到最后一个节点。
完成的代码如下：

首先是extjs3.x版本中的方法：

```js
//获取选中的节点  
var node = tree.getSelectionModel().getSelectedNode();  
if(node == null) { //没有选中 重载树  
    tree.getRootNode().reload();  
} else {        //重载树 并默认选中上次选择的节点    
    var path = node.getPath('id');  
    tree.getLoader().load(tree.getRootNode(),  
         function(treeNode) {  
             tree.expandPath(path, 'id', function(bSucess, oLastNode) {  
                  tree.getSelectionModel().select(oLastNode);  
              });  
         }, this);    
}
```

跟Extjs3.0不同Extjs4.2的写法如下

```js
idPath = selNode.getPath("id");                 
tree.getStore().load({                     
  node: tree.getRootNode(),                     
  callback: function () {                          
    tree.expandPath(idPath, 'id');                  
  }             
});
```

需要注意的是后台返回的树的json数据时节点必须包含`id`属性，原本我没有这个属性，但是我把getPath方法中的参数改成其他的一个属性。事实证明这样是达不到效果的，最后在json中添加了id属性才成功的。
