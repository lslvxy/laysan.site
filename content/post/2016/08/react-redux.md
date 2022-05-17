---
title:  React + Redux 入坑指南
date: 2016-08-08
comments: on
categories:  [Web]
tags: [React,Redux,Web]
id: 201608080930

---

React + Redux 基本入坑配置

<!-- more -->

# Redux

## 原理

**1. 单一数据源**

`all states ==>Store`

- 随着组件的复杂度上升（包括交互逻辑和业务逻辑），数据来源逐渐混乱，导致组件内部数据调用十分复杂，会产生数据冗余或者混用等情况。
- Store 的基本思想是将所有的数据集中管理，数据通过 Store 分类处理更新，不再在组件内放养式生长。

**2. 单向数据流**

`dispatch(actionCreator) => Reducer => (state, action) => state`

- 单向数据流保证了数据的变化是有迹可循且受控制的。
- 通过绑定 Store 可以确定唯一数据来源。
- actionCreator 通过 dispatch 触发，使组件内事件调用逻辑清晰，具体的事件处理逻辑不用放在组件写，保持 view 层的纯净。
- Reducer 通过判断不同的 actionType 处理不同数据更新，保证数据有秩序更新。

# React + Redux

## Action

- actionType 定义操作类型
- actionCreator 定义操作具体执行函数

### 1. Action&nbsp;基础写法

- actionType 提供给 Reducer 判断动作类型
- actionCreator 为可调用的执行函数，必须返回 actionType 类型

```js
// actionType
export const ACTION_TYPE = "ACTION_TYPE";

// actionCreator
let actionCreator = config => {
  return {
    type: ACTION_TYPE, // 必须定义 type
    config // 传递参数 => reducer
  };
};
```

### 2. Action 异步解决方法

- [redux-thunk](https://github.com/gaearon/redux-thunk?spm=5176.100239.blogcont58700.7.nE2wTr) 中间层做数据异步转换
- [redux-saga](https://github.com/yelouafi/redux-saga?spm=5176.100239.blogcont58700.8.nE2wTr) 使用 ES6 generator / yield

### 2.1 redux-thunk 使用方法

- **redux-thunk 配置**
  redux-thunk 为独立工具，需要另外安装，通过 redux 提供的中间件 applyMiddleware ，绑定到 store 中。

```js
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import reducers from "../reducers";

let store = createStore(reducers, applyMiddleware(thunk));
```

- **Action 使用 redux-thunk**
  获取数据方法在异步获取数据后需要再次调用接收方法接收数据。

```js
// 接收方法
let receiveSomething = res => {
  return {
    type: RECEIVE_SOME,
    res
  };
};

// 获取数据方法
export let fetchSomething = args => {
  return dispatch => {
    return fetch(args).then(res => {
      return dispatch(receiveSomething(res));
    });
  };
};
```

## Reducer

- 引入 Action 中定义好的 actionType
- 传入 初始数据 和 actionType 后，返回更新数据`(initialState, action) => newState`

### Reducer 基础写法

#### 1.依据不同执行 ActionType 直接更新状态

```js
import { ACTION_A, ACTION_B } from '../actions';

let initialState = { ... }

function example(state = initialState, action) {
    switch(action.type) {
        case ACTION_A:
          return Object.assign({}, state, action.config)
        case ACTION_B:
          return Object.assign({}, state, action.config)
    }
}

```

#### 2.对 Action 传递的数据多加一层处理

```js
let doSomething = config => {
  let { a, b } = config;
  // do something with a, b
  return { a, b };
};

function example(state = initialState, action) {
  switch (action.type) {
    case ACTION_TYPE:
      return Object.assign({}, state, doSomething(action.config));
  }
}
```

#### 3.合并多个 Reducer

通过 redux 提供的 combineReducers 将不同处理逻辑的 reducer 合并起来。

```js
import { combineReducers } from 'redux';

export default combineReducers({
  reducerA,
  reducerB
});

// or

export let reducer = (state = initialState, action) {
    a: processA(state.a, action),
    b: processB(state.b, action)
}

```

## Store

### 1. 将 Store 绑定 React

使用 react-redux 提供的 Provider 可以将 Store 注入到 react 中。

Store 将合并后的 reducers 通过 createStore 创建，此外下面示例代码还使用中间件加入了一层 react-thunk 处理。

```js
import ReactDOM from "react-dom";
import { createStore, applyMiddleware } from "redux";
import { Provider } from "react-redux";
import thunk from "redux-thunk";
import reducers from "./reducers";

let store = createStore(reducers, applyMiddleware(thunk));

ReactDOM.render(
  <Provider store={store}>// ...</Provider>,
  document.querySelector("#app")
);
```

### 2. 将 state 绑定到 Component

使用 react-redux 提供的 connect 方法 将组件和所需数据绑定。

**需要注意的是**，Store 创建时接收的是合并后的 reducers, 因此不同 reducer 上的处理数据绑定在了不同 reducer 对象上，而不是全部挂载在 Store 上。

mapStateToProps 将组件内部所需数据通过 props 传入组件内部。更多绑定机制，具体可参考[connect](http://cn.redux.js.org/docs/react-redux/api.html?spm=5176.100239.blogcont58700.9.nE2wTr)

```js
import React, { Component } from "react";
import { connect } from "react-redux";

class ComponentA extends Component {
  //...
}

let mapStateToProps = state => {
  // attention !!!
  let { reducerA, reducerB } = state;
  return {
    propA: reducerA.propA,
    propB: reducerB.propB
  };
};

export default connect(mapStateToProps)(ComponentA);
```

## Component

### 1. 概念

> React bindings for Redux embrace the idea of separating presentational and container components.
>
> Redux 的 React 绑定库包含了 **容器组件和展示组件相分离** 的开发思想。

- Presentational Components 展示型组件
- Container Components 容器型组件

展示型组件和容器型组件的区别在官方文档中已经给出很详细的解释了，但是中文文档的翻译有误，所以直接看英文比较更容易懂。

|                | Presentational Components        | Container Components                           |
| -------------- | -------------------------------- | ---------------------------------------------- |
| Purpose        | How things look (markup, styles) | How things work (data fetching, state updates) |
| Aware of Redux | No                               | Yes                                            |
| To read data   | Read data from props             | Subscribe to Redux state                       |
| To change data | Invoke callbacks from props      | Dispatch Redux actions                         |
| Are written    | By hand                          | Usually generated by React Redux               |

组件类型区分的模糊点在于怎么界定组件的内部功能规划。如果判定一个组件为展示型组件，那么它所需数据和处理方法都应该从父级传入，保持组件内部“纯净”。

在实际开发中，一个组件的逻辑跟业务紧密相关。如果需要将数据和方法从外部传入，那么父级组件所做的事情会很多，多重的子组件也会把父级逻辑弄乱，这就不是 redux 的初衷了。

中文文档翻译的意思是：容器组件应该为路由层面的组件，但这样既不符合实际开发需要，也违背了 redux 思想。真正界定两种组件的因素是：

- **展示型组件：** 类似纯模板引擎，外加一层样式渲染，只负责渲染从 props 传进来的数据或者监听事件和父组件做小联动。它是“纯净”的，不需要使用到 Redux 的一套规则。
- **容器型组件：** 需要异步获取数据，更新组件状态等等。需要跟业务逻辑打交道的组件都可以认为是容器组件。这些逻辑的复杂性需要将数据整合到 Store 里统一管理。

### 2. Component 基础写法

- **组件渲染完成后调用 Action**

当组件 connect 后，dispatch 方法已经注入到 props 中，所以触发 Action 可以从 props 获取 dispatch 方法。

```js
import React, { Component } from "react";
// actionCreator
import { actionA, actionB } from "actions/actionA";

class ComponentA extends Component {
  constructor(props) {
    super(props);
  }
  componentDidMount() {
    let { dispatch } = this.props;
    dispatch(actionA());
  }
}
export default connect()(ComponentA);
```

- **组件模板内调用 Action**

组件内部所需的渲染数据都已经绑定在了 props 上，直接获取即可。

**需要注意的是**，在事件监听中触发 Action，需要用一个匿名函数封装，否则 React 在渲染时就会执行事件绑定事件，而不是当事件发生再执行。

```js
render() {
  let { dispatch, propA, propB } = this.props;

    return (
      <section>
        // Attention !!!
        <input type="text" onClick={(ev) => dispatch(actionB(ev))} />
        <p className={propA}>{propB}</p>
      </section>
    )
}
```

- **容器组件传递方法**

容器型组件需要连接 Redux，使用 dispatch 触发 actionCreator。

展示型组件需要用到的方法调用在容器型组件内定义好，通过 props 传入到展示型组件中。

```js
// get actionCreator
import { actionA } from "./actions/actionA";

class Parent extends Component {
  handleCallback(data) {
    // use dispatch
    let { dispatch } = this.props;
    dispatch(actionA(data));
  }
  render() {
    return <Child onSomethingChange={this.handleCallback} />;
  }
}
// connet Redux
export default connect()(Parent);
```

- **展示组件接收 props**

展示型组件不需要用到 Redux 的一切，它的 props 仅仅存在于父级传入的数据和方法。

```js
// don't need action/dispatch/connect
class Child extends Component {
  handleSomething(data) {
    // handle anything with props
    this.props.onSomethingChange(data);
  }
  render() {
    return (
      // just markup & style
      <input onChange={handleSomething} />
    );
  }
}
```

# Conclusion

图示箭头代表各概念之间的相互关系，不代表数据流。（ 能理解下面这张图，这篇文章就没白看了 -。- ）

![](//img.leense.site/post/2016/08/201608080930-1.png)

**参考文档**

- [Redux 英文文档](http://redux.js.org/?spm=5176.100239.blogcont58700.11.nE2wTr)
- [Redux 中文文档](http://cn.redux.js.org/index.html?spm=5176.100239.blogcont58700.12.nE2wTr)

END.
