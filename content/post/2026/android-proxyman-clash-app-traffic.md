---
title: "Android 单应用抓包：用 Clash 和 Proxyman 采集域名与调试 HTTPS"
date: 2026-11-20
comments: on
categories: [Android]
tags: [Android, macOS, Proxyman, Clash, Mihomo]
id: 202611201606
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: "在 Android 上用 Clash（Mihomo）的分应用 VPN 将单个 App 的流量转发到 Mac 上的 Proxyman，采集域名白名单，并在自家调试包中查看 HTTPS 请求和响应。"
---

给 Android 的 Wi-Fi 配置全局 HTTP 代理后，浏览器和后台服务的请求很容易混在一起。如果只想知道某个 App 在启动、登录或打开特定页面时访问了哪些域名，可以让 Clash（Mihomo）通过 Android 的 VPN 只接管这个 App，再把它的 TCP 连接交给 Mac 上的 Proxyman。

这套分流方法适用于已 Root 和未 Root 的设备。**整理域名时，保持 HTTPS 隧道直通，手机无需安装代理证书。** 调试自家 App 的请求头、请求体或响应体时，再为测试域名开启 SSL Proxying。

## 1. 准备 Mac 上的 Proxyman

1. 让手机和 Mac 接入彼此可访问的局域网。在 Mac 的「系统设置 → Wi-Fi → 详细信息 → TCP/IP」查看局域网 IP，例如 `192.168.1.100`。
2. 打开 Proxyman，确认代理监听端口和录制状态。默认端口为 `9090`。如果启用了 Proxyman 的 **Access Control**，把测试手机的 IP 加入允许列表。macOS 防火墙也需要允许 Proxyman 接收入站连接。
3. 清除手机 Wi-Fi 上手动配置的 HTTP 代理，断开其他 VPN。后续由 Android 的分应用 VPN 接管目标 App。

域名采集前，打开 Proxyman 的 **SSL Proxying List**，暂时停用会命中目标流量的解密规则，尤其是匹配所有域名的 `*`。如果 Mac 本机流量也在录制，采集和导出时按手机这个远程来源筛选。[Proxyman Android 设置](https://proxyman.com/docs/debug-devices/android-device) · [Access Control](https://proxyman.com/docs/advanced-features/access-control) · [SSL Proxying](https://proxyman.com/docs/basic-features/ssl-proxying)

## 2. 设置 Android 分应用代理

新建 `proxyman.yaml`，把 `server` 和 `port` 换成 Mac 上的实际值。这里使用 Mihomo 的**规则模式（Rule）**，确保客户端执行下方的 UDP 规则。

```yaml
mode: rule
log-level: info

proxies:
  - name: Mac-Proxyman
    type: http
    server: 192.168.1.100
    port: 9090

sniffer:
  enable: true
  parse-pure-ip: true
  override-destination: true
  sniff:
    HTTP:
      ports: [80, 8080]
    TLS:
      ports: [443, 8443]

rules:
  - AND,((NETWORK,udp),(DST-PORT,53)),DIRECT
  - NETWORK,udp,REJECT
  - MATCH,Mac-Proxyman
```

第一条规则让进入规则匹配的普通 UDP DNS 查询直连。第二条拒绝其余 UDP，因为这里使用的 HTTP 代理承载的是 TCP。常见的 HTTP/3（QUIC）流量使用 UDP 443，拒绝后客户端可能回退到基于 TCP 的 HTTPS。依赖 UDP 且没有 TCP 回退的功能可能无法运行，测试记录里要注明这个限制。[Mihomo 运行模式](https://wiki.metacubex.one/config/general/) · [Mihomo 路由规则](https://wiki.metacubex.one/config/rules/) · [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html#section-3.1)

分应用 VPN 接收到的目标地址有时只有 IP。上面的 `sniffer` 会尝试从 HTTP Host 或可见的 TLS SNI 获取域名，并在识别成功时将它用作代理的目标地址。这可能改变解析结果。遇到直连 IP、无可见 SNI 或启用 ECH 的连接时，保留实际观察到的 IP，并注明域名未知。[Mihomo 域名嗅探](https://wiki.metacubex.one/config/sniff/) · [Android 网络安全配置](https://developer.android.com/privacy-and-security/security-config#domainEncryption)

以支持 Mihomo 的 Android 客户端 FlClash 为例，导入配置后按下面的顺序检查。

1. 导入并启用 `proxyman.yaml`。确认客户端界面仍显示 **Rule**，有些客户端会记住上次选用的模式。
2. 打开 VPN / TUN 模式。在「应用访问控制」中选择**白名单模式**，只勾选目标 App，重连 VPN 使名单生效。
3. 强行停止目标 App，清空 Proxyman 的旧记录，再冷启动 App。到 Clash 的连接列表确认命中了 `Mac-Proxyman`，到 Proxyman 确认出现来自手机的连接。

白名单按 Android 应用包生效。如果登录跳转到外部浏览器，或推送走独立的系统服务，那部分流量可能需要单独采集。[Android 分应用 VPN](https://developer.android.com/develop/connectivity/vpn#per-app) · [FlClash 应用访问控制](https://github.com/chen08209/FlClash/blob/main/arb/intl_en.arb)

## 3. 采集域名并整理白名单

依次操作需要覆盖的流程，例如冷启动、登录、首页、个人中心和客服。记录每轮的 App 版本、操作和触发的域名。HTTPS 隧道通常会留下 `CONNECT` 目标，例如 `api.example.com:443`。所见的主机名取决于 Clash 转发时带上的目标地址。HTTPS 请求路径、头部和正文仍在加密隧道内。[RFC 9110 的 CONNECT 说明](https://www.rfc-editor.org/rfc/rfc9110.html#name-connect)

只需要域名清单时，可以直接根据 Proxyman 左栏的远程设备和域名分组整理。记录较多时，从手机来源选择请求，右键 **Export → HAR**，保存为 `exported.har`。在 HAR 所在目录运行下面的 Python 3 命令。它会解析请求 URL，去掉端口和域名末尾的点，将域名转成小写并去重。IPv4 和 IPv6 地址统一另存为 IP 清单。[Proxyman 导出文档](https://proxyman.com/docs/basic-features/import-export)

```bash
python3 - <<'PY'
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

with Path("exported.har").open(encoding="utf-8-sig") as har_file:
    entries = json.load(har_file)["log"]["entries"]

domains = set()
addresses = set()
for entry in entries:
    try:
        url = urlsplit(entry["request"]["url"])
    except ValueError:
        continue
    if url.scheme not in {"http", "https"} or not url.hostname:
        continue

    host = url.hostname.lower().rstrip(".")
    if not host:
        continue
    try:
        addresses.add(str(ipaddress.ip_address(host)))
    except ValueError:
        domains.add(host)

Path("whitelist_domains.txt").write_text(
    "".join(f"{host}\n" for host in sorted(domains)), encoding="utf-8"
)
Path("observed_ips.txt").write_text(
    "".join(f"{address}\n" for address in sorted(addresses)), encoding="utf-8"
)
PY
```

HAR 中可能缺少只建立了隧道的 `CONNECT` 记录，也可能有不带完整 URL 的条目。回到 Proxyman 界面补录这些隧道的目标，再按业务流程复核。只在特定账号、地区或时间触发的访问需要另行覆盖。IP 可能属于共享 CDN 或来自动态解析，确认用途后再制定对应规则。

## 4. 在自家 App 的调试包里查看 HTTPS 明文

已 Root 和未 Root 的手机都可以用同一套调试包配置。先在 Mac 上从 **Certificate → Export → Root Certificate as PEM** 导出 Proxyman CA，再将公开证书放到 Android 项目的 `app/src/debug/res/raw/proxyman_ca.pem`。在 `app/src/debug/res/xml/network_security_config.xml` 中声明该证书。

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <debug-overrides>
        <trust-anchors>
            <certificates src="@raw/proxyman_ca" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

在 `app/src/debug/AndroidManifest.xml` 中，让 `<application>` 引用这份配置。

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:networkSecurityConfig="@xml/network_security_config" />
</manifest>
```

项目若已引用同名资源，在 debug 资源中保留原有的域名与信任配置，只合并 `debug-overrides`。如果已有其他文件名的配置，也可以沿用原名称，并保持 Manifest 引用一致。Android 只会在可调试构建中应用 `debug-overrides`。应用自己的 TLS 实现可能还需要由开发者在调试构建中配置测试 CA。[Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config#debug-overrides)

安装调试包后，在 Clash 的白名单中选中调试包实际使用的应用包名。在 Proxyman 找到自家测试域名，右键 **Enable SSL Proxying**，重启 App 或重新发起请求。连通后，Proxyman 会显示实际的 HTTP 方法、路径、请求头和响应。调试完成后关闭 VPN 和临时的 SSL Proxying 规则。需要共享时优先发送域名清单，原始 HAR 可能包含令牌、Cookie 和业务数据。[Proxyman SSL Proxying](https://proxyman.com/docs/basic-features/ssl-proxying)

对于已 Root 的实体测试机，分应用转发和上述调试包流程都可以照常使用。Android 14 起，系统根证书还涉及 Conscrypt APEX，单独往旧版系统证书目录复制文件可能对目标进程无效。确实需要测试系统 CA 行为时，可以用 Proxyman 官方支持的 Android 模拟器流程，结束后恢复代理设置。[Android Conscrypt 文档](https://source.android.com/docs/core/ota/modular-system/conscrypt#changes-in-android-14) · [Proxyman 模拟器设置](https://proxyman.com/docs/debug-devices/android-device/automatic-script-for-android-emulator)

## 5. 常见问题

| 现象 | 排查方法 |
| --- | --- |
| 开启 VPN 后 App 无法访问，Proxyman 也没有记录 | 核对 Mac 当前的 IP、监听端口和录制状态，再检查防火墙、Proxyman Access Control 和 Wi-Fi 客户端隔离。 |
| Proxyman 出现大量无关请求 | 检查 Clash 是否开启了应用访问控制并处于白名单模式，设置后重连 VPN。导出时只选手机来源。 |
| 能看到 `CONNECT`，看不到 URL 路径或正文 | 域名采集使用隧道直通，这是预期结果。调试自家 App 时，为测试域名开启 SSL Proxying，并用信任测试 CA 的调试包重新发起请求。 |
| 采集域名时出现 TLS 握手失败，App 卡在首屏 | 检查是否仍有 SSL Proxying 规则匹配该域名。关闭命中的解密规则，再冷启动重试。 |
| 调试包开启 SSL Proxying 后握手失败 | 确认装的是正确的 debug 构建、Manifest 引用了调试配置，并检查包内 CA 是否来自当前的 Proxyman 实例。 |
| 域名列表中出现 IP 地址 | 查看 Clash 连接详情，确认它是否识别出了主机名。无法确认时，单独记录 IP 和触发场景。 |
