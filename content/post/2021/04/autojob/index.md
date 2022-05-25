---
title:  AutoJob 使用文档
date: 2021-04-21
comments: on
categories:  [Other]
tags: [Other ]
id: 202104212330
no_image: https://source.unsplash.com/random/800x600
description: AutoJob 使用文档
---


这里是AutoJob小程序的一个简单的使用手册

欢迎扫码体验

![](autojob.jpg)

## 简介

AutoJob是使用Java开发的一个自动签到的程序，服务端采用springboot+quartz实现，前端使用小程序提供界面和操作

**服务器采用AES加密了账号密码，理论上只要服务器不被黑账号信息不会泄露，也提供了私有化部署的方法，有自己服务器的可以自己部署**

### 私有化部署

**如果你是Javaer，可以直接 clone [AutoJob](https://github.com/lslvxy/autojob-server) 源代码进行部署**

#### 安装OpenJDK环境

推荐安装OpenJDK 1.8 ,OracleJDK 会有验证加密的签名问题，除非不使用加密算法

#### 安装Mysql8环境

安装Mysql8,理论上支持其他关系型数据库，未实际测试

####  下载可执行Jar文件

[releases](https://github.com/lslvxy/autojob-server/releases)地址，请下载`autojob.jar`和`application.yml`文件

#### 修改配置

```yml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:51306/autojob?characterEncoding=utf-8&allowMultiQueries=true&&useAffectedRows=true&useSSL=false
    username: root
    password: ${AUTOJOB_MYSQL_PASSWORD}

server:
  port: 8080   #端口号，如果有端口冲突请修改为其他值

autojob:
  password:
    encrypt: true #是否开启加密
  rsa:
    public_key: ${AUTOJOB_RSA_PUBLIC_KEY} 
    private_key: ${AUTOJOB_RSA_PRIVATE_KEY}

```
url 修改为mysql 的连接地址，修改对应的username和password

`autojob.password.encrypt` 表示是否加密存储账号密码，`true` or `false`

当配置为false的时候不需要配置下面的`rsa.public_key` 和`rsa.private_key`


#### 初始化数据库

```sql
create database autojob default character set utf8mb4
```

数据库实例名称保持和yml中配置的一致

#### 生成加密公私钥

`autojob.password.encrypt`配置为`false`则跳过这一段

使用`cmd`或者`bash` 执行
```bash
java -jar autojob.jar generateKey
```
然后当前目录下会生成`publicKey.txt`和`privateKey.txt`两个文件

将文件内容配置到上面的`rsa.public_key` 和`rsa.private_key`中


#### 运行项目

使用`cmd`或者`bash` 执行
```bash
java -jar autojob.jar -Dspring.config.location=application.yml
```

#### 添加账号

在`autojob_user`表添加用户信息

在`autojob_account`表添加账号信息


### Docker部署

## 支持项目

* 时光相册
* 天翼网盘

### Server酱推送

可选配置,填写SCKEY可以推送签到消息到微信

小程序默认会推送订阅消息,需要手动确认下,勾选同意不再询问则每天自动签到完成都会推送消息

自行配置`SCKEY`,[Server酱官网](http://sc.ftqq.com/)

### 时光相册

直接新增配置账号密码即可

### 天翼网盘

使用账号密码登录

**没有设置密码的请去cloud.189.cn设置一下**

**签到提示验证码的请 [点击这里](https://cloud.189.cn/udb/udb_login.jsp?pageId=1&redirectURL=/main.action) 选择账号密码登录,一般会有验证码弹出来,退出多登录几次一般就不需要验证码了**



