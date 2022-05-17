---
title:  JavaScript 的装饰器：它们是什么及如何使用
date: 2017-06-23
comments: on
categories:  [Web]
tags: [JavaScript,Decorator,装饰器]
id: 201704052130
no_image: https://source.unsplash.com/random/800x600
description: 装饰器的流行应该感谢在Angular 2+中使用，在Angular中，装饰器因TypeScript能使用。但是在JavaScript中，还处于提议阶段。本文将介绍装饰器是什么，及装饰器如何让代码更加简洁和容易理解。
---
装饰器的流行应该感谢在Angular 2+中使用，在Angular中，装饰器因TypeScript能使用。但是在JavaScript中，还处于提议阶段。本文将介绍装饰器是什么，及装饰器如何让代码更加简洁和容易理解。

# 什么是装饰器

装饰器是用一个代码包装另一个代码的简单方式。

这个概念与之前所听过的函数复合和高阶组件相似。

这已经用于很多情况，就是简单的将一个函数包装成另一个函数：

```js
function doSomething(name) {
  console.log('Hello, ' + name);
}

function loggingDecorator(wrapped) {
  return function() {
    console.log('Starting');
    const result = wrapped.apply(this, arguments);
    console.log('Finished');
    return result;
  }
}

const wrapped = loggingDecorator(doSomething);
```

上个例子产生新函数`wrapped`，此函数与`doSomething`做同样事情，但是他们不同在于在包装函数之前和之后输出一些语句。

```js
doSomething('Graham');
// Hello, Graham
wrapped('Graham');
// Starting
// Hello, Graham
// Finished
```

# 如何使用JavaScript装饰器

JavaScript中装饰器使用特殊的语法，使用`@`作为标识符，且放置在被装饰代码之前。

> **注意：**现在装饰器还处于提议阶段，意味着还有可以变化之处

可以放置许多装饰器在同样代码之前，然后解释器会按照顺序相应执行

```js
@log()
@immutable()
class Example {
  @time('demo')
  doSomething() {

  }
}
```

上例中定义了一个类，采用了三个装饰器：两个用于类本身，一个用于类的属性：

*   `@log`能记录所有所有访问类
*   `@immutable`让类不可变-也许新实例调用了`Object.freeze`
*   `@time`会记录一个方法从执行到输出一个独特标签

现在，虽然现在浏览器或Node还没支持。但是如果使用Babel，能使用 [transform-decorators-legacy](https://github.com/loganfsmyth/babel-plugin-transform-decorators-legacy)插件使用装饰器。

> 插件中使用legacy是因为Babel 5支持处理装饰器，但是它也许会跟最终的标准有区别，所以才使用legacy这个词。

# 为什么使用装饰器

函数复合在JavaScript已经成为可能，但是它相当困难或不可能用于另一个代码（如类或类属性）。

装饰器提议可以用于类或属性，未来JavaScript版本可能会增加用于其他地方。

装饰器也考虑到采用较为简洁的语法。

# 不同类型的装饰器

现在，装饰器只支持类和类属性，这包含属性、方法、get函数和set函数

装饰器只会在程序第一次运行时执行一次，装饰的代码会被返回的值代替

## 类属性装饰器

属性装饰器适用于类的单独成员-无论是属性、方法、get函数或set函数。
装饰器函数调用三个参数：

*   target-被修饰的类
*   name-类成员的名字
*   descriptor-成员描述符。对象会将这个参数传给`Object.defineProperty`

`@readonly`是经典的例子：

```js
function readonly(target, name, descriptor) {
  descriptor.writable = false;
  return descriptor;
}
```

上例会将成员描述符中的`writable`设为`false`。

接着用于类中属性：

```js
class Example {
  a() {}
  @readonly
  b() {}
}

const e = new Example();
e.a = 1;
e.b = 2;
// TypeError: Cannot assign to read only property 'b' of object '#<Example>'
```

但是我们可以做的更好，可以用别的形式代替装饰函数。例如，记录所有的输入和输出：

```js
function log(target, name, descriptor) {
  const original = descriptor.value;
  if (typeof original === 'function') {
    descriptor.value = function(...args) {
      console.log(`Arguments: ${args}`);
      try {
        const result = original.apply(this, args);
        console.log(`Result: ${result}`);
        return result;
      } catch (e) {
        console.log(`Error: ${e}`);
        throw e;
      }
    }
  }
  return descriptor;
}
```

注意我们使用了扩展运算符，会自动将所有参数转为数组。

```js
class Example {
    @log
    sum(a, b) {
        return a + b;
    }
}

const e = new Example();
e.sum(1, 2);
// Arguments: 1,2
// Result: 3
```

可以让装饰器获取一些参数，例如重写`log`装饰器如下：

```js
function log(name) {
  return function decorator(t, n, descriptor) {
    const original = descriptor.value;
    if (typeof original === 'function') {
      descriptor.value = function(...args) {
        console.log(`Arguments for ${name}: ${args}`);
        try {
          const result = original.apply(this, args);
          console.log(`Result from ${name}: ${result}`);
          return result;
        } catch (e) {
          console.log(`Error from ${name}: ${e}`);
          throw e;
        }
      }
    }
    return descriptor;
  };
}
```

这与之前的`log`装饰器相同，只是利用了外部函数的`name`参数。

```js
class Example {
  @log('some tag')
  sum(a, b) {
    return a + b;
  }
}

const e = new Example();
e.sum(1, 2);
// Arguments for some tag: 1,2
// Result from some tag: 3
```

# 类装饰器

类装饰器用于整个类，装饰器函数的参数为被装饰的构造器函数。

注意只用于构造器函数，而不适用于类的每个实例。这就意味着如果想控制实例，就必须返回一个包装版本的构造器函数。

通常，类装饰器没什么用处，因为你所需要做的，同样可以用一个简单函数来处理。你所做的只需要在结束时返回一个新的构造函数来代替类的构造函数。

回到我们记录那个例子，编写一个记录构造函数参数：

```js
function log(Class) {
  return (...args) => {
    console.log(args);
    return new Class(...args);
  };
}
```

这里接收一个类作为参数，返回新函数作为构造器。此函数打印出参数，返回这些参数构造的实例。

例如：

```js
@log
class Example {
  constructor(name, age) {
  }
}

const e = new Example('Graham', 34);
// [ 'Graham', 34 ]
console.log(e);
// Example {}
```

构造`Example`类时会输出提供的参数，构造值`e`也确实是`Example`的实例。

传递参数到类装饰器与类成员一样。

```js
function log(name) {
  return function decorator(Class) {
    return (...args) => {
      console.log(`Arguments for ${name}: args`);
      return new Class(...args);
    };
  }
}

@log('Demo')
class Example {
  constructor(name, age) {}
}

const e = new Example('Graham', 34);
// Arguments for Demo: args
console.log(e);
// Example {}
```

# 真实例子

## Core decorators

[Core decorators](https://www.npmjs.com/package/core-decorators)是一个库，提供了几个常见的修饰器，通过它可以更好地理解修饰器。

想理解此库，也可以去看看阮老师的关于[此库的介绍](http://es6.ruanyifeng.com/#docs/decorator#core-decorators-js)

## React

React广泛运用了高阶组件，这让React组件成为一个函数，并且能包含另一个组件。
使用装饰器是不错的替代法，例如，Redux库有一个`connect`函数，用于连接React组件和React store。

通常，是这么使用的：

```js
class MyReactComponent extends React.Component {}

export default connect(mapStateToProps, mapDispatchToProps)(MyReactComponent);
```

然而，可以使用装饰器代替：

```js
@connect(mapStateToProps, mapDispatchToProps)
export default class MyReactComponent extends React.Component {}
```

# 参考资料

[JavaScript Decorators: What They Are and When to Use Them](https://www.sitepoint.com/javascript-decorators-what-they-are/)
[阮老师ES6入门-修饰器](http://es6.ruanyifeng.com%2F%23docs%2Fdecorator)