---
title:  CSS布局之-水平垂直居中
date: 2017-04-05
comments: on
categories:  [Web]
tags: [JavaScript, CSS, 布局]
id: 201704052130
no_image: https://source.unsplash.com/random/800x600
description: 对一个元素水平垂直居中，在我们的工作中是会经常遇到的，也是CSS布局中很重要的一部分，本文就来讲讲CSS水平垂直居中的一些方法。
---

对一个元素水平垂直居中，在我们的工作中是会经常遇到的，也是 CSS 布局中很重要的一部分，本文就来讲讲 CSS 水平垂直居中的一些方法。

<!-- more -->

另外，文中的 css 都是用 less 书写的，如果看不懂 less，可以把我给的 demo 链接打开，然后在控制台中查看最终的 css，或者是点击 codepen 上的“View Compiled”按钮，可以查看编译后的 css

先看一张图，这是去年 cssConf 大会时阿里的 @寒冬 winter 老师放出来的：

![alt](//img.souche.com/20160316/png/75f94274a6a7095538eb10cbd18eb4a8.png)

如图所示，CSS 布局是可以分为几大块的：

- 盒子内部的布局
  - 文本的布局
  - 盒模型本身的布局
- 盒子之间的布局 visual formatting
  - 脱离正常流 normal flow 的盒子的布局
    - absolute 布局上下文下的布局
    - float 布局上下文下的布局
  - 正常流 normal flow 下的盒子的布局
    - BFC 布局上下文下的布局
    - IFC 布局上下文下的布局
    - FFC 布局上下文下的布局
    - table 布局上下文下的布局
    - css grid 布局上下文下的布局

所有的 CSS 布局其实都是围绕着这些布局模块来的，水平垂直居中也一样。

#### 一. 文本的水平垂直居中

**line-height + text-align:center**

[DEMO 链接](http://codepen.io/Dudy/pen/aOKWWO?editors=110)

代码：

```js
<div class="wrap">水平垂直居中水平垂直居中</div>
```

```js
html,body{
  margin: 0;
}

.wrap{
  line-height: 400px;
  text-align:center;

  height: 400px;
  font-size: 36px;
  background-color: #ccc;
}

```

这种方法只适合单行文字的水平垂直居中

#### 二. 利用盒模型的水平垂直居中

我们一般讲的盒模型都是说的块级盒的盒模型，也只有块级盒的盒模型用得多一点，块级盒 block-level box 又是分别由 content-box、padding-box、border-box、margin-box 组成的，如下图：

![Alt text](//img.souche.com/20160316/png/93a4055545278d504a8add63bc0883bf.png)

也就说我任一个子盒子的水平和垂直方向的边与最外面盒子的间距都是可以控制的，因此也就有如下居中方法：

**padding 填充**

[DEMO 链接](http://codepen.io/Dudy/pen/EjRvgp?editors=110)

代码：

```js
<div class="wrap">
  <div class="content" />
</div>
```

```js
@wrapWidth : 400px;

.wrap{
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  width: @wrapWidth;
  height: @wrapWidth;
  background-color: #ccc;
}

.content{
  @contentWidth : 100px;
  width: @contentWidth;
  height: @contentWidth;
  padding: (@wrapWidth - @contentWidth) / 2;
  background-color: #333;
  background-clip:content-box;
}

```

也可以用 css3 的 calc()动态计算:

[DEMO 链接](http://codepen.io/Dudy/pen/RPJZVw?editors=110)

```js
<div class="wrap">
  <div class="content" />
</div>
```

```js
.wrap{
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
  width: 400px;
  height: 400px;
  background-color: #ccc;
  .content{
    padding: -webkit-calc(~"(100% - 100px) / 2");
    padding: calc(~"(100% - 100px) / 2");
    width: 100px;
    height: 100px;
    background-color: #333;
    background-clip: content-box;
  }
}

```

注意这里我在 calc 中使用了一个~""的写法，这是 less 中的一个语法，告诉 less 这里不被 less 所编译，要是被 less 编译了的话，css 的 calc 函数的参数就不是 100% - 100px，而是 0%了。

**margin 填充**

[DEMO 链接](http://codepen.io/Dudy/pen/jPKxYL?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele" />
</div>
```

```js
.wrap{
  @wrapHeight : 400px;
  @contenHeight : 100px;
  overflow: hidden;
  width: 100%;
  height: @wrapHeight;
  background-color: #ccc;
  .ele{
    margin-left: auto;
    margin-right: auto;
    margin-top: (@wrapHeight - @contenHeight) / 2;
    width: 100px;
    height: @contenHeight;
    background-color: #333;
    color: #fff;
  }
}

```

使用 margin 填充我们需要知道元素的宽度，这点不太灵活，不过 CSS3 搞出了一个加 fit-content 的属性值，可以动态计算元素的宽度，[DEMO 链接](http://codepen.io/Dudy/pen/yNEZVQ)

使用盒模型进行布局不会产生 reflow，兼容也好，使用盒模型布局是一种布局思想，其实仅仅靠它就能实现很多 visual formatting 才能实现的布局，这是另一个话题，这里不展开。

#### 三. absolute 布局上下文下的水平垂直居中

**50% + -50%**

原理很简单，就是利用 left：50%将盒子的左边先置于父容器的中点，然后再将盒子往左偏移盒子自身宽度的 50%，这里有三种具体实现：

[DEMO 链接](http://codepen.io/Dudy/pen/VLdzRv?editors=110)

```js
<div class="wrap">
  <div class="ele margin">水平垂直居中水平垂直<br>居中水平垂直居中水平<br>垂直居中水平垂直居<br>中水平垂直居中</div>
</div>

<div class="wrap">
  <div class="ele translate">水平垂直居中水平垂直<br>居中水平垂直居中水平<br>垂直居中水平垂直居<br>中水平垂直居中</div>
</div>

<div class="wrap">
  <div class="ele relative">
    <div class="ele-inner">水平垂直居中水平垂直<br>居中水平垂直居中水平<br>垂直居中水平垂直居<br>中水平垂直居中</div>
  </div>
</div>

```

```js
.wrap{
  position: relative;
  width: 100%;
  height: 200px;
  border:1px solid;
  background-color: #ccc;
  .ele{
    position: absolute;
    left: 50%;
    top: 50%;
    background-color: #333;
    &.margin{
      width: 160px;
      height: 100px;
      margin-left: -80px;
      margin-top: -50px;
    }
    &.translate{
      -webkit-transform:translate3d(-50%, -50%, 0);
      transform:translate3d(-50%, -50%, 0);
    }
    .ele-inner{
      position: relative;
      left: -50%;
      top: -50%;
      width: 100%;
      height: 100%;
      background-color: #333;
    }
    &.relative{
      width: 150px;
      height: 100px;
      background-color: transparent;
    }
  }
}

```

上面三个方法中，margin 方法和 relative 方法都需要知道元素的宽高才行(relative 方法只知道高也行)，适用于固定式布局，而 transform 方法则可以不知道元素宽高

**text-align:center + absolute**

text-aign:center 本来是不能直接作用于 absolute 元素的，但是没有给其 left 等值的行级 absolute 元素是会受文本的影响的，可以参考张老师的[这篇文章](http://www.zhangxinxu.com/wordpress/2011/12/position-absolute-text-align-center/)

[DEMO 链接](http://codepen.io/Dudy/pen/BNVwJx?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele" />
</div>
```

```js
.wrap{
  text-align: center;

  width: 100%;
  height: 400px;
  background-color: #ccc;
  font-size: 0;
}
.ele{
  position: absolute;
  margin-left: -(100px / 2);
  margin-top: (400px - 100px) / 2;

  width: 100px;
  height: 100px;
  display: inline-block;
  background-color: #333;
}

```

简单解释下，首先，text-align:center 作用的是文本而不是 absolute 的元素，但是，当 absolute 元素为 inline-block 的时候，它会受到文本的影响，然后你可能会问这里没文本啊，我只能告诉你说这下面是有的，是个匿名的文本节点。具体的这里不展开，可以参考[标准](http://www.w3.org/TR/CSS2/visudet.html#propdef-line-height)，然后理解这句话:

> If the inline box contains no glyphs at all, it is considered to contain a strut (an invisible glyph of zero width) with the A and D of the element's first available font

然后这个匿名文本由于受到 text-align:center 影响居中了，这个时候 absolute 盒子的左边跟父容器的中点对齐了，所以就还需要往回拉 50%，这里用的是 margin-left，你也可以用其它方式拉。然后就是垂直方向的对齐，垂直方向是不能被操作文本的属性影响的，所以我这里用的是 margin-top 来让它偏移下去。

**absolute + margin : auto**

[DEMO 链接](http://codepen.io/Dudy/pen/mJKqXa?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele" />
</div>
```

```js
html,body{
  width: 100%;
  height: 100%;
  margin: 0;
}
.wrap{
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #ccc;
  .ele{
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
    width: 100px;
    height: 100px;
    background-color: #333;
  }
}

```

关于这种布局的原理，在标准中能找到如下解释：

[w3c.org](http://www.w3.org/TR/CSS21/visudet.html#abs-non-replaced-width)中有这样一句话：

> The constraint that determines the used values for these elements is:
> 'left' + 'margin-left' + 'border-left-width' + 'padding-left' + 'width' + 'padding-right' + 'border-right-width' + 'margin-right' + 'right' = width of containing block

这句话说的是 absolute 性质的盒子，它的包含块的宽度等于它的盒模型的宽度 + left + right 值，包含块的高度同理，盒模型包括 margin-box、border-box、padding-box、content-box，而在这个居中方法中，.ele 的 left + right 值是 0，width 是定值，width 所在盒子包括了除了 margin-box 外的那三个 box，margin 都是 auto 值，按照上面那个公式，margin-left + margin-right 的值应该等于包含块的宽度 - left 的值 - right 的值 - width 的值，也就是说 margin-left + margin-right 的值等于除了 width 所占宽度外的剩下宽度，拥有剩下宽度后，就是平分其宽度，以让左右两边相等，达到居中，标准中给出了答案：

> If none of the three is 'auto': If both 'margin-left' and 'margin-right' are 'auto', solve the equation under the extra constraint that the two margins get equal values, unless this would make them negative, in which case when direction of the containing block is 'ltr' ('rtl'), set 'margin-left' ('margin-right') to zero and solve for 'margin-right' ('margin-left')

这里的"three"指的是 left, width, right。如果 left、right 和 width 都不为 auto，同时 margin-left 和 margin-right 都是 auto，除非特别情况，它们俩就是相等的，而这个例子中不在特殊情况之列，因此两者平分，此时达到了水平居中。而对于垂直方向的 margin 的 auto 值的计算，标准中也有如下两句话，跟水平方向的同理(这里的“three”指的是“top, height, bottom”)：

> the used values of the vertical dimensions must satisfy this constraint:
> 'top' + 'margin-top' + 'border-top-width' + 'padding-top' + 'height' + 'padding-bottom' + 'border-bottom-width' + 'margin-bottom' + 'bottom' = height of containing block
>
> if none of the three are 'auto': If both 'margin-top' and 'margin-bottom' are 'auto', solve the equation under the extra constraint that the two margins get equal values.

垂直方向也就因此也居中了。

这种方法能简单的做到居中，但是必须有 width 和 height 值

**适用于图片居中的网易 nec 的一个方法**

[DEMO 链接](http://codepen.io/Dudy/pen/GJGzJr?editors=110)

代码：

```js
<div class="wrap">
  <p>
    <img src="http://nec.netease.com/img/s/1.jpg" alt="" />
    <img src="http://nec.netease.com/img/s/1.jpg" alt="" />
  </p>
</div>
```

```js
html,body{
  width: 100%;
  height: 100%;
  margin: 0;
}

.wrap{
  position:relative;
  width: 100%;
  height: 100%;
  p{
    position:absolute;
    left:50%;
    top:50%;
  }
  img{
    &:nth-child(1){
      position:static;
      visibility:hidden;
    }
    &:nth-child(2){
      position:absolute;
      right:50%;
      bottom:50%;
    }
  }
}

```

这种方法主要是利用了一个图片进行占位，以让父容器获得高宽，从而让进行-50%偏移的图片能有一个参照容器作百分比计算。优点是可以不知道图片的大小，随便放张尺寸不超过父容器的图片上去都能做到居中。另外，兼容性好，如果是不使用 nth-child 选择器的花，IE6 都是能顺利兼容的

#### 四. float 布局上下文下的水平垂直居中

**float + -50%**

[DEMO 链接](http://codepen.io/Dudy/pen/xGzjZa?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele">
    <div class="ele-inner">居中居中居中居中居中居中<br>居中居中居中居中居中居中居中居中居<br>中居中居中居中居中居中居中居中居中居<br>中居中居中居中居中居中居中</div>
  </div>
</div>

```

```js
.wrap{
  float: left;
  width: 100%;
  height: 400px;
  background-color: #ccc;
  .ele{
    float: left;
    position: relative;
    left: 50%;
    top: 50%;
  }
  .ele-inner{
    position: relative;
    left: -50%;
    -webkit-transform : translate3d(0, -50%, 0);
    transform : translate3d(0, -50%, 0);
    background-color: #333;
    color: #fff;
  }
}

```

这种方法的原理，首先是利用 float 属性将需要居中的元素的父元素.ele 的宽度收缩，然后 left:50%将.ele 的左边和水平中线对齐，这个时候还没居中，还需要将其往回拉自身宽度的 50%，于是.ele-inner 便是真正需要水平居中的元素，我给它一个 position:relative，将其往回拉自身宽度 50%就行了。对于垂直方向，依然是先将.ele top:50%到垂直方向中点，但是这时给.ele-inner top:50%是不起作用的，因为如果没给父元素明确高度的话，这个 50%是计算不出来的，因此，就有了 transform : translate3d(0, -50%, 0)。

这种方法的好处是元素可以不定宽，任何时候都可以做到居中

我当时在 w3cplus 的站上发现这个方法后，当时觉得这个方法很好，兼容性好，又还可以不定宽，但当我用了一段时间后，发现了一个问题：

就是当居中元素的父元素 left:50%时，如果元素宽度足够大，会超出外面的容器，而如果外面的容器又正好是 overflow:auto 的话，那就会在外面产生滚动条，问题 DEMO 链接[在这里](http://codepen.io/Dudy/pen/vENMwr?editors=110)，后来我找到了一个办法：[DEMO 链接](http://codepen.io/Dudy/pen/YPWeYY?editors=110) ，基本思想就是利用元素超出父元素的左边不会产生滚动条的特性，有点奇淫技巧，但是能解决问题，有兴趣的可以看看

**margin-bottom : -50%**

[DEMO 链接](http://codepen.io/Dudy/pen/bdKMrB?editors=110)

代码：

```js
<div class="wrap">
  <div class="placeholder" />
  <div class="content" />
</div>
```

```js
.wrap{
  float: left;
  width: 100%;
  height: 400px;
  background-color: #ccc;
  @contentHeight : 100px;
  .placeholder{
    float: left;
    width: 100%;
    height: 50%;
    /*居中元素.content高度一半*/
    margin-bottom: -(@contentHeight / 2);
  }
  .content{
    position: relative;
    left: 50%;
    transform:translate3d(-50%, 0, 0);
    clear: both;
    /*演示用，实际不需要定宽*/
    max-width: 100px;
    height: @contentHeight;
    background-color: #333;
  }
}

```

这种方法是先让占位元素.placeholder 占据 50%高度，然后给一个居中元素高度一半的负的 margin-bottom，然后下面的元素只要跟着摆放就能垂直居中了。水平方向就是利用 translate 做偏移，这个没什么好说的，你也可以换成其他办法。

这种方法就是各种固定死，首先最外层的父容器需要一个固定高度，以让.placeholder 的 height:50%有效，然后，margin-bottom 也需要固定死，而且得需要知道居中元素高度。单纯就水平方向来说，这个方法比较适合需要兼容低版本 IE 的固定式布局的项目，因为兼容性好。

#### 五.BFC 布局上下文下的水平垂直居中

BFC 的全称是块级排版上下文，这里有篇[文章](http://div.io/topic/834?page=1#3261)对齐进行了简单的介绍，BFC 布局上下文下的布局其实就是利用盒模型本身进行的布局，前面在利用盒模型布局的那一节中已经讲过了，这里就不重复了

#### 六.IFC 布局上下文下的水平垂直居中

IFC 又是个什么概念呢，你可以看看[官方文档](http://www.w3.org/TR/CSS21/visuren.html#inline-formatting)，也可以简单的理解为 display 为 inline 性质的行级元素的布局。

**text-align:center + vertical-align:middle**

[DEMO 链接](http://codepen.io/Dudy/pen/pJKVZa?editors=110)

代码：

```js
<div class="wrap">
  <div class='placeholder'><!--占位元素，用来作为居中元素的参照物--></div>
  <div class="ele"></div>
</div>

```

```js
.wrap{
  width: 100%;
  height: 400px;
  /* min-height: 400px; */
  text-align:center;
  font-size: 0;
  background-color: #ccc;
  .placeholder,
  .ele{
    vertical-align: middle;
    display: inline-block;
  }
  .placeholder{
    overflow: hidden;
    width: 0;
    min-height: inherit;
    height: inherit;
  }
  .ele{
    width: 100px;
    height: 100px;
    background-color: #333;
  }
}

```

行级元素会受到 text-align 和 vertical-align 的影响，关于 vertical-align，不太好理解，我多贴几篇文章：[@灵感 idea 的](http://www.html-js.com/article/2952)，[张鑫旭的](http://www.zhangxinxu.com/wordpress/2010/05/%E6%88%91%E5%AF%B9css-vertical-align%E7%9A%84%E4%B8%80%E4%BA%9B%E7%90%86%E8%A7%A3%E4%B8%8E%E8%AE%A4%E8%AF%86%EF%BC%88%E4%B8%80%EF%BC%89/)，[MDN 上的](https://developer.mozilla.org/en-US/docs/Web/CSS/vertical-align)，[css-trick 上的](https://css-tricks.com/almanac/properties/v/vertical-align/)，以及[官方文档](http://www.w3.org/TR/CSS21/visudet.html#line-height)，这里首先是用 text-center 让 inline-block 水平居中，然后给一个 vertical-align:middle，但是仅仅给 vertical-align:middle 是不够的，因为此时它还没有 vertical-align 对齐的参照物，所以就给了一个占位的 inline-block，它的高度是 100%。

这个方法对于居中元素不需要定宽高，而且元素根据 vertical-align 值的不同不仅仅可以实现居中，还可以将其放在上面下面等。缺点是父元素需定高

**text-align:center + line-height**

[DEMO 链接](http://codepen.io/Dudy/pen/ZGRmqL?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele">居中居中居中居中居中居中<br>居中居中居中居中居中居中居中<br>居中居中居中居中居中居中居中居中<br>居中居中居中居中居中居中居中居中</div>
</div>

```

```js
.wrap{
  text-align: center;
  line-height: 400px;

  width: 100%;
  height: 400px;
  background-color: #ccc;
  font-size: 0;
  .ele{
    line-height: normal;
    vertical-align: middle;
    display: inline-block;
    background-color: #333;
    font-size: 18px;
    color: #fff;
  }
}

```

这个方法，首先是水平方向，text-align:center 就行了，至于垂直方向，起作用的就是父容器的一个 line-height 和居中元素的 vertical-align:middle，为什么这两个属性可以让一个 inline-block 垂直居中呢，这里重点是父容器在其下面产生了一个隐匿的文本节点，这个我在上面 text-align:center + absolute 那个方法的讲解中说到过了，然后这个这个隐匿文本节点会因 line-height 属性的作用而拥有了一个父容器一样高的行高，此时元素有了一个 vertical-align 对齐的参照物，再给其 vertical-align:middle 值就能垂直对齐了。

使用这个方法，居中元素无需定宽高，但缺点是得给父容器一个固定的行高才行。

**text-align:center + font-size**

[DEMO 链接](http://codepen.io/Dudy/pen/vOrvBP?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele" />
</div>
```

```js
.wrap{
  text-align: center;
  font-size: 400px * 0.873;/*约为高度的0.873*/

  margin-left: auto;
  margin-right: auto;
  width: 400px;
  height: 400px;
  background-color: #ccc;
  .ele{
    vertical-align: middle;

    width: 100px;
    height: 100px;
    display: inline-block;
    background-color: #333;
  }
}

```

这个方法来自淘宝，基本原理还是让隐匿文本节点所占据的行高等于父容器的高度，然后给居中元素一个 vertical-align:middle 对齐的一个参照。只是这里把定义 line-height 值换成了定义 font-size 值，让 font-siz 足够大从而让其行高等于父容器高度。为了证明这个 font-size 的作用，我把居中元素换成文本

[DEMO 链接](http://codepen.io/Dudy/pen/JdZwGa?editors=110)

代码：

```js
<div class="wrap">a</div>
```

```js
.wrap{
  text-align: center;
  font-size: 400px * 0.873;/*约为高度的0.873*/

  margin-left: auto;
  margin-right: auto;
  width: 400px;
  height: 400px;
  background-color: #ccc;
}

```

效果：

![alt](//img.souche.com/20160316/png/12de8abcbfff3671be67c69f4353273a.png)

可以看到字母 a 垂直居中了，这个字母 a 就对应那个隐匿文本节点

#### 七.FFC 布局上下文下的水平垂直居中

**父元素、子元素都定义 flex：**

[DEMO 链接](http://codepen.io/Dudy/pen/PqaXOZ?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele">
  居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中
  </div>
</div>

```

```js
html,body{
  width: 100%;
  height: 100%;
}

.wrap{
  display: flex;
 align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #ccc;
  .ele{
    background-color: #333;
  }
}

```

**只有父元素定义 flex，子元素定义 margin:auto：**

[DEMO 链接](http://codepen.io/Dudy/pen/zGLzRN?editors=110)

代码：

```js
<div class="wrap">
  <div class="ele">
  居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中<br>
    居中居中居中居中居中居中居中
  </div>
</div>

```

```js
html,body{
  width: 100%;
  height: 100%;
}

.wrap{
  display: flex;
  width: 100%;
  height: 100%;
  background-color: #ccc;
  .ele{
    margin:auto;
    background-color: #333;
  }
}

```

flex box 的标准中有这句话(参考链接:[http://www.w3.org/TR/css-flexbox-1/#item-margins):](http://www.w3.org/TR/css-flexbox-1/#item-margins):)

> The margins of adjacent flex items do not collapse. Auto margins absorb extra space in the corresponding dimension and can be used for alignment and to push adjacent flex items apart; see Aligning with auto margins.

意思就是说 flex item 的 margin 不会折叠，在 flex-item 有明确大小并且 margin:auto 时外边距吸收了伸缩包含块下的额外的空间，并且能被用于居中以及会让其相邻的 flex item 尽可能的往这个 flex item 所在的那一个方向靠。

flexbox 是个很强大的布局模块，也就三个属性就搞定居中了，而且不论父容器还是居中元素都可以不定宽高。参考链接：[图解 CSS3 Flexbox 属性](http://www.w3cplus.com/css3/a-visual-guide-to-css3-flexbox-properties.html)

#### 八.table 布局上下文下的水平垂直居中

[DEMO 链接](http://codepen.io/Dudy/pen/EjRGRO?editors=110)

代码：

```js
<div class='wrap'>
    <div class='ele'>
      <div class="ele-inner">居中居中居中居中居中居中居中居中<br>居中居中居中居中居中居中居中居中<br>居中居中居中居中居中居中居中居中居中居中</div>
    </div>
</div>

```

```js
.wrap{
  width: 100%;
  height: 300px;
  display: table;
  background-color: #ccc;
}
.ele{
  text-align:center;
  vertical-align: middle;
  display:table-cell;
}

.ele-inner{
  display: inline-block;
  background-color: #333;
}

```

原理就是把 div 模拟成表格（换成真正的表格标签也是可以的），然后给那几个属性就成了，这个没什么好讲的，不懂的去翻翻手册就明白了，然后[@于江水](http://weibo.com/u/2945647940?topnav=1&wvr=6&topsug=1)写的一篇[table 那些事](http://yujiangshui.com/about-table/)还不错

#### 九.CSS grid 布局上下文下的水平垂直居中

CSS3 grid layout 是 IE 搞出来的一个布局模块，目前貌似还只有 IE0 和 IE11 支持，我没有研究过其居中的方法，有兴趣的可以看看[大漠老师的介绍文章](http://www.w3cplus.com/blog/tags/356.html)

#### 十.其它未知归属的水平垂直居中方法

**使用 button 标签**

[DEMO 链接](http://codepen.io/Dudy/pen/aOKPgr?editors=110)

代码：

```js
<button>
  <div>
    居中居中居中居中居中居中<br>
    居中居中居中居中居中居中<br>
    居中居中居中居中居中居中<br>
    居中居中居中居中居中居中<br>
  </div>
</button>

```

```js
button{
  width: 100%;
  height: 400px;
  background-color: #cccccc;
  border-width:0;
  &:focus{
    outline:none;
  }
  div{
    display: inline-block;
    font-size: 18px;
    background-color: #333;
    color: #fff;
  }
}

```

这种方法属于奇淫技巧，利用 button 标签天生外挂的这一技能对其里面的元素进行居中。

**（本文完）**

> 原文地址: [http://div.io/topic/1155](http://div.io/topic/1155)
