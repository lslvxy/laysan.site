---
title:  PVE 报错  Unable to create new inotify object 解决方案
date: 2024-12-04
comments: on
categories:  [PVE]
tags: [PVE,AIO,ALL In One ]
id: 202412041230
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: PVE 报错  Unable to create new inotify object 解决方案
---


# 执行PVE pct 等命令时报错 
```shell
Unable to create new inotify object: Too many open files at /usr/share/perl5/PVE/INotify.pm line 398.
```
# 原因


检查是否是启动了很多的LXC, 需要增加inotify 的限制

执行命令`sysctl fs.inotify` 检查 max_user_instances

```shell
# sysctl fs.inotify
fs.inotify.max_queued_events = 16384
fs.inotify.max_user_instances = 128
fs.inotify.max_user_watches = 65536
```
# 解决方案

增加 max_user_instances的值

```shell
sysctl fs.inotify.max_user_instances=512
```