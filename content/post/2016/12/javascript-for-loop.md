---
title:  深入了解 JavaScript 中的 for 循环
date: 2016-12-12
comments: on
categories:  [Web]
tags: [JavaScript,For]
id: 201612121330
no_image: https://source.unsplash.com/random/800x600
description:  深入了解 JavaScript 中的 for 循环
---

在[ECMAScript5（简称 ES5）](https://link.zhihu.com/?target=http%3A//ecma-international.org/ecma-262/5.1/)中，有三种 for 循环，分别是：

*   简单for循环
*   for-in
*   forEach

在2015年6月份发布的[ECMAScript6（简称 ES6）](https://link.zhihu.com/?target=https%3A//people.mozilla.org/%7Ejorendorff/es6-draft.html)中，新增了一种循环，是：

*   for-of

下面我们就来看看这 4 种 for 循环。

<!-- more -->

## 简单 for 循环

下面先来看看大家最常见的一种写法：

```js
const arr = [1, 2, 3];
for(let i = 0; i　< arr.length; i++) {
    console.log(arr[i]);
}
```

当数组长度在循环过程中不会改变时，我们应将数组长度用变量存储起来，这样会获得更好的效率，下面是改进的写法：

```js
const arr = [1, 2, 3];
for(let i = 0, len = arr.length; i < len; i++) {
    console.log(arr[i]);
}
```

## for-in

通常情况下，我们可以用 for-in 来遍历一遍数组的内容，代码如下：

```js
const arr = [1, 2, 3];
let index;
for(index in arr) {
    console.log("arr[" + index + "] = " + arr[index]);
}
```

一般情况下，运行结果如下：

```js
arr[0] = 1
arr[1] = 2
arr[2] = 3
```

但这么做往往会出现问题。

**for-in 的真相**

for-in 循环遍历的是对象的属性，而不是数组的索引。因此， for-in 遍历的对象便不局限于数组，还可以遍历对象。例子如下：

```js
const person = {
    fname: "san",
    lname: "zhang",
    age: 99
};
let info;
for(info in person) {
    console.log("person[" + info + "] = " + person[info]);
}
```

结果如下：

```js
person[fname] = san
person[lname] = zhang
person[age] = 99
```

需要注意的是， for-in 遍历属性的顺序并不确定，即输出的结果顺序与属性在对象中的顺序无关，也与属性的字母顺序无关，与其他任何顺序也无关。

**Array 的真相**

Array 在 Javascript 中是一个对象， Array 的索引是属性名。事实上， Javascript 中的 “array” 有些误导性， Javascript 中的 Array 并不像大部分其他语言的数组。首先， Javascript 中的 Array 在内存上并不连续，其次， Array 的索引并不是指偏移量。实际上， Array 的索引也不是 Number 类型，而是 String 类型的。我们可以正确使用如 arr[0] 的写法的原因是语言可以自动将 Number 类型的 0 转换成 String 类型的 “0″ 。所以，在 Javascript 中从来就没有 Array 的索引，而只有类似 “0″ 、 “1″ 等等的属性。有趣的是，每个 Array 对象都有一个 length 的属性，导致其表现地更像其他语言的数组。但为什么在遍历 Array 对象的时候没有输出 length 这一条属性呢？那是因为 for-in 只能遍历“可枚举的属性”， length 属于不可枚举属性，实际上， Array 对象还有许多其他不可枚举的属性。

现在，我们再回过头来看看用 for-in 来循环数组的例子,我们修改一下前面遍历数组的例子：

```js
const arr = [1, 2, 3];
arr.name = "Hello world";
let index;
for(index in arr) {
    console.log("arr[" + index + "] = " + arr[index]);
}
```

运行结果是：

```js
arr[0] = 1
arr[1] = 2
arr[2] = 3
arr[name] = Hello world
```

我们看到 for-in 循环访问了我们新增的 “name” 属性，因为 for-in 遍历了对象的所有属性，而不仅仅是“索引”。同时需要注意的是，此处输出的索引值，即 “0″、 “1″、 “2″不是 Number 类型的，而是 String 类型的，因为其就是作为属性输出，而不是索引。那是不是说不在我们的 Array 对象中添加新的属性，我们就可以只输出数组中的内容了呢？答案是否定的。因为 for-in 不仅仅遍历 array 自身的属性，其还遍历 array 原型链上的所有可枚举的属性。下面我们看个例子：

```js
Array.prototype.fatherName = "Father";
const arr = [1, 2, 3];
arr.name = "Hello world";
let index;
for(index in arr) {
    console.log("arr[" + index + "] = " + arr[index]);
}
```

运行结果是：

```js
arr[0] = 1
arr[1] = 2
arr[2] = 3
arr[name] = Hello world
arr[fatherName] = Father
```

写到这里，我们可以发现 for-in 并不适合用来遍历 Array 中的元素，其更适合遍历对象中的属性，这也是其被创造出来的初衷。却有一种情况例外，就是稀疏数组。考虑下面的例子：

```js
let key;
const arr = [];
arr[0] = "a";
arr[100] = "b";
arr[10000] = "c";
for(key in arr) {
    if(arr.hasOwnProperty(key)  &&    
        /^0$|^[1-9]\d*$/.test(key) &&    
        key <= 4294967294               
        ) {
        console.log(arr[key]);
    }
}
```

for-in 只会遍历存在的实体，上面的例子中， for-in 遍历了3次（遍历属性分别为”0″、 “100″、 “10000″的元素，普通 for 循环则会遍历 10001 次）。所以，只要处理得当， for-in 在遍历 Array 中元素也能发挥巨大作用。

为了避免重复劳动，我们可以包装一下上面的代码：

```js
function arrayHasOwnIndex(array, prop) {
    return array.hasOwnProperty(prop) &&
        /^0$|^[1-9]\d*$/.test(prop) &&
        prop <= 4294967294; // 2^32 - 2
}
```
使用示例如下：

```js
for (let key in arr) {
    if (arrayHasOwnIndex(arr, key)) {
        console.log(arr[key]);
    }
}
```

**for-in 性能**

正如上面所说，每次迭代操作会同时搜索实例或者原型属性， for-in 循环的每次迭代都会产生更多开销，因此要比其他循环类型慢，一般速度为其他类型循环的 1/7。因此，除非明确需要迭代一个属性数量未知的对象，否则应避免使用 for-in 循环。如果需要遍历一个数量有限的已知属性列表，使用其他循环会更快，比如下面的例子：

```js
const obj = {
    "prop1": "value1",
    "prop2": "value2"
};

const props = ["prop1", "prop2"];
for(let i = 0; i < props.length; i++) {
    console.log(obj[props[i]]);
}
```

上面代码中，将对象的属性都存入一个数组中，相对于 `for-in` 查找每一个属性，该代码只关注给定的属性，节省了循环的开销和时间。

## forEach

在 ES5 中，引入了新的循环，即 forEach 循环。

```js
const arr = [1, 2, 3];
arr.forEach((data) => {
    console.log(data);
});
```

运行结果：

```js
1
2
3
```

forEach 方法为数组中含有有效值的每一项执行一次 callback 函数，那些已删除（使用 delete 方法等情况）或者从未赋值的项将被跳过（不包括那些值为 undefined 或 null 的项）。 callback 函数会被依次传入三个参数：

*   数组当前项的值；
*   数组当前项的索引；
*   数组对象本身；

需要注意的是，forEach 遍历的范围在第一次调用 callback 前就会确定。调用forEach 后添加到数组中的项不会被 callback 访问到。如果已经存在的值被改变，则传递给 callback 的值是 forEach 遍历到他们那一刻的值。已删除的项不会被遍历到。

```js
const arr = [];
arr[0] = "a";
arr[3] = "b";
arr[10] = "c";
arr.name = "Hello world";
arr.forEach((data, index, array) => {
    console.log(data, index, array);
});
```

运行结果：

```js
a 0 ["a", 3: "b", 10: "c", name: "Hello world"]
b 3 ["a", 3: "b", 10: "c", name: "Hello world"]
c 10 ["a", 3: "b", 10: "c", name: "Hello world"]
```
这里的 index 是 Number 类型，并且也不会像 for-in 一样遍历原型链上的属性。

所以，使用 forEach 时，我们不需要专门地声明 index 和遍历的元素，因为这些都作为回调函数的参数。

另外，forEach 将会遍历数组中的所有元素，但是 ES5 定义了一些其他有用的方法，下面是一部分：

*   every: 循环在第一次 return false 后返回
*   some: 循环在第一次 return true 后返回
*   filter: 返回一个新的数组，该数组内的元素满足回调函数
*   map: 将原数组中的元素处理后再返回
*   reduce: 对数组中的元素依次处理，将上次处理结果作为下次处理的输入，最后得到最终结果。

**forEach 性能**

大家可以看 [jsPerf](https://jsperf.com/for-vs-foreach/66) ，在不同浏览器下测试的结果都是 forEach 的速度不如 for。如果大家把测试代码放在控制台的话，可能会得到不一样的结果，主要原因是控制台的执行环境与真实的代码执行环境有所区别。

## for-of

先来看个例子：

```js
const arr = ['a', 'b', 'c'];
for(let data of arr) {
    console.log(data);
}
```

运行结果是：

```js
a
b
c
```
**为什么要引进 for-of？**

要回答这个问题，我们先来看看ES6之前的 3 种 for 循环有什么缺陷：

*   forEach 不能 break 和 return；
*   for-in 缺点更加明显，它不仅遍历数组中的元素，还会遍历自定义的属性，甚至原型链上的属性都被访问到。而且，遍历数组元素的顺序可能是随机的。

所以，鉴于以上种种缺陷，我们需要改进原先的 for 循环。但 ES6 不会破坏你已经写好的 JS 代码。目前，成千上万的 Web 网站依赖 for-in 循环，其中一些网站甚至将其用于数组遍历。如果想通过修正 for-in 循环增加数组遍历支持会让这一切变得更加混乱，因此，标准委员会在 ES6 中增加了一种新的循环语法来解决目前的问题，即 for-of 。

那 for-of 到底可以干什么呢？

*   跟 forEach 相比，可以正确响应 break, continue, return。
*   for-of 循环不仅支持数组，还支持大多数类数组对象，例如 DOM nodelist 对象。
*   for-of 循环也支持字符串遍历，它将字符串视为一系列 Unicode 字符来进行遍历。
*   for-of 也支持 Map 和 Set （两者均为 ES6 中新增的类型）对象遍历。

总结一下，for-of 循环有以下几个特征：

*   这是最简洁、最直接的遍历数组元素的语法。
*   这个方法避开了 for-in 循环的所有缺陷。
*   与 forEach 不同的是，它可以正确响应 break、continue 和 return 语句。
*   其不仅可以遍历数组，还可以遍历类数组对象和其他可迭代对象。

但需要注意的是，for-of循环不支持普通对象，但如果你想迭代一个对象的属性，你可以用

for-in 循环（这也是它的本职工作）。

最后要说的是，ES6 引进的另一个方式也能实现遍历数组的值，那就是 Iterator。上个例子：

```js
const arr = ['a', 'b', 'c'];
const iter = arr[Symbol.iterator]();

iter.next() // { value: 'a', done: false }
iter.next() // { value: 'b', done: false }
iter.next() // { value: 'c', done: false }
iter.next() // { value: undefined, done: true }
```
不过，这个内容超出了本文的范围，而且 Iterator 要讲的也有很多，以后有时间专门写一篇文章介绍，欢迎关注。
