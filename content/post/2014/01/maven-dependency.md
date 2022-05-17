---
title:  Maven排除项目中同名不同版本的jar
date: 2014-01-13
comments: on
categories:  [Java]
tags: [maven,jar,版本]
id: 201401130930
---
有人认为Maven是一个依赖管理工具，当然这种想法是错误的（确切的说Maven是一个项目管理工具，贯穿了整个项目生命周期，编译，测试，打包，发布...），但Maven给人造成这种错误的印象也是有原因的，因为Maven的依赖管理十分强大，用好了Maven，你不再需要面对一大堆jar感到头大，依赖冲突，无用依赖等问题也能够得到有效的防止和解决。
<!-- more -->
今天突然发现web项目打包后的exe居然有200M+了，心想不应该有这么大的啊，于是检查了一番发现引用的jar有130+个，仔细一瞅发现好多同名的但是不同版本的jar，比如说有commons-httpclient就有两个，3.0和3.1版本的。这样直接导致了lib下有很多重复的jar，安装程序体积自然就上去了。

打开POM.xml，运行了一下mvn dependency:tree 命令，查看依赖关系树形结构发现有两个jar都是依赖了commons-httpclient这个jar，但是这两个依赖的版本是不一样的，所以maven就把两个版本的都添加进来了。

解决办法就是通过exclusions配置dependency中要排除的jar文件。
示例如下：

```js
<dependency>
	<groupId>org.codehaus.xfire </groupId>
	<artifactId>xfire-all </artifactId>
	<version>1.2.6 </version>
	<exclusions>
		<exclusion>
			<groupId>org.springframework </groupId>
			<artifactId>spring </artifactId>
		</exclusion>
	</exclusions>
</dependency>
```

这样就排除了xfire中的spring依赖。同理，根据maven依赖树可以看到哪些jar是重复依赖的，然后通过exclusions排除掉重复的项就可以了。
