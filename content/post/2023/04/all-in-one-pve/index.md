---
title:  从零开始的 All In One With PVE 之一 硬件配置与系统安装
date: 2023-04-06
comments: on
categories:  [PVE]
tags: [PVE,AIO,ALL In One ]
id: 202304061230
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: 从零开始的 All In One With PVE 之一 硬件配置与系统安装
---


本系列记录自己的小机 All In One 的折腾之路,坚持不断更!

# 硬件配置

一直想拥有一个自己的服务器,之前一直用的群辉,没有关注过 MicorServer 这一块。一次无意中看到了HPE Gen 10 plus这款机器瞬间背迷住了,立即转手出掉了陪伴自己已久的940+,转身投入了Gen10+ 的怀抱里。历时2个月从CU上淘了一台，加上硬盘就能投入使用了。

目前机器的配置如下
* 512G SSD  * 2
* 2T   SSD  * 2
* 18T  HDD  * 1

硬盘的规划是1个512G SSD 作为PVE 系统盘用转接器安装在PCI上

1个512G SSD 做黑群辉做照片备份

2个2T SSD 做ZFS 给各个虚拟机和容器使用

HDD 则作为冷备份和低频文件存储

# 系统选择
尝试过一段时间Unraid和PVE 最终还是选择了PVE。

Unraid 界面操作友好，Docker、磁盘阵列、显卡直通、虚拟U盘等都是亮点,必须U盘引导有点麻烦（廉价U盘7x24工作，心还是很慌）

PVE 需要一定的Linux 基础，对自己来说问题不大，所以还是选择了PVE。

# PVE 安装

PVE 的安装还是很方便的，安装官网的步骤刻录好U盘，机器设置U盘启动直接启动U盘安装就可以了。

刻录U盘的步骤见 [installation_prepare_media](https://pve.proxmox.com/wiki/Prepare_Installation_Media#installation_prepare_media) 

安装重启后即可看到管理地址。也可以此时登陆控制台进行高级操作。

# 虚拟机规划

目前已经搭建好的虚拟机和容器有
* Openwrt 软路由
* Synology 群辉
* Plex 媒体服务
* MariaDB Mysql 数据库
* Postgresql PG 数据库
* Minio OSS 存储
* Redis KV 缓存
* Immich 照片备份管理(替换Synology Photos)
* Dashy Dashboard 

# PVE 初始配置
PVE 安装完成后需要进行一些配置,推荐一个脚本库提供了很多有用的配置脚本和容器的一键创建,非常的方便 [tteck] https://github.com/tteck/Proxmox

## 配置Debian 国内源

参考 [中科大源](http://mirrors.ustc.edu.cn/help/proxmox.html) 修改 Debian 以及 CT 模板的源


## 移除 Enterprise Repo 及 No-Subscription 弹窗
```
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)"
```

## 暗黑主题
PVE 最新版(7.4.x)已经原生支持黑色主题,之前的版本可以额外安装,使用如下脚本即可自动安装
```
bash <(curl -s https://raw.githubusercontent.com/Weilbyte/PVEDiscordDark/master/PVEDiscordDark.sh ) install
```

至此 PVE 已经可以投入到日常的运行中了,下一篇将介绍如何配置OpenWrt软路由及PVE各虚拟机直接的内网访问和传输配置。



