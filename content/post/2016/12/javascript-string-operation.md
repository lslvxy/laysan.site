---
title:  JavaScript 字符串常用操作
date: 2016-12-20
comments: on
categories:  [Web]
tags: [JavaScript,String,字符串]
id: 201612201330
no_image: https://source.unsplash.com/random/800x600
description: JavaScript 字符串用于存储和处理文本。因此在编写 JS 代码之时她总如影随形，在你处理用户的输入数据的时候，在读取或设置 DOM 对象的属性时，在操作 Cookie 时，在转换各种不同 Date 时，诸此等等，繁不能数.
---


JavaScript 字符串用于存储和处理文本。因此在编写 JS 代码之时她总如影随形，在你处理用户的输入数据的时候，在读取或设置 DOM 对象的属性时，在操作 Cookie 时，在转换各种不同 Date 时，诸此等等，繁不能数；而她那满多的 API 呵，总有些让人不愿去记忆的冲动，既然用时常搜，倒不如烂笔头一翻，顺道也体现下博客存在的价值，由此就有了这篇纪要。
<!-- more -->
## 字符串截取

### 1. substring()

xString.substring(start,end)

substring()是最常用到的字符串截取方法，它可以接收两个参数(参数不能为负值)，分别是要截取的开始位置和结束位置，它将返回一个新的字符串，其内容是从start处到end-1处的所有字符。若结束参数(end)省略，则表示从start位置一直截取到最后。
```js
let str = 'www.jeffjade.com'
console.log(str.substring(0,3)) // www
console.log(str.substring(0))   //www.jeffjade.com
console.log(str.substring(-2))  //www.jeffjade.com (传负值则视为0)
```

### 2. slice()
```js
stringObject.slice(start, end)
```
`slice()`方法与`substring()`方法非常类似，它传入的两个参数也分别对应着开始位置和结束位置。而区别在于，`slice()`中的参数可以为负值，如果参数是负数，则该参数规定的是从字符串的尾部开始算起的位置。也就是说，-1 指字符串的最后一个字符。

```js
let str = 'www.jeffjade.com'
console.log(str.slice(0, 3))    // www
console.log(str.slice(-3, -1))  // co
console.log(str.slice(1, -1))   // www.jeffjade.co
console.log(str.slice(2, 1))    // '' (返回空字符串,start须小于end)
console.log(str.slice(-3, 0))   // '' (返回空字符串,start须小于end)
```

### 3. substr()

```js
stringObject.substr(start,length)
```
`substr()`方法可在字符串中抽取从`start`下标开始的指定数目的字符。其返回值为一个字符串，包含从` stringObject`的`start`（包括`start`所指的字符）处开始的`length`个字符。如果没有指定 `length`，那么返回的字符串包含从`start`到`stringObject`的结尾的字符。另外如果`start`为负数，则表示从字符串尾部开始算起。

```js
let str = 'www.jeffjade.com'
console.log(webStr.substr(1, 3))   // ww.
console.log(webStr.substr(0))      // www.jeffjade.com
console.log(webStr.substr(-3, 3))  // com
console.log(webStr.substr(-1, 5))  // m  (目标长度较大的话，以实际截取的长度为准)
```
### 4. split()

```js
str.split([separator][, limit])
```
`separator` 指定用来分割字符串的字符（串）。`separator` 可以是一个字符串或正则表达式。 如果忽略 `separator`，则返回整个字符串的数组形式。如果 `separator` 是一个空字符串，则 str 将会把原字符串中每个字符的数组形式返回。
limit 一个整数，限定返回的分割片段数量。split 方法仍然分割每一个匹配的 `separator`，但是返回的数组只会截取最多 limit 个元素。

```js
let str = 'www.jeffjade.com'
str.split('.')      // ["www", "jeffjade", "com"]
str.split('.', 1)   // ["www"]
str.split('.').join('') // wwwjeffjadecom
```

话说这个函数真心好用，很多时候的字符截取需求，就是依赖于某个字符；而以上三个函数都需知道其位置。我们当然可以借助 indexOf 等方法获取，很显然这很繁琐；而借助 split 则显得更轻而易举。

## 查找类方法

### 1. indexOf() & includes()

```js
stringObject.indexOf(searchValue,fromIndex)
```

`indexOf()`用来检索指定的字符串值在字符串中首次出现的位置。它可以接收两个参数，`searchValue`表示要查找的子字符串，`fromIndex` 表示查找的开始位置，省略的话则从开始位置进行检索。

```js
let str = 'www.jeffjade.com'
console.log(str.indexOf('.'))     // 3
console.log(str.indexOf('.', 1))  // 3
console.log(str.indexOf('.', 5))  // 12
console.log(str.indexOf('.', 12)) // -1
```
虽然 `indexOf()`用来检索指定的字符串值在字符串中首次出现的位置 ，然而很多时候，使用它的场景在于判断字符串中是否存在指定的字符串；因此代码就会如此：

```js
if (str.indexOf('yoursPecifiedStr') !== -1) {
    // do something
}
```

要知道在这样的场景下，ES6 语言中的`includes()`就显得更优雅许多；`includes()` 方法用于判断一个字符串是否被包含在另一个字符串中，如果是返回true，否则返回false。

```js
str.includes(searchString[, position])
```
`searchString` 将要搜寻的子字符串。`position` 可选。从当前字符串的哪个索引位置开始搜寻子字符串；默认为0。需要注意的是，`includes()` 是区分大小写的。

```js
'Blue Whale'.includes('blue'); // returns false
'乔峰乔布斯乔帮主'.includes('乔布斯'); // returns true
if (str.includes('yoursPecifiedStr')) {
    // do something(这样写是不是更为人性化？Yeah，这是一个更趋向人性化的时代嘛)
}
```

### 2. lastIndexOf()

```js
stringObject.lastIndexOf(searchValue,fromIndex)
```
`lastIndexOf()`语法与`indexOf()`类似，它返回的是一个指定的子字符串值最后出现的位置，其检索顺序是从后向前。

```js
let str = 'www.jeffjade.com'
console.log(str.lastIndexOf('.'))     // 12
console.log(str.lastIndexOf('.', 1))  // -1
console.log(str.lastIndexOf('.', 5))  // 3
console.log(str.lastIndexOf('.', 12)) // 12
```
### 3. search()

```js
stringObject.search(substr)
stringObject.search(regexp)
```
search()方法用于检索字符串中指定的子字符串，或检索与正则表达式相匹配的子字符串。它会返回第一个匹配的子字符串的起始位置，如果没有匹配的，则返回-1。

```js
let str = 'www.jeffjade.com'
console.log(str.search('w'))    // 0
console.log(str.search(/j/g))   // 4
console.log(str.search(/\./g))  // 3
```
### 4. match()方法

```js
stringObject.match(substr)
stringObject.match(regexp)
```
`match()`方法可在字符串内检索指定的值，或找到一个或多个正则表达式的匹配。

如果参数中传入的是子字符串或是没有进行全局匹配的正则表达式，那么match()方法会从开始位置执行一次匹配，如果没有匹配到结果，则返回null。否则则会返回一个数组，该数组的第0个元素存放的是匹配文本，除此之外，返回的数组还含有两个对象属性index和input，分别表示匹配文本的起始字符索引和stringObject 的引用(即原字符串)。

```js
let str = '#1a2b3c4d5e#';
console.log(str.match('A'));    //返回null
console.log(str.match('b'));    //返回["b", index: 4, input: "#1a2b3c4d5e#"]
console.log(str.match(/b/));    //返回["b", index: 4, input: "#1a2b3c4d5e#"]
```
如果参数传入的是具有全局匹配的正则表达式，那么match()从开始位置进行多次匹配，直到最后。如果没有匹配到结果，则返回null。否则则会返回一个数组，数组中存放所有符合要求的子字符串，并且没有index和input属性。

```js
let str = '#1a2b3c4d5e#'
console.log(str.match(/h/g))     //返回null
console.log(str.match(/\d/g))    //返回["1", "2", "3", "4", "5"]
```
## 其他方法

### replace()方法

```js
stringObject.replace(regexp/substr,replacement)
```
`replace()`方法用来进行字符串替换操作，它可以接收两个参数，前者为被替换的子字符串（可以是正则），后者为用来替换的文本。

如果第一个参数传入的是子字符串或是没有进行全局匹配的正则表达式，那么replace()方法将只进行一次替换（即替换最前面的），返回经过一次替换后的结果字符串。

```js
let str = 'www.jeffjade.com'
console.log(str.replace('w', 'W'))   // Www.jeffjade.com
console.log(str.replace(/w/, 'W'))   // Www.jeffjade.com
```
如果第一个参数传入的全局匹配的正则表达式，那么replace()将会对符合条件的子字符串进行多次替换，最后返回经过多次替换的结果字符串。

```js
let str = 'www.jeffjade.com'
console.log(str.replace(/w/g, 'W'))   // WWW.jeffjade.com
```
### toLowerCase() & toUpperCase()

```js
stringObject.toLowerCase()
stringObject.toUpperCase()
```
`toLowerCase()`方法可以把字符串中的大写字母转换为小写，`toUpperCase()`方法可以把字符串中的小写字母转换为大写。

```js
let str = 'www.jeffjade.com'
console.log(str.toLowerCase())   // www.jeffjade.com
console.log(str.toUpperCase())   // WWW.JEFFJADE.COM
```
## 模板字符串

这个也是 ES6 才引入进来的新语法，来解决传统输出String模板的蹩脚问题；其功能之强大，设计之贴心，着实令人得到极大满足感，好如久旱逢甘霖一般的舒畅。更何况，在当今 MVVM 前端框架大行其道的时代，使用 ES6 语法也是不用自己个儿去操心兼容性问题，对于塑造 Dom Template 更是如虎添翼，令人爱不释手。

对于她的使用，阮一峰在ECMAScript 6 入门有过详细的描述以及示例，在此就不赘述。只需要明白我们可以像这样去操作了，试问爽否？
```js
function ncieFunc() {
  return "四海无人对夕阳";
}
var niceMan = "陈寅恪";
var jadeTalk = `一生负气成今日 \n ${ncieFunc()} ,
语出 ${niceMan} 的《忆故居》。
`
console.log(jadeTalk)
```

运行之，Chrome Console 输出结果如下：
```
    一生负气成今日
    四海无人对夕阳 ,
    语出 陈寅恪 的《忆故居》。
```
## 组合其法

细看 JavaScript 提供的String Api，还是有蛮多的，也有些许废弃的，也有将在未来版本会出来的；这其中不乏很多也挺有用的，譬如： charAt(x)、charCodeAt(x)、concat(v1, v2,…)、fromCharCode(c1, c2,…) 等等,还有 ES6 对字符串的扩展，比如 字符串的遍历器接口，repeat() 等等，这可以参见 ES6-string，这里就不多赘述。

在实际代码生产中，很多时候需要用这些提供的基本方法，来打出一套组合拳，以解决其需求所需。很显然又可以借助 prototype 属性，将自造的各路拳法，其归置于 String 对象，然后天亮啦。这一步就看个人喜好了，这里抛出一二段，以引大玉。

### 字符串反转

```js
String.prototype.reverse = function () {
	return this.split('').reverse().join('')
}
```

### 去除空白行

```js
String.prototype.removeBlankLines = function () {
	return this.replace(/(\n[\s\t]*\r*\n)/g, '\n').replace(/^[\n\r\n\t]*|[\n\r\n\t]*$/g, '')
}
```

### String转化为数组

#### 1, 转化为一维数组

场景是根据某子字符串转化，直接就用 split 就好；如果转换规则不统一，那么请自求多福吧。

```js
let Str = '陈寅恪,鲁迅,钱钟书,胡适,王国维,梁启超,吴宓,季羡林'
let hallAllOfFameArr = Str.split(',')
console.log(hallAllOfFameArr)
// ["陈寅恪", "鲁迅", "钱钟书", "胡适", "王国维", "梁启超", "吴宓", "季羡林"]
```
#### 2, 转化为二维数组

```js
String.prototype.removeBlankLines = function () {
	return this.replace(/(\n[\s\t]*\r*\n)/g, '\n').replace(/^[\n\r\n\t]*|[\n\r\n\t]*$/g, '')
}
String.prototype.strTo2dArr = function(firstSplit, secondSplit){
	var contentStr = this.removeBlankLines(),
		contentStrArr = contentStr.split(firstSplit),
		resultArr = contentStrArr.map((element) => {
            return element.split(secondSplit)
        })
	return resultArr
}
var str = `
渺渺钟声出远方,依依林影万鸦藏。
一生负气成今日,四海无人对夕阳。
破碎山河迎胜利,残馀岁月送凄凉。
松门松菊何年梦,且认他乡作故乡。
`
console.log(str.strTo2dArr('\n', ','))
```
运行之，输出结果如下：

```
[ [ ‘渺渺钟声出远方’, ‘依依林影万鸦藏。’ ],
[ ‘一生负气成今日’, ‘四海无人对夕阳。’ ],
[ ‘破碎山河迎胜利’, ‘残馀岁月送凄凉。’ ],
[ ‘松门松菊何年梦’, ‘且认他乡作故乡。’ ] ]
```
