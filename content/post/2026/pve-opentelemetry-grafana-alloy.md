---
title:  VE 9 监控新纪元：基于 OpenTelemetry 与 Grafana Alloy 的全栈观测实践
date: 2026-04-16
comments: on
categories:  [PVE]
tags: [PVE,AIO,ALL In One ]
id: 202604161230
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: VE 9 监控新纪元：基于 OpenTelemetry 与 Grafana Alloy 的全栈观测实践
---


# PVE 9 监控新纪元：基于 OpenTelemetry 与 Grafana Alloy 的全栈观测实践

## 引言

随着 Proxmox VE (PVE) 9 的发布，官方原生引入了对 **OpenTelemetry (OTel)** 协议的支持。作为一名深耕 Java 后端与云原生架构的开发者，这无疑是一个令人兴奋的信号：我们终于可以摆脱传统的 InfluxDB 或 Graphite 直连方案，转而使用更加标准化、解耦的观测性管道。

本文将分享如何利用 **PVE 9 + Grafana Alloy + Prometheus** 构建一套生产级的监控系统。

---

## 1. 为什么选择 OpenTelemetry + Alloy？

在传统的监控方案中，PVE 通常直接对接数据库。但在现代架构中，我们追求的是“观测性网关”的概念：

* **解耦化**：PVE 不再关心后端存入哪种数据库。
* **标准化**：OTLP 协议是目前观测性的工业标准，方便后续接入应用层 Trace 和 Log。
* **可视化管道**：Grafana Alloy 提供了图形化的数据流监控，让每一条指标的去向都清晰可见。

---

## 2. 架构设计

整体数据流向如下：
**PVE 9 (指标推送)** -> **Grafana Alloy (接收与转换)** -> **Prometheus (远端写入/存储)** -> **Grafana (可视化大盘)**



---

## 3. 环境部署

建议将监控栈部署在独立的 LXC 容器中，以实现资源隔离。使用 Docker Compose 可以快速拉起核心组件。

### Docker Compose 配置

```yaml
services:
  # Grafana Alloy: 核心采集与分发引擎
  alloy:
    image: grafana/alloy:latest
    container_name: grafana-alloy
    volumes:
      - ./config.alloy:/etc/alloy/config.alloy
    ports:
      - "4318:4318"   # 接收 OTLP HTTP 推送
      - "12345:12345" # Alloy UI 界面
    command: [ "run", "--server.http.listen-addr=0.0.0.0:12345", "/etc/alloy/config.alloy" ]
    restart: unless-stopped

  # Prometheus: 时间序列数据库
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--web.enable-remote-write-receiver' # 必须开启，允许 Alloy 推送数据
    restart: unless-stopped

  # Grafana: 可视化面板
  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

---

## 4. 关键配置文件

### Grafana Alloy 配置 (`config.alloy`)
Alloy 使用声明式语法定义数据管道。我们将 OTLP 接收器的输出直接导向 Prometheus。

```hcl
// 接收 PVE 9 推送
otelcol.receiver.otlp "pve_receiver" {
  http {
    endpoint = "0.0.0.0:4318"
  }
  output {
    metrics = [otelcol.exporter.prometheus.to_prometheus.input]
  }
}

// 协议转换：OTLP -> Prometheus
otelcol.exporter.prometheus "to_prometheus" {
  forward_to = [prometheus.remote_write.local_prom.receiver]
}

// 写入后端存储
prometheus.remote_write "local_prom" {
  endpoint {
    url = "http://prometheus:9090/api/v1/write"
  }
}
```

---

## 5. PVE 9 端配置

登录 PVE 管理后台：
1.  进入 **Datacenter -> Metric Server**。
2.  点击 **Add -> OpenTelemetry**。
3.  **Server**: 填写监控容器的内网 IP。
4.  **Port**: `4318`。
5.  **Path**: `/v1/metrics`。

---

## 6. Grafana 可视化实践

在 PVE 9 的 OTel 模式下，指标命名发生了变化。在 Grafana 中通过 **Explore** 搜索 `pve_` 开头的指标。

### 核心 PromQL 映射参考

| 监控项 | 常用 PromQL |
| :--- | :--- |
| **宿主机 CPU** | `pve_node_cpu_utilization * 100` |
| **宿主机内存** | `pve_node_memory_utilization * 100` |
| **虚拟机实时 CPU** | `pve_guest_cpu_utilization * 100` |
| **存储使用率** | `pve_storage_used_ratio * 100` |

### 面板建议
目前社区专门针对 PVE 9 OTel 的面板尚在完善中，建议基于 **Node Exporter (ID: 1860)** 进行修改，将其中的数据查询项替换为上述 `pve_` 开头的 OTLP 指标。

---

## 总结

通过 PVE 9 原生的 OpenTelemetry 支持，我们不仅提升了监控的标准化程度，还为后续应用层（如 Java 微服务）的接入打下了坚实基础。借助 Grafana Alloy 的可视化能力，监控不再是一个黑盒，而是一条清晰的数据流水线。

---
*本文首发于我的个人博客 https://laysan.site，转载请注明出处。*