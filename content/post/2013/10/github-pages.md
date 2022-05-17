---
title:  GitHub Pages 搭建
date: 2013-10-30
comments: on
categories:  [Other]
tags: [git,github,github pages]
id: 201310300930
---

我写这篇文章的目的是记录本博客的搭建过程，自己从零开始逐步搭建起来了GitHub Pages，其中借鉴了很多的博客和模版，稍后会在后面列出，也为没有用过gihub和jekyll的童鞋提供一点帮助。

学习使用github网页的最好办法就是clone别人的代码，看懂他们的代码，并修改成自己喜欢的样子。这篇文章介绍了windows下从最初安装软件到使用的过程。
<!-- more -->
下面开始一步步讲解Github Pages的使用流程：

## 一、安装git工具

下载安装 [Git for Windows](http://code.google.com/p/msysgit/downloads/list)（选择下载类似于 Git-1.7.*-preview.exe 的文件）
打开安装好的 Git Bash，依次输入：
`git config --global user.name "your username"
git config --global user.email "username@email.com"`
请确保 name 和 email 信息与在 GitHub 注册时的信息相符。
紧接着创建一个 SSH Public Keys，输入：
`ssh-keygen -t rsa -C "username@email.com"`
回车后，你会看到类似画面：

```
Generating public/private rsa key pair.
Enter file in which to save the key (/c/Users/Tekkub/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /c/Users/Tekkub/.ssh/id_rsa.
Your public key has been saved in /c/Users/Tekkub/.ssh/id_rsa.pub.
The key fingerprint is:
e8:ae:60:8f:38:c2:98:1d:6d:84:60:8c:9e:dd:47:81 tekkub@gmail.com
```

此时，你需要的 SSH Public Keys 就保存在 `id_rsa.pub` 文件中，找到并打开它，将里面的代码复制到[Account Settings](https://github.com/account#ssh_bucket) 的相应区域。
后面就轻松多了，因为，除非重装系统或换新机器，你都不必再重复操作以上步骤。

## 二、在windows下安装ruby环境

##### 1). 下载并安装 [RubyInstaller for Windows](http://rubyinstaller.org/downloads/)。

版本可以选择2.0或者1.9.3都可以。

双击安装，安装时选中“Add Ruby executables to your PATH”前的框将ruby添加到环境变量中。

安装完成后，在 Windows 命令行窗口中执行以下命令，检查ruby是否已经加到PATH中： `ruby --version`

##### 2). 安装 [DevKit ](http://rubyinstaller.org/downloads/)。

请根据主页上的描述下载对应的DevKit版本，下载后直接解压到没有空格的路径（例如 E:\DevKit)，然后在Windows的命令行窗口中执行以下命令：

```
E:
cd E:\DevKit
ruby dk.rb init
ruby dk.rb install
```

##### 3). 安装Jekyll和相关的包。

安装完成Ruby和DevKit 后继续安装jekyll，执行如下命令安装：

`gem install jekyll`

等待安装完成即可。

## 三、创建git版本库

登录到自己的Github账户，选择New repository，Project Name命名为：”你的用户名”.github.com，例如我的就叫“lslvxy.github.com”。

完成后在本地克隆jekyll-bootstrap模版，运行命令：

`git clone https://github.com/plusjade/jekyll-bootstrap.git USERNAME.github.com`

将jekyll-bootstrap模版克隆到本地USERNAME.github.com文件夹下。

然后cd到文件夹内运行命令：
`jekyll serve`

成功后打开浏览器输入地址：

[http://localhost:4000](http://localhost:4000) 即可浏览本地生成的页面。

## 四、关于jekyll-bootstrap模版

jekyll-bootstrap是一个搭建好的模版框架，里面提供了常用的插件等内容，包括google analytics 、disqus等。使用jekyll-bootstrap可以加快个人博客的搭建。

类似的模版还有Octopress ，不过Octopress 安装使用较jekyll-bootstrap要麻烦许多，所以我就使用了jekyll-bootstrap。

jekyll-bootstrap的目录结构分析：

其中includes文件夹下内容为包含文件，其他页面可以直接引用。包含了常用的页面和主题等，jekyll-bootstrap是支持更更换主题的。

layouts文件夹内为布局文件，在每个页面的头部都需要指定使用的布局：

```
---
layout: page
header : Post Archive
group: navigation
---
```

---之前不能包含空格等。

posts文件夹为自己写的文章，文件格式必须按照“年-月-日-文章名”进行命名。

_config.yml 文件为必须配置项。

首页为index.md文件。

可以根据自己的实际情况进行修改，可以自定义主题和页面布局等。

## 五、关于jekyll使用过程中的问题

jekyll是不支持中文编码的，若需要添加中文的话需要修改部分代码：

找到ruby的安装目录，比如我本机的地址：D:\Ruby200\lib\ruby\gems\2.0.0\gems\jekyll-1.2.1\lib\jekyll

下的convertible.rb文件，用记事本打开修改第31行代码为:

self.content = File.read(File.join(base, name), :encoding => "utf-8")

打开D:\Ruby200\lib\ruby\gems\2.0.0\gems\jekyll-1.2.1\lib\jekyll\tags目录下的include.rb文件，

修改第58行代码为：

source = File.read(File.join(includes_dir, @file), :encoding => "utf-8")

这样在include模版中也支持中文格式了。

## 六、附加插件

由于gitHub只支持静态页面，所以评论内容需要借助外部插件，可以使用jekyll-bootstrap提供的disqus，disqus是国外最流行的一个评论系统。国内的可以使用多说、友言等。

代码高亮插件可以使用

用js插件：[DlHightLight](http://mihai.bazon.net/projects/javascript-syntax-highlighting-engine)或[Google Code Prettify](http://code.google.com/p/google-code-prettify/)

用[gist](https://gist.github.com/)：强烈推荐菜鸟使用，省心省事，支持语言多

用[pygment](http://pygments.org)：要安装python以及python的包管理软件，又是个大坑，不建议菜鸟使用，尤其是使用windows的

分享插件：国内的[jiathis](http://jiathis.com)和国外的[addthis](http://addthis.com)

图片：国内的[yupoo](http://www.yupoo.com/) 、[poco](http://www.poco.cn/)，国外的[Flickr](http://www.flickr.com/)、[imgur](http://imgur.com)

访问量统计可以使用[CNZZ](http://www.cnzz.com/ "http://www.cnzz.com/")

## 七、其他内容

博客想要做的漂亮并且访问量足够的话是需要下很多功夫的，计划着博客中添加Google+，文章搜索等内容现在还没有添加进去，页面效果这些都需要比较扎实的html和css基础。这些就需要靠自己提高了。

暂时先写这么多吧，以后在慢慢添加，如果有什么问题的话可以Q我活着给我Email都可以的哦！

最后附上我搭建博客时参照的网站：

[Github Pages极简教程](http://www.360doc.com/content/12/0421/09/1016783_205350218.shtml "http://www.360doc.com/content/12/0421/09/1016783_205350218.shtml")

[使用Github Pages建独立博客](http://beiyuu.com/github-pages/#github)

[搭建一个免费的，无限流量的Blog----github Pages和Jekyll入门](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html)

[Jekyll QuickStart](http://jekyllbootstrap.com/usage/jekyll-quick-start.html)

--本篇完--
