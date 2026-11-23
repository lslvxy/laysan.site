---
title: "PVE 家庭组网中的双网卡、远程访问与 DNS 排查"
date: 2026-11-23
comments: on
categories: [PVE]
tags: [PVE, OpenWrt, Tailscale, Cloudflare Tunnel, DNS, IPv6]
id: 202611232356
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: "记录 PVE 家庭组网的双网卡单默认路由、Tailscale 和 Cloudflare Tunnel，以及定位 TP-Link 静态域名映射的 EDNS 和 AAAA 异常、清理 OpenWrt 临时规则的过程。"
---

家里的 PVE 会按需关机。我希望在家能直接用 IP 访问服务，在外能用域名打开 Plex、Emby 和监控页，自己也能远程管理 PVE。普通上网则始终由 TP-Link 提供网关和 DHCP，家庭设备使用公共 DNS。这样 PVE 停机时，家庭上网和自建服务的可用性各自有清楚的边界。

这次沿用了之前的 Cloudflare Tunnel 和 Nginx Proxy Manager（NPM），主要调整了容器的路由，并试验了同域名的内外网分流。文中的公网域名使用示例值。[此前的 Tunnel 与 NPM 配置](/2026/04/pve-cloudflare-tunnel-npm/)

## 家庭网和 PVE 内部网

| 组件 | 家庭网 `vmbr0` | PVE 内部网 `vmbr1` | 用途 |
| --- | --- | --- | --- |
| TP-Link | `192.168.50.1` | — | 家庭网关和 DHCP |
| PVE | `192.168.50.177` | `10.10.10.177` | 宿主机管理和虚拟网桥 |
| OpenWrt · VM 100 | `192.168.50.200` | `10.10.10.10` | 按需使用 Nikki，保留内部网接口 |
| Tailscale · LXC 109 | `192.168.50.109` | `10.10.10.109` | 发布两个 IPv4 子网 |
| NPM 和 cloudflared · LXC 119 | `192.168.50.119` | `10.10.10.119` | 接收隧道请求并转发到后端 |

`vmbr0` 接家庭 LAN，`vmbr1` 承载 PVE 内部通信。119 访问 `10.10.10.x` 后端时，两端同属一个网段，可以直接经 `vmbr1` 通信。双网卡的业务容器也接在家庭 LAN，能从家庭网访问哪些端口取决于应用的监听地址和防火墙。

## 双网卡只保留一个 IPv4 默认网关

问题最早出现在 109。运行中的默认路由已经指向 TP-Link，但 PVE 持久配置仍给第二张网卡填了 `10.10.10.10`。Debian 的启动日志出现 `RTNETLINK answers: File exists`，`networking.service` 随后报错。另一些容器的运行路由表则同时装入了两条默认路由。

统一后的设置是，`eth0` 保留原来的静态 IPv4 或 DHCP，默认网关由 TP-Link 提供。接 `vmbr1` 的 `eth1` 保留 `10.10.10.x/24`，网关留空。同网段的回源和互访由内核生成的直连路由处理。

在 PVE 宿主机上，可以用下面几条命令对照持久配置和实际选路。

```bash
pct config 109 --current
pct exec 109 -- ip -4 route show table all
pct exec 109 -- ip -4 route get 1.1.1.1
pct exec 109 -- ip -4 route get 10.10.10.119
```

预期外网地址经 `192.168.50.1` 从 `eth0` 发出，内部地址从 `eth1` 直达。修改第二张网卡时，还要在应用后立即检查默认路由。PVE 的运行中网卡更新可能暂时移除当前默认路由，处理管理容器或远程入口时，最好能从宿主机控制台恢复。

调整完成后，我检查了 PVE 中保存的网卡配置、在线容器的路由表、OpenWrt 转发规则的计数以及连接跟踪表。确认观察期间没有设备使用旧路径后，才移除 OpenWrt 上允许 `10.10.10.0/24` 转发到外网的临时规则及对应的 IPv4 masquerade。

## 在家用 IP，在外用域名或 Tailscale

在家可以直接访问业务容器的家庭网 IP 和服务端口。访问公开域名时，请求由 Cloudflare 接收，经 Tunnel 送到 119 的 cloudflared，再由 NPM 按域名转发到后端。多数后端的回源地址使用 `10.10.10.x`。Cloudflared 主动建立外连，家庭路由器可以保持现有的入站规则。[Cloudflare Tunnel 防火墙说明](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/)

我自己在外管理设备时，通过 109 的 Tailscale 子网路由访问 `192.168.50.0/24` 和 `10.10.10.0/24`。109 同时直连这两个网段，并使用 Tailscale 默认的子网路由源地址转换。[Tailscale 子网路由说明](https://tailscale.com/docs/features/subnet-routers)

验证 NPM 时，先在家庭网用 `curl --resolve` 将业务域名临时指向 119。这样能同时验证目标 IP、域名对应的虚拟主机和 HTTPS 证书。再用公网解析走 Cloudflare，比较两条链路的 HTTP 状态。命令里的示例域名需替换为实际配置且证书覆盖的域名。

```bash
curl --resolve media.example.com:443:192.168.50.119 \
  -sS -o /dev/null -w 'https=%{http_code} peer=%{remote_ip}\n' \
  https://media.example.com/identity
```

## 同域名分流试验遇到了两层 DNS 问题

第一层在 OpenWrt。dnsmasq 可以给已选域名返回 119 的内网 A 记录，并对这些域名的 AAAA 查询返回空应答。Nikki 在同一台 OpenWrt 上接管了部分 DNS 查询。单台设备把 DNS 指向 OpenWrt 后，查询普通域名得到了 `198.18.x.x` 的 Fake-IP。测试设备的默认网关仍是 TP-Link，经这个网关访问 Fake-IP 会超时。把发往 OpenWrt 本机 DNS 地址的查询临时交给 dnsmasq 后，三个业务域名和普通网站都通过了测试。[dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html) · [Mihomo DNS 配置](https://wiki.metacubex.one/en/config/dns/)

第二层在 TP-Link 本机。测试的 SAR205GP-CT-H 支持「静态域名映射」，可把 Plex、Emby 和监控页指向 119。单台 Linux 客户端用了 TP-Link 的 DNS 后，三个原域名的 HTTPS 访问都能直连。进一步对比原始 DNS 报文，发现静态映射的响应有两处格式异常。

- 带 EDNS 的查询会把 `OPT` 记录放在应答区，真正的地址记录留在报文尾部，且没有计入应答。标准要求 `OPT` 位于附加记录区。[RFC 6891](https://datatracker.ietf.org/doc/html/rfc6891#section-6.1.1)
- 普通 AAAA 查询会收到一条长度为 4 字节的 AAAA 记录。IPv6 地址应占 16 字节。对这些仅设置内网 IPv4 的域名，预期是有效的空 AAAA 应答。[RFC 3596](https://datatracker.ietf.org/doc/html/rfc3596#section-2.2)

下面三条查询分别检查普通 A、EDNS A 和 AAAA。用同一台设备查询一个未映射的公网域名作对照，可以缩小排查范围。

```bash
dig @192.168.50.1 media.example.com A +noedns
dig @192.168.50.1 media.example.com A +edns=0
dig @192.168.50.1 media.example.com AAAA +noedns
```

这台 TP-Link 的「DNS 策略」只能选择出接口。最终停用了 TP-Link 上的试验映射，并移除了 dnsmasq 和 Nikki 的三条域名覆盖及试验期间新增的 DNS 旁路规则。OpenWrt 的 dnsmasq 收回到 `127.0.0.1` 和 `::1`，供本机使用。Nikki 的 DNS 和代理继续运行。家庭 DHCP 继续下发公共 DNS。

## IPv6 单独验证

家庭侧网卡在 PVE 里统一设为 SLAAC。客户端从路由通告（RA）学习前缀和默认路由。DHCPv6 可以分配地址，IPv6 默认网关仍由 RA 提供。109 启用了 IPv6 转发，因此家庭侧需要 `accept_ra=2`，才能在转发开启时接收通告。[RFC 8504](https://datatracker.ietf.org/doc/html/rfc8504#section-8.2) · [Linux 内核 IPv6 sysctl 文档](https://docs.kernel.org/networking/ip-sysctl.html#conf-interface-accept-ra)

部分在线容器实测经 IPv6 访问 HTTPS 成功。另外几台在复测时还没有 IPv6 默认路由。要给独立的 `vmbr1` 提供原生 IPv6，需要上游能向这个网段另行路由一个 `/64`。当前的回源和远程管理继续使用 IPv4。

## 最终复测

| 验证项 | 结果 |
| --- | --- |
| LXC IPv4 出网 | 10 个在线容器都经 TP-Link，访问测试网站均返回 HTTPS `200` |
| OpenWrt 和 Nikki | 两个回环地址的 DNS 查询成功，Nikki 的 DNS 和 HTTPS 代理均通过 |
| Nginx 与公网 Tunnel | Nginx 配置检查通过，Plex、Emby 和监控页的公网请求分别返回 `200`、`200`、`302`，均带 `CF-Ray` |
| Tailscale | 109 在线，两个 IPv4 子网路由生效 |
| 家庭上网 | 客户端仍取得 TP-Link 网关和公共 DNS。DNS 与网站连通性均通过实测 |

家庭上网独立于 PVE 的结论来自 DHCP 下发值和实际路由检查。本次没有做整机断电测试。PVE 停机时，上面承载的服务、Tunnel 和 Tailscale 子网入口也会随之停用。
