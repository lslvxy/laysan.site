---
title:  实现用CSS切割图片的方法
date: 2014-04-03
comments: on
categories:  [Web]
tags: [css,cut,图片,切割]
id: 201404030930
---


切割图片这里不是真正的切割，只是用CSS取图片中的一部分而已。这样做的好处就是减少了打开网页时请求图片的次数。主要有两种方式，一是做为某一元素的背景图片，二是用img元素的属性。
<!-- more -->
### 方法一：


用CSS中元素的`background` : `background-color `|| `background-image `|| `background-repeat` || `background-attachment `|| `background-position`。
示例代码如下：

```css
background:transparent url(123.jpg) no-repeat scroll -140px -20px;
```

解释：

```css
transparent表示透明无颜色
url(123.jpg) 表示背景图片
no-repeat 表示图片不重复
scroll 表示背景图片随浏览器下拉而滚动
-140px 表示水平位置在图片的-140px处（以图片的左上角为0,0）
-20px 表示垂直位置在图片的-20px处（以图片的左上角为0,0）
```

### 方法二：

用img的clip属性中的`rect`，`clip:rect(y1 y1 x2 x1)`参数说明如下：

y1=定位的y坐标(垂直方向)的起点

x1=定位的x坐标(水平方向)的起点

y2=定位的y坐标(垂直方向)的终点

x2=定位的x坐标(水平方向)的终点

可以看成`clip:rect(上，左，下，右)`

注:坐标的起点是在左上角

示例代码：

```css
img{
	position:absolute;
	clip:rect(20px 100px 50px 20px);
}
```

上面可以看出控制图片显示的关键在于`clip:rect(20px 100px 50px 20px)`这句，千万不要忘记`position:absolute;`这是用于使用绝对值来定位元素。
