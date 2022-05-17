---
title:  ExtJs 中 gridpanel 分组后组名排序
date: 2013-12-02
comments: on
categories:  [ExtJs]
tags: [extjs, grid,分组,排序]
id: 201312021200

---

ExtJs 中对 gridpanel 分组后的组名进行排序，GroupingGrid 分组后是不能对组名再进行排序的，本文介绍了相关方法。

<!-- more -->

![group](//img.leense.site/post/2013/12/201312021200-1.jpg)

```js
/**
  * 定义降序的groupingStore
  */
var DescGroupingStore = Ext.extend(Ext.data.GroupingStore, {
groupDir : 'ASC',
groupBy : function(field, forceRegroup, direction) {
    direction = direction ? (String(direction)
              .toUpperCase() == 'DESC' ? 'DESC' : 'ASC')
              : this.groupDir;
    if (this.groupField == field
           this.groupDir == direction &amp;&amp; !forceRegroup) {
          return;
   }
   this.groupField = field;
   this.groupDir = direction;
   if (this.remoteGroup) {
       if (!this.baseParams) {
          this.baseParams = {};
       }
       this.baseParams['groupBy'] = field;
          this.baseParams['groupDir'] = direction;
       }
       if (this.groupOnSort) {
            this.sort(field, direction);
            return;
       }
       if (this.remoteGroup) {
            this.reload();
       } else {
            var si = this.sortInfo || {};
            if (si.field != field || si.direction != direction) {
                this.applySort();
            } else {
                this.sortData(field, direction);
            }
            this.fireEvent('datachanged', this);
        }
    },
    applySort : function() {
        Ext.data.GroupingStore.superclass.applySort.call(this);
        if (!this.groupOnSort && !this.remoteGroup) {
            if (this.groupField != this.sortInfo.field
                    || this.groupDir != this.sortInfo.direction) {
                this.sortData(this.groupField, this.groupDir);
            }
        }
    },
    applyGrouping : function(alwaysFireChange) {
        if (this.groupField !== false) {
            this.groupBy(this.groupField, true, this.groupDir);
            return true;
        } else {
            if (alwaysFireChange === true) {
                this.fireEvent('datachanged', this);
            }
            return false;
        }
    }
});
```

```js
/*************************调用***************************/
// 消息列表数据源
var messageStore = new DescGroupingStore({
  proxy: new Ext.data.HttpProxy({
    url: "listMessGrid.action"
  }),
  reader: myReader,
  groupDir: "DESC",
  groupField: "status",
  sortInfo: {
    field: "id",
    direction: "DESC"
  }
});
messageStore.load();
```

```js
/*****************在gridpanel中添加如下属性*************************************/
view: new Ext.grid.GroupingView({
  showGroupName: false,
  groupTextTpl: "{gvalue}:{text}",
  showGroupsText: "ddd"
});
```
