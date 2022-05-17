---
title:  通过MD5排除重复文件
date: 2014-08-16
comments: on
categories:  [Java]
tags: [MD5,重复,文件]
id: 201408160930
---


今天下载了好多美女图片壁纸，可是看了一下发现好多图片重复了，有强迫症的我必须把重复的都给剔除掉，首先想到的当然是百度了，问问度娘有没有什么图片去重的工具，搜了一下还真有。奈何本人智商捉急用不来这高级的软件，无奈之下只好准备一张一张的挑出来了，CTRL+A一看2000+的图片，好吧一晚上不用干别的事了。。
<!-- more -->
辛亏脑袋还比较好使，既然作为一个程序员，为什么不能写个代码处理一下呢？想到点子说干咱就干，最重要的问题就是怎么判断图片是不是重复的呢？通过文件名？还是比较大小？好像都不怎么靠谱啊。。突然又是灵光一闪，每个文件不都是有个DNA信息嘛，相同的文件MD5值肯定是一样的嘛。

废话说了这么多，下面说正经的了，首先要怎么获得文件的MD5值呢？这回度娘倒没让我失望了，直接上代码：

```java
String p = "E:\\123.jpg";
FileInputStream fis = new FileInputStream(p);
String md5 = DigestUtils.md5Hex(IOUtils.toByteArray(fis));
IOUtils.closeQuietly(fis);
System.out.println("md5: "+md5);
```

得到所有文件的md5之后进行比较，相同的md5就是重复的文件了。md5已经得到了剩下的就很简单了，通过File取到所有的文件，然后再获取文件的MD5，再写个双重for循环排除掉相同的md5，写完收工搞定。运行起来就等结果了，这一等就是两个小时。。好在结果倒是挺不错。但是这个时间有点让人接受不了啊，这个代码还是有问题啊，得优化。又一想，集合去重复这不可以用Set嘛，赶紧把代码稍作改造，分分钟搞定。。差距也恁大了，看来这java基础还是不够牢固啊。又要从头看一遍书了。。附上最终代码：

```java
String path = "E:\\123";
File dir = new File(path);
String[] files = dir.list();
Map<String,String> map=new HashMap<String,String>();
for (int i = 0; i < files.length; i++)
{
    String p = path + "\\" + files[i];
    FileInputStream fis = new FileInputStream(p);
    String md5 = DigestUtils.md5Hex(IOUtils.toByteArray(fis));
    IOUtils.closeQuietly(fis);
    map.put(md5,files[i]);
}
Iterator<String> it = map.keySet().iterator();
while (it.hasNext())
{
    String md5=it.next();
    String filename=map.get(md5);
    System.out.println("不重复的文件:"+filename);
}
```

各位看官们要是有什么更好的方法可以给我提出来啊。最后还是不管遇到什么问题还是要先仔细的分析研究一下，不要急着动手敲代码，思路清晰了敲出来的代码才会更有效。

明天再准备做一个简单的客户端程序，这样以后就不用每次来运行代码了。回头会把源代码附上。
