---
title:  ExtJs4中的复选树级联选择
date: 2014-02-18
comments: on
categories:  [ExtJs]
tags: [extjs,tree,树,级联,选择]
id: 201402180930
---

这几天要把项目中的几个模块有ext3升级到ext4，还要保持页面展示和功能要跟3.x版本的一样。升级并不是一件简单的是，基本相当于重写了，3.x版本的复选框树级联操作是在网上找的一个现成的插件，直接搬运到4.2中就不能用了，但是又找不到可用的插件。百度谷歌了好久，还真让我搞出来一个方法，记录下来吧，也分享给大家。如有不合理或者更好的方法希望不吝赐教。
<!-- more -->
在3.x版本中要实现级联选择的话，我使用的是一个`TreeCheckNodeUI.js`这个文件百度一下都能找到啊，就不详细说明了，很好用。

在4.2中实现的方法是在`treepanel`的配置项`viewConfig`中添加函数`onCheckboxChange`，表示复选框选择状态发生变化是触发的事件，先把代码贴出来：

```js
viewConfig:{
  onCheckboxChange: function(e, t) {
         var item = e.getTarget(this.getItemSelector(), this.getTargetEl()), record;
         if (item) {
             record = this.getRecord(item);
             var check = !record.get('checked');
             record.set('checked', check);
             if (check) {
                 record.bubble(function(parentNode) {
                     parentNode.set('checked', true);
                 });
                 record.cascadeBy(function(node) {
                     node.set('checked', true);
                 });
                 record.expand();
               record.expandChildren();
             } else {
               record.collapse();
               record.collapseChildren();
                 record.cascadeBy(function(node) {
                     node.set('checked', false);
                 });
               record.bubble(function(parentNode) {
                var childHasChecked=false;
                var childNodes = parentNode.childNodes;
              if(childNodes || childNodes.length>0){
                for(var i=0;i<childNodes.length;i++){
                  if(childNodes[i].data.checked){
                    childHasChecked= true;
                    break;
                  }
                }
              }
                if(!childHasChecked){
                       parentNode.set('checked', false);
                     }
                 });

             }
         }
     }
}
```

其实这段代码我也不是很懂，几个方法是百度出来的，然后纯属于东拼西凑，最后居然还实现了功能，等闲来再好好了解一下这段代码的意思。

还遇到过一个问题，3.x的版本中有个grid的单元格悬浮展示数据的功能，其实就是一个`quicktip`将单元格中的内容展示出来。同样的，直接搬运到extjs4中还是实现不了的，又花了半天时间才找到一个方法，还是直接贴出代码吧：

```js
{
  header : "姓名",
  width : 100,
  dataIndex : "name",
  menuDisabled : true,
  sortable : false,
  renderer : function(value, metadata, record, rowIndex,
      columnIndex, store) {
    value = value.replace(/</g, '&lt');
    metadata.tdAttr = 'data-qtip="' + value+ '"';
    return value;
  }
}
```

给colmodel中的列添加一个`renderer`函数，给单元格所在的`td`添加一个`qtip`，将单元格的内容放到里面就可以了。

extjs的qtip提示会有个小问题，也不知道是不是bug，如果value的值中包含了空格，横线等特殊符号的时候qtip显示的内容不完整，只能显示第一个空格之前的内容。为了避免这种情况可以用`xmp`标签将value包含起来：
`metadata.tdAttr = 'data-qtip="<xmp>' + value+ '</xmp>"';`

还有一种办法就是给grid添加一个鼠标移动事件，当鼠标移动到单元格内的时候取到单元格的内容，然后生成一个tooltip显示出来。代码如下：

```js
listeners:{
   'render': function(g) {    
       g.on("itemmouseenter", function(view,record,mode,index,e) {
           var view = g.getView();
           logGrid.tip = Ext.create('Ext.tip.ToolTip', {  
              target: view.el,
              delegate: view.getCellSelector(),
              trackMouse: true,
              renderTo: Ext.getBody(),
              listeners: {   
                  beforeshow: function updateTipBody(tip) {
                      tip.update(tip.triggerElement.innerHTML);
                  }  
              }  
           });  
       });    
   }  
}
```
