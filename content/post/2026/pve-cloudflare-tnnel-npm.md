---
title:  家庭实验室（Home Lab）网络架构演进：从旁路由劫持到 Cloudflare Tunnel + NPM 方案
date: 2026-04-15
comments: on
categories:  [PVE]
tags: [PVE,AIO,ALL In One ]
id: 202604041230
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: 家庭实验室（Home Lab）网络架构演进：从旁路由劫持到 Cloudflare Tunnel + NPM 方案
---


# 家庭实验室（Home Lab）网络架构演进：从旁路由劫持到 Cloudflare Tunnel + NPM 方案

在构建家庭实验室的过程中，如何优雅地从公网访问内网服务，并兼顾内网直连的速度与稳定性，一直是核心挑战。本文记录了我的架构从**旁路由 DNS 劫持**向 **Cloudflare Tunnel + Nginx Proxy Manager (NPM)** 演进的过程，以及如何解决 Docker 容器回环访问等棘手问题。

---

## 1. 架构演进：为什么放弃旁路由 DNS 劫持？

最初，我尝试在硬路由（TP-Link）下挂载 OpenWrt 旁路由，通过 Dnsmasq 实现“内外网分流”。

* **痛点**：
    1.  **单点故障**：旁路由（LXC 容器）一旦挂掉，全家 DNS 解析失效。
    2.  **切换冲突**：移动设备在内外网切换时，DNS 缓存常导致解析结果异常。
    3.  **配置复杂**：需要处理 NAT 回流（NAT Loopback）以及各种防火墙规则。

**最终方案**：采用 **All-in-Cloudflare** 策略。所有流量通过隧道进入，NPM 负责内网分发。这种方案无需公网 IP，无需开启路由器端口映射，安全性最高。

---

## 2. 核心组件拓扑

该架构全部运行在 **Proxmox VE (PVE)** 的一个 **LXC 容器**内，底层基于 Docker 部署。

* **Cloudflare Tunnel**: 建立安全隧道，将 `*.yourdomain.biz` 流量拉入内网。
* **Nginx Proxy Manager (NPM)**: 流量总闸，负责 SSL 卸载和反向代理。
* **应用服务**: 如 Homepage、Containerd 业务应用等。



---

## 3. 关键配置步骤

### 3.1 统一 Docker 内部网络
为了避免“回环访问”失败（即容器通过宿主机 IP 访问自身失败），必须将所有容器放入同一个 Docker 虚拟网络中。

```bash
# 创建自定义网桥
docker network create proxy-net

# 将所有关键容器加入网络
docker network connect proxy-net cloudflared
docker network connect proxy-net nginx-proxy-manager
docker network connect proxy-net homepage
```

### 3.2 Cloudflare Tunnel 配置
在 Cloudflare Zero Trust 面板中，使用通配符配置，实现“一劳永逸”：

1.  **Public Hostname**: 配置为 `*.yourdomain.biz`。
2.  **Service URL**: 填写 `http://nginx-proxy-manager:80`（**注意：** 直接使用容器名，而非 IP）。
3.  **DNS 设置**: 在 Cloudflare DNS 中添加一条 CNAME 记录，名称为 `*`，目标指向你的隧道 ID。

### 3.3 NPM 反向代理配置
在 NPM 管理界面（81 端口），配置具体的转发规则。以代理 NPM 自身后台为例：

* **Domain Name**: `npm.yourdomain.biz`
* **Forward Hostname**: `nginx-proxy-manager` (或 `127.0.0.1`)
* **Forward Port**: `81`
* **Websockets Support**: **必须开启**（管理后台依赖此协议）。

---

## 4. 常见坑点与排查（Q&A）

### Q: 访问域名时出现 301 重定向循环？
**原因**：Cloudflare 开启了强制 HTTPS，而 NPM 内部也开启了 "Force SSL"，两者在握手协议上不一致。
**解决**：
1.  在 NPM 中取消勾选 **Force SSL**。
2.  在 Cloudflare 后台将 SSL 模式设置为 **Full**。

### Q: 为什么访问未配置的域名会看到 "Congratulations"？
**原因**：这说明流量已成功到达 NPM，但 NPM 找不到对应的 Host，跳转到了默认站点。
**解决**：在 NPM 中检查 `Proxy Host` 里的域名拼写是否与访问的 URL 完全一致。

### Q: 为什么日志显示 "stream canceled with error code 0"？
**原因**：通常是反向代理的后端服务不可达，或者 Docker 容器间网络不通。
**解决**：进入 Tunnel 容器内部，使用 `curl -I http://nginx-proxy-manager:80` 测试连通性。

---

## 5. 总结
通过这套架构，我实现了：
1.  **极简配置**：新增服务只需在 NPM 点几下，无需动域名解析和隧道。
2.  **全链路加密**：Cloudflare 边缘证书 + NPM 内部转发。
3.  **高可用性**：即便旁路系统挂了，也不影响基础局域网的稳定性。
