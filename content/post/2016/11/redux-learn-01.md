---
title:  Redux教程1：环境搭建，初写Redux
date: 2016-11-13
comments: on
categories:  [Web]
tags: [React,Redux,Web]
id: 201611130930
---


如果将React比喻成士兵的话，你的程序还需要一位将军，去管理士兵（的状态），而Redux恰好是一位好将军，简单高效；

相比起React的学习曲线，Redux的稍微平坦一些；本系列教程，将以“红绿灯”为示例贯穿整个demo，希望能让用户快速理解&学习Redux。
<!-- more -->

强烈推荐 [Redux 中文文档](http://camsong.github.io/redux-in-chinese/index.html)，本redux教程所有的材料和思路都来源于此；

这个系列拆分成3篇文章，最后获得的效果图为：

[![result](https://gw.alicdn.com/tps/TB1HYmUKVXXXXXhXXXXXXXXXXXX-224-316.gif "result")](https://gw.alicdn.com/tps/TB1HYmUKVXXXXXhXXXXXXXXXXXX-224-316.gif)
（这个是gif图，如果没动画请点击在新窗口打开）

红绿灯初始状态是 #绿灯5s#，继而循环 #黄灯3s# -> #红灯7s# -> #绿灯5s# -> #黄灯3s# -> ...

## 1、Redux简介

在Redux中，最为核心的概念就是 `state`、`action` 、`reducer` 以及 `store`，单词大家都懂，就是初学者不知道该怎么用。

以常见的红路灯为例，将其应用到Redux中：

*   `action`：就是灯的变化，"红变绿"等，用名词表述
*   `state`：就是灯的名字，红灯、绿灯等，用名词表述
*   `reducer`：就是灯的变化规则，红灯之后是绿灯等，用状态转移表述，归根到底也是名词
*   `store`：就像是交警，执行上述的交通规则；

简单的说，Redux所想表达的就是这些内容，所以它的学习曲线不会很陡。对于程序员来讲，阅读代码会比阅读文字舒服，那么我们如何简单地用redux实现。


## 2、文件夹结构

### 2.1、安装依赖

创建符合redux风格的文件夹结构：

```js
mkdir actions constants components layouts reducers stores tests views
touch server.js index.js webpack.config.js
```

这些文件夹结构也是借鉴自官网redux的todos示例；

然后安装依赖：

```js
npm init
npm install --save koa koa-handlebars koa-router react react-dom react-redux classnames
npm install --save-dev webpack webpack-dev-server webpack-hot-middleware babel-core babel-loader babel-plugin-react-transform style-loader less-loader css-loader extract-text-webpack-plugin babel-preset-es2015 babel-preset-react
```


最终的文件夹结构为：

[![file structor](https://gw.alicdn.com/tps/TB1lE1DKVXXXXaDXFXXXXXXXXXX-170-352.jpg "file structor")](https://gw.alicdn.com/tps/TB1lE1DKVXXXXaDXFXXXXXXXXXX-170-352.jpg)

### 2.2、配置开发环境

这里需要启用两个服务器，一个是webpack服务器，专门用于转换代码；另外一个是web应用服务器，响应客户端的请求


```js
var path = require('path');
var fs = require('fs');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// 遍历目录
var searchDir = ['components','app']; // 需要webpack打包的目录
var entry = {};

searchDir.forEach(function(dir){
  var srcBasePath = path.join(__dirname, './', dir);
  var files = fs.readdirSync(srcBasePath);
  var ignore = ['.DS_Store']; // 忽略某些文件夹
  files.map(function (file) {

    if (ignore.indexOf(file) < 0) {
      entry[dir+'/'+file] = path.join(srcBasePath, file, 'index.js');

      var demofile = path.join(srcBasePath, file, 'demo.js');
      if(fs.existsSync(demofile)){
        entry[dir+'/'+file + '/demo'] = demofile;
      }

      var reduxfile = path.join(srcBasePath, file, 'redux.js');
      if(fs.existsSync(reduxfile)){
        entry[dir+'/'+file + '/redux'] = reduxfile;
      }
    }

  });
});

Object.keys(entry).forEach(function (key) {
  entry[key] = [entry[key], 'webpack-hot-middleware/client'];
});

module.exports = {
  devtool:'cheap-module-eval-source-map',
  entry :entry,
  output:{
    path:path.join(__dirname,'dist'),
    filename:'[name].js',
    publicPath:'/static/'
  },
  plugins:[
    new ExtractTextPlugin("[name]/index.css"),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  module:{
    loaders:[{
      test:/\.js$/,
      loader:'babel-loader',
      exclude:/node_modules/,
      include:__dirname,
      query:{
        presets: ['es2015','react']
      }
    },{
      test: /\.less$/,
      loader: ExtractTextPlugin.extract('style-loader','css-loader!less-loader'),
      exclude: /node_modules/
    }]
  }
}
```

注意Babel 6的配置和上一个版本有很大的不同；详见：[Setting up Babel 6](http://babeljs.io/blog/2015/10/31/setting-up-babel-6/)

这是webpack配置项，接下来专门起一个nodejs程序提供webpack服务：

`server.js`：

```js
var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.config');

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  stats: { colors: true },
  historyApiFallback: true
}).listen(3009, 'localhost', function (err, result) {
  if (err) {
    console.log(err);
  }

  console.log('Listening at localhost:3009');
});

```

此webpack服务专门用于整合前端资源，顺带使用babel转换ES6的JS代码；这里的含义就不多说了，可以参考以前的文章 [Webpack](http://www.atatech.org/articles/37601)；

使用koa作为web服务器，因为测试所以比较简单，用了最基本的代码快速搭建：

```js
var koa = require('koa');
var router = require('koa-router')();
var handlebars = require("koa-handlebars");
var app = koa();
var port = 3000;

// 使用handlerbars作为模板文件
app.use(handlebars({
  defaultLayout: "index"
}));

// 定义路由
router.get("/", function *(next) {
  yield this.render('index',{
    ---
title: 'Redux示例-交通灯',
    name:'交通灯示例'
  });
});

// 定义应用路由
router.get('app','/app/:name',function*(next){
  this.appName = this.params.name || 'index'; // 应用名字

  yield this.render('app/'+this.appName,{
    ---
title: '应用',
    filename:this.appName
  });

})

// 定义demo路由
router.get('demo','/:name/:type', function *(next) {
  this.demoName = this.params.name || 'demo'; // 获取demo名称
  this.demoType = this.params.type; // 获取文件类型，'demo' 或者 'redux'
  yield this.render(this.demoName + '/index',{
    ---
title: '示例',
    filename:this.demoType
  });
});

// 启用路由
app
  .use(router.routes())
  .use(router.allowedMethods());

// 监听端口
app.listen(port, function(error) {
  if (error) {
    console.error(error)
  } else {
    console.info("==>   监听端口 %s. 请在浏览器里打开 http://localhost:%s/.", port, port)
  }
})

```

好了，在命令行里开启这两个服务吧：

```js
nodemon server.js & nodemon --harmony index.js

```

在package.json中的`scripts`增加一条配置：`"start": "nodemon server.js & nodemon --harmony index.js"`，以后就可以使用 `npm start` 命令同时启动两个服务了；

这里使用了`nodemon`应用程序，方便修改后快速启动，该程序可通过`npm install -g nodemon`安装

## 3、开始Redux吧

环境搭建好了，我们就依据最开始的设定用redux搭建红绿灯示例。

先创建所需要的文件：

```js
mkdir actions/light reducers/light stores/light components/light

touch constants/TrafficLight.js actions/light/index.js reducers/light/index.js stores/light/index.js components/light/redux.js

```

### 3.1、Actions

Action 本质是 *JavaScript 普通对象* action 内必须使用一个 *字符串类型* 的 `type` 字段来表示将要执行的动作。多数情况下，type 会被定义成字符串常量。当应用规模越来越大时，建议使用单独的模块或文件来存放 action。

在 `constants/TrafficLight.js`中定义actions的名称，使用 `const` 修饰防止被修改：

```js
export const CHANGE_GREEN = 'CHANGE_GREEN'
export const CHANGE_YELLOW = 'CHANGE_YELLOW'
export const CHANGE_RED = 'CHANGE_RED'

```

然后在 `actions/light/index.js` 文件，定义 *Actions* 对象：

```js
import * as lights from '../../constants/TrafficLight'

export function changeGreen(){
 return {type:lights.CHANGE_GREEN}
}

export function changeYellow(){
 return {type:lights.CHANGE_YELLOW}
}

export function changeRed(){
 return {type:lights.CHANGE_RED}
}

```

这里的 *{type:lights.CHANGE_GREEN}* 等就是Redux的 *action对象*（就是这么简单....）， 而对应的 `changeGreen`方法则称为 *action创建函数* ；

详细的概念及作用请参考Redux的中文文档 [Actions](http://camsong.github.io/redux-in-chinese/docs/basics/Actions.html)


### 3.2、Reducer

正所谓“不以规矩，不能方圆”，万物的运作都要符合规律，Reducer 就是描述各状态之间流转的 *规律*：

*   当红灯时，过n1秒会触发 `CHANGE_GREEN` 事件，灯编程绿色的
*   当绿灯时，过n2秒会触发 `CHANGE_YELLOW` 事件，灯编程黄色的
*   当黄灯时，过n3秒会触发 `CHANGE_RED` 事件，灯编程红色的
*   ...周而复始...

继续在 `reducers/light/index.js`文件，描述不同等之间的转移：

```js
import {CHANGE_GREEN, CHANGE_YELLOW, CHANGE_RED} from '../../constants/TrafficLight'

// 定义初始化状态，初始化状态是常量
// 初始状态是红灯
const initState = {
 color:'red',
 time:'7' // 持续时间20ms
}

// 定义灯转换的reducer函数
export default function light(state=initState,action){
 switch(action.type){
   case CHANGE_GREEN:
     return {
       color:'green',
       time:'5'
     }

   case CHANGE_YELLOW:
     return {
       color:'yellow',
       time:'3'
     }

   case CHANGE_RED:
     return Object.assign({},initState);

   default:
     return state
 }
}

```

这里的`switch`语句就是典型的用于表述 *状态转移* 逻辑的代码结构，自己尝试写状态机的同学应该深有体会；


### 3.3、Store

有了交规还不行，得有付诸具体行动的载体 —— 交通信号灯 才行，在 `stores/light/index.js` ：

```js
import {createStore} from 'redux'
import lightReducer from '../../reducers/light/'

export default function lightStore(initState){
 return createStore(lightReducer,initState); // 初始化创建
}

```

关键就那句`createStore`函数，接受 `reducer`（交通规则）和 `initState` （初始状态，灯的初始状态是红灯）作为参数；

这里的 “交通信号灯” 也是一种类别，并不是具体指 “灯” —— 额，希望你能理解我想表述的...

自此，恭喜你你已经成功实施了 Redux 的必要规范了，接下来我们检验一下是否正如你所愿；

此节中我们先简单的实施一下，后续文章再补充细节

## 4、检查能否运行

按照上面创建的一系列JS文件，你已经基于 `Redux` 完成了红绿灯的规则效果，那怎么检验呢？

来，拿一个红绿灯过来！

接通电源，给这个灯 *发送* 事件（类似于dom中的“触发事件”），假设事件的 `type` 依次是 **CHANGE_GREEN** 、**CHANGE_GREEN**，看看事件结束之后的状态是否符合期望。

### 4.1、编写demo文件

编写 `components/light/demo.js`：

```js
import lightStore from '../../stores/light'
import {changeGreen, changeYellow, changeRed} from '../../actions/light'

let store = lightStore();

let unsubscribe = store.subscribe(() =
  console.log(store.getState())
);

store.dispatch(changeGreen());
store.dispatch(changeYellow());
store.dispatch(changeRed());

```

### 4.2、编写view模板

上面的都是 `redux` 的功能代码，现在为了方便在浏览器查看，使用 `koa` 搭建一个简单的服务器；使用`handlerbars` 作为模板引擎，使用下列方式创建模板和视图

在 `layouts/index.hbs` 中编写母模板，其中的 `{@body}` 是留给子模板填充的

```js
<!DOCTYPE html>
<html>
  <head>
    <title{{title}}</title>
  </head>
  <body>
    {@body}
  </body>
</html>

```

在`views/light/index.hbs`中编写子模板内容，程序会自动将里面的内容自动替换上述模板中的 `{@body}` 占位符：

```js
<link rel="stylesheet" href="http://localhost:3009/static/components/light/index.css">

<h1交通灯示例</h1>
<div id="demo"</div>

<script src="http://localhost:3009/static/components/light/{{filename}}.js"</script>

```



### 4.3、查看结果

使用`npm start`开启两个服务，在浏览器URL里输入 `http://localhost:3000/light/demo` ，打开`console`，你将看到以下字符串：

```js
Object {color: "green", time: "5"}
Object {color: "yellow", time: "3"}
Object {color: "red", time: "7"}

```

你get到了什么？全程你都没有涉及到红绿灯的UI，但仿佛却有红绿灯的即视感，状态完全可控可预见！redux 其实就是帮你实现了一套状态机，且逻辑清晰。由于不涉及UI，所以非常也很利于单元测试。

如果启动的时候 webpack 报错：**You may need an appropriate loader to handle this file type** ，请见[use Webpack with Babel to compile ES6 assets,](http://stackoverflow.com/questions/33469929/you-may-need-an-appropriate-loader-to-handle-this-file-type-with-webpack-and-b) 这里的解决方案，因为Babel 6是相比以前是一个重大升级，配置按模块方式加载了；


 ## 5、总结

 在继续后面的章节之前，稍微整理一下上面的逻辑，使用图表描述会更加清晰些：

 [![light](https://gw.alicdn.com/tps/TB1HK1IKVXXXXbRXpXXXXXXXXXX-1043-623.jpg "light")](https://gw.alicdn.com/tps/TB1HK1IKVXXXXbRXpXXXXXXXXXX-1043-623.jpg)

 这简单的图里面还涉及到 `倒计时的状态`，此篇文章为减少复杂度，方便读者快速理解Redux的基本概念，并不牵涉倒计时的状态，后续文章示例自然会将车的状态考虑进去；

 将图中的`Action` `Reducer`以及 `Store` 和上述代码对照，一切都是那么合乎逻辑，自然而然；

 本文更多的是讲解如何快速上手Redux，并没有对其中的语法和概念进行过多的解释

 *   一方面是语法的解释，中文文档里面的解释很全面，我没有自信能够超越它；
 *   另一方面让新手对这些简单的代码中的陌生概念(诸如`combineReducers` `dispatch`等）产生疑惑，带着问题来探索答案，加深印象

 这里将上述操作流程大致绘制一下：

 [![workflow](https://gw.alicdn.com/tps/TB1PEqxKVXXXXXuXVXXXXXXXXXX-1556-817.jpg "workflow")](https://gw.alicdn.com/tps/TB1PEqxKVXXXXXuXVXXXXXXXXXX-1556-817.jpg)

 顺带提及一下Redux的三大原则，看一眼就好，后续用多了自然会记住：

 [![three princel](https://gw.alicdn.com/tps/TB1n_uzKVXXXXXBXVXXXXXXXXXX-912-388.jpg "three princel")](https://gw.alicdn.com/tps/TB1n_uzKVXXXXXBXVXXXXXXXXXX-912-388.jpg)


 最后，非常推荐`redux`库，里面有很多示例可以参考，比如经典的 `todos` 例子：

  ```js
  git clone https://github.com/rackt/redux.git

  cd redux/examples/todomvc
  npm install
  npm start

  open http://localhost:3000/

  ```

  该示例包含：

  *   Redux 中使用两个 reducer 的方法
  *   嵌套数据更新
  *   测试代码

  更多参考：[Redux示例](http://camsong.github.io/redux-in-chinese/docs/introduction/Examples.html)
