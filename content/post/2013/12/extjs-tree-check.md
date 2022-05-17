---
title:  ExtJs改变树节点的勾选状态
date: 2013-12-02
comments: on
categories:  [ExtJs]
tags: [extjs,tree,树,勾选]
id: 201312021500
---


今天系统中有处地方需要一个功能点击一个按钮后将树节点前的复选框去掉，变成没有选择的状态。网上搜索了半天，然后自己查查API，终于找到解决办法了，下面把方法贴出来。
<!-- more -->
在Extjs3.x和4.x版本中的处理方法是不一样的， 3.x版本中可以这样操作：

```js
node.attributes.checked=false;
node.getUI().toggleCheck(false);
```

这样就可以取消节点的check状态并且将页面上的勾去掉。

在ExtJs4中的方法如下：

```js
node.raw.checked=false;
node.set("checked",false);
```

这样同样可以达到效果！
