---
title:  iview-admin 2.x 兼容IE11的方法
date: 2019-01-28
comments: on
categories:  [Web]
tags: [Web ,Vue , ]
id: 201901282330
no_image: https://source.unsplash.com/random/800x600
description: iview-admin 2.x 兼容IE11的方法
---


最近使用iview-admin搭建的项目突然说要兼容ie,瀑汗.经过一番查阅资料,暂时找到一个可行的方法.记录如下

一般开源项目遇到问题首先想到去Issue中去寻找答案,兼容IE肯定是个普遍问题,issue中已经有很多类似问题和解决方案了.[https://github.com/iview/iview-admin/issues?utf8=%E2%9C%93&q=is%3Aissue+ie](https://github.com/iview/iview-admin/issues?utf8=%E2%9C%93&q=is%3Aissue+ie)

整理了一下本人成功兼容IE11 的方案:

1. 更改webpack-dev-server版本为2.71

`npm install --save-dev webpack-dev-server@2.7.1 `

2. 安装@babel/polyfill 

`npm install --save @babel/polyfill`

3. main.js代码最前面加入

`import '@babel/polyfill'`


4. main.js相关的语言包全部删除

```
1.main.js中的以下三部分注释掉：
//import i18n from '@/locale'

Vue.use(iView, {
// i18n: (key, value) => i18n.t(key, value)
})

new Vue({
el: '#app',
router,
// i18n,
store,
render: h => h(App)
})

2.还需要把components\main下的：

// this.setLocal(this.$i18n.locale)
两段注释掉
```

5. 修改配置文件

```
编辑.babelrc
{
  "presets": [["@vue/app", { "useBuiltIns": "entry" }]]
}

编辑vue.config.js

  transpileDependencies: ['tree-table-vue', 'iview'],

  chainWebpack: config => {
    config.entry('polyfill').add('@babel/polyfill')
    config.resolve.alias
      .set('@', resolve('src')) // key,value自行定义，比如.set('@@', resolve('src/components'))
      .set('_c', resolve('src/components'))
  },

```

6. 删除TreeTable依赖

TreeTable 插件不兼容ie需要注释掉

```
在main.js注释掉

// import TreeTable from 'tree-table-vue'
// import VOrgTree from 'v-org-tree'

以及

// Vue.use(TreeTable)
// Vue.use(VOrgTree)


```


