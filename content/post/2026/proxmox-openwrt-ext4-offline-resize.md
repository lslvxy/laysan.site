---
title: Proxmox VE 给 OpenWrt 扩盘后仍只有 100 MB？离线扩展 ext4 根分区
date: 2026-11-19
comments: on
categories:  [PVE]
tags: [PVE,AIO,ALL In One ]
id: 202611191230
no_image: https://cdn.jsdelivr.net/gh/lslvxy/imgs@main/pics/20230406161428.jpg
description: Proxmox VE 给 OpenWrt 扩盘后仍只有 100 MB？离线扩展 ext4 根分区
---

在 Proxmox VE（PVE）里把 OpenWrt 虚拟机的磁盘扩到 32 GiB，进系统执行 `df -h`，根目录却还只有 98.3 MiB。原因是虚拟磁盘、分区和文件系统各自记录容量。PVE 已经增大了虚拟磁盘，还需要把尾部空间分给根分区，再扩展分区里的 ext4。

这次使用 OpenWrt x86/64、BIOS 启动、MBR 分区表，虚拟磁盘存放在 PVE 的 LVM-thin 存储 `local-lvm`。虚拟机里的 `parted` 缺少共享库，`resize2fs` 也没有安装。我在 OpenWrt 正常关机后，直接用 PVE 宿主机上的工具扩展分区和文件系统。操作完成后，`df -h` 显示根目录 **31.6 GiB**，可用 **31.5 GiB**，网络、防火墙和 DHCP 的配置文件校验值均与扩容前一致。

| 检查项 | 扩容前 | 扩容后 |
| --- | --- | --- |
| PVE 虚拟磁盘 `scsi0` | 32 GiB | 32 GiB |
| OpenWrt 根分区 `/dev/sda2` | 104 MiB | 约 32 GiB |
| `df -h` 显示的根文件系统 | 98.3 MiB | 31.6 GiB |
| 根目录可用空间 | 48.6 MiB | 31.5 GiB |

## 1. 确认这套步骤适用

本文的写盘命令适用于以下布局。实际操作时，从自己的机器读取设备名和扇区数。

- PVE 上能通过 `pvesm path` 找到对应的 LVM-thin 块设备。
- 虚拟磁盘采用 DOS/MBR 分区表，逻辑扇区为 512 字节，根分区是第二个主分区，分区后面直到磁盘末尾都是未分配空间。
- OpenWrt 的 `/` 直接挂载在第二分区上，文件系统类型为 ext4。
- 维护期间可以关闭 OpenWrt。如果它承担网关职责，管理电脑需要能在 OpenWrt 下线时继续访问 PVE，或能使用宿主机控制台。

如果看到 GPT、`squashfs`、独立的 `/overlay`，或根分区后另有分区，请先重新确认布局。特别是 SquashFS 镜像，可写空间通常来自 `rootfs_data`，要先识别它的文件系统和挂载方式。本文的 MBR 检查和 ext4 写盘命令面向上面列出的布局。[OpenWrt x86 安装与分区说明](https://openwrt.org/docs/guide-user/installation/openwrt_x86) · [OpenWrt Extroot 文档](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)

### 在 OpenWrt 上确认根文件系统

```bash
df -h
cat /proc/partitions
awk '$5 == "/" || $5 == "/overlay" || $5 == "/boot"' /proc/self/mountinfo
cat /proc/cmdline
cat /sys/class/block/sda2/start
cat /sys/class/block/sda2/size
```

本例中，`/proc/partitions` 已显示 `sda` 有 32 GiB。根挂载的设备号为 `8:2`，对应 `/dev/sda2`，类型是 ext4，挂载点为 `/`。即使系统没有可访问的 `/dev/root` 设备节点，也可以通过设备号确认来源。启动参数里有 `root=PARTUUID=011cbbbd-02`，后续要保留 MBR 磁盘签名和分区编号。

### 在 PVE 上确认虚拟磁盘

以下 PVE 命令使用 root 的 Bash 会话。本文的虚拟机 ID 是 `100`，请以自己的 `qm config` 输出为准。

```bash
VMID=100
qm status "$VMID"
qm config "$VMID" --current

# 本例的 scsi0 指向此卷。请按实际配置填写。
VOLID=local-lvm:vm-100-disk-0
DISK=$(pvesm path "$VOLID")
printf 'PVE 块设备 %s\n' "$DISK"
test -b "$DISK"

lsblk -dn -o NAME,MAJ:MIN,SIZE,TYPE "$DISK"
blockdev --getss "$DISK"
blockdev --getsize64 "$DISK"
sfdisk --dump "$DISK"
sfdisk --list-free "$DISK"
```

关机前可在 PVE 检查所需工具是否齐全。下面的命令会打印可执行文件路径，缺失的工具会单独标出来。

```bash
for tool in sfdisk kpartx dmsetup blkid e2fsck resize2fs tune2fs vzdump zstd vma; do
  command -v "$tool" || printf '缺少 %s\n' "$tool"
done
```

本例的宿主机设备是 `/dev/pve/vm-100-disk-0`。OpenWrt 里的 `/dev/sda` 是虚拟机看到的设备名，PVE 宿主机也可能有自己的 `/dev/sda`。在 PVE 上只操作已经通过虚拟机配置和存储卷 ID 对上的 `$DISK`。

本例的分区表如下，单位是扇区。

```text
label: dos
label-id: 0x011cbbbd
sector-size: 512

p1 : start=   512, size= 32768, type=83, bootable
p2 : start= 33792, size=212992, type=83
```

`sfdisk --list-free` 显示连续空闲区从扇区 `247808`（`33792 + 212992`）一直到磁盘最后一个扇区 `67108863`。如果 PVE 上的虚拟磁盘本身还没达到计划容量，先在 PVE 的虚拟机硬件页扩盘，再重新核对这一步的输出。[Proxmox VE 管理指南](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf)

## 2. 备份配置并验证整机归档

### 从管理电脑导出配置

下面的地址是占位符。先换成两台机器的真实管理地址，并确认可以分别通过 SSH 登录。使用 Bash 执行。

```bash
(
  set -euo pipefail
  PVE_HOST=pve.example.net
  OWRT_HOST=openwrt.example.net
  BACKUP_DIR=$(ssh "root@$PVE_HOST" \
    'umask 077; mktemp -d /var/lib/vz/dump/openwrt-before-resize.XXXXXXXX')

  ssh "root@$OWRT_HOST" 'sysupgrade -k -b -' |
    ssh "root@$PVE_HOST" \
      "umask 077; cat > '$BACKUP_DIR/openwrt-config.tar.gz'"

  ssh "root@$OWRT_HOST" \
    'sha256sum /etc/config/network /etc/config/firewall /etc/config/dhcp' |
    ssh "root@$PVE_HOST" \
      "umask 077; cat > '$BACKUP_DIR/guest-config.sha256'"

  ssh "root@$PVE_HOST" \
    "gzip -t '$BACKUP_DIR/openwrt-config.tar.gz' &&
     tar -tzf '$BACKUP_DIR/openwrt-config.tar.gz' |
     grep -E '(^|/)etc/config/(network|firewall|dhcp)$'"

  printf '请记下 PVE 上的备份目录 %s\n' "$BACKUP_DIR"
)
```

`sysupgrade -k -b -` 将配置归档写到标准输出，并记录已安装的软件包清单。后面的 PVE 整机归档保存虚拟磁盘和虚拟机配置，是本次的主要回退方案。两份备份可能包含密码、密钥和凭据，创建时限制访问权限，发布文章时只分享命令和脱敏输出。

### 正常关机，在 PVE 上制作整机备份

先在 OpenWrt 的 SSH 会话执行 `sync; /sbin/poweroff`。SSH 断开后，在 PVE 会话执行下列步骤。把 `BACKUP_DIR` 改成上一节打印的实际路径，并继续使用第一节的 `VMID` 和 `DISK`。

```bash
BACKUP_DIR=/var/lib/vz/dump/openwrt-before-resize.REPLACE_ME

require_vm_stopped() {
  qm status "$VMID" | grep -qx 'status: stopped'
}

(
  set -euo pipefail
  umask 077
  require_vm_stopped
  test -b "$DISK"
  test -s "$BACKUP_DIR/openwrt-config.tar.gz"
  test -s "$BACKUP_DIR/guest-config.sha256"
  df -h "$BACKUP_DIR"

  qm config "$VMID" --current > "$BACKUP_DIR/qm-before.conf"
  sfdisk --dump "$DISK" > "$BACKUP_DIR/partition-before.sfdisk"
  dd if="$DISK" of="$BACKUP_DIR/mbr-before.bin" bs=512 count=1 status=none

  vzdump "$VMID" --mode stop --compress zstd --remove 0 \
    --dumpdir "$BACKUP_DIR"
  require_vm_stopped

  cd "$BACKUP_DIR"
  shopt -s nullglob
  archives=(vzdump-qemu-"$VMID"-*.vma.zst)
  test "${#archives[@]}" -eq 1
  ARCHIVE=${archives[0]}
  chmod 600 "$ARCHIVE"

  zstd -dc -- "$ARCHIVE" | vma verify -
  sha256sum "$ARCHIVE" openwrt-config.tar.gz guest-config.sha256 \
    qm-before.conf partition-before.sfdisk mbr-before.bin > SHA256SUMS
  sha256sum -c SHA256SUMS
  printf '已验证整机归档 %s/%s\n' "$BACKUP_DIR" "$ARCHIVE"
)
```

备份前确认目录所在存储有足够空间。备份日志应明确包含目标磁盘，本例为 `include disk 'scsi0'`，并显示任务完成。归档还要通过 `vma verify` 和 SHA-256 校验。PVE 在离线备份中短暂启动备份所需的 QEMU 进程属于正常行为，写盘前仍须再次确认虚拟机状态为 `stopped`。本例验证了归档完整性，没有执行一次真实恢复。[Proxmox VE 备份与恢复指南](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf)

## 3. 计算新分区大小并进行试写

对于这块 512 字节扇区的 MBR 磁盘，`blockdev --getsz` 输出总扇区数。第二分区的起始扇区保持原值，新大小等于总扇区数减去起始扇区。

```text
磁盘总扇区数   67108864
第二分区起点      33792
第二分区新大小  67075072
第二分区末扇区  67108863
```

下面先把备份的首扇区复制到一个同容量的稀疏文件，只在这个临时文件上试写。输出的预期分区表会在写入设备之后用于逐项核对。

```bash
ROOT_START=33792    # 从自己的 sfdisk --dump 读取
OLD_SECTORS=212992   # 从同一分区的 size 读取
TOTAL_SECTORS=$(blockdev --getsz "$DISK")
NEW_SECTORS=$((TOTAL_SECTORS - ROOT_START))

(
  set -euo pipefail
  require_vm_stopped
  test "$(blockdev --getss "$DISK")" -eq 512
  test "$NEW_SECTORS" -gt "$OLD_SECTORS"
  grep -qx 'label: dos' "$BACKUP_DIR/partition-before.sfdisk"
  (cd "$BACKUP_DIR" && sha256sum -c SHA256SUMS)

  scratch=$(mktemp "$BACKUP_DIR/.partition-trial.XXXXXXXX")
  trap 'rm -f -- "$scratch"' EXIT
  truncate -s "$((TOTAL_SECTORS * 512))" "$scratch"
  dd if="$BACKUP_DIR/mbr-before.bin" of="$scratch" \
    bs=512 count=1 conv=notrunc status=none

  printf 'start=%s, size=%s, type=83\n' "$ROOT_START" "$NEW_SECTORS" |
    sfdisk --lock=yes --wipe never --wipe-partitions never -N 2 "$scratch"
  sfdisk --verify "$scratch"
  sfdisk --dump "$scratch" | sed "s|$scratch|$DISK|g" \
    > "$BACKUP_DIR/partition-planned.sfdisk"

  # MBR 第二个主分区表项位于字节 462 至 477。
  cmp -n 462 "$BACKUP_DIR/mbr-before.bin" "$scratch"
  dd if="$scratch" bs=512 count=1 status=none |
    cmp -i 478 "$BACKUP_DIR/mbr-before.bin" -
  sed -E "/p2[[:space:]]*:/ s/size=[[:space:]]*$OLD_SECTORS,/size=$NEW_SECTORS,/" \
    "$BACKUP_DIR/partition-before.sfdisk" |
    diff -w -u - "$BACKUP_DIR/partition-planned.sfdisk"
  cat "$BACKUP_DIR/partition-planned.sfdisk"
)
```

对照原始表和预期表，本例只有 `p2` 的 `size` 从 `212992` 变成 `67075072`。两个分区的起点、第一分区的大小和启动标记、分区类型及 MBR 磁盘签名均应一致。如果结果有其他变化，就在这一步停下核对。[`sfdisk` 手册](https://man7.org/linux/man-pages/man8/sfdisk.8.html)

## 4. 在 PVE 上离线检查原有 ext4

`kpartx` 可以为虚拟磁盘里的分区创建设备映射。先用 `kpartx -l` 查看映射名称，再核对实际映射的底层设备号、起始扇区和长度。以下函数保留在同一个 PVE Bash 会话中，供后续步骤使用。

```bash
kpartx -l "$DISK"

# 使用 kpartx -l 输出中对应第二分区的名称。
ROOT_NAME=pve-vm--100--disk--0p2
ROOT_MAP=/dev/mapper/$ROOT_NAME
DEVNUM=$(lsblk -dn -o MAJ:MIN "$DISK" | awk '{print $1}')

require_unused_disk() {
  require_vm_stopped &&
    test -n "$DEVNUM" &&
    test -d "/sys/dev/block/$DEVNUM/holders" &&
    test -z "$(ls -A "/sys/dev/block/$DEVNUM/holders")" &&
    test "$(dmsetup info -c --noheadings -o open "$DISK" | awk '{print $1}')" = 0
}

verify_root_mapping() {
  local sectors=$1
  test -b "$ROOT_MAP" &&
    test "$(dmsetup table "$ROOT_NAME" | awk '{$1=$1; print}')" = \
      "0 $sectors linear $DEVNUM $ROOT_START" &&
    test "$(blockdev --getsz "$ROOT_MAP")" -eq "$sectors" &&
    test "$(blkid -p -s TYPE -o value "$ROOT_MAP")" = ext4 &&
    test -z "$(lsblk -nr -o MOUNTPOINTS "$ROOT_MAP")"
}

(
  set -euo pipefail
  require_unused_disk
  trap 'kpartx -d -s "$DISK"' EXIT
  kpartx -a -s -r "$DISK"
  verify_root_mapping "$OLD_SECTORS"
  test "$(blockdev --getro "$ROOT_MAP")" -eq 1
  e2fsck -f -n "$ROOT_MAP"
)
```

`-r` 让分区映射保持只读，`e2fsck -n` 也按只读方式检查。必须确认检查通过、返回码为 0，再继续。如果这里发现文件系统已有问题，先保留备份并排查，避免把旧问题带进扩容步骤。脚本结束后会撤掉临时映射。[`e2fsck` 手册](https://www.man7.org/linux/man-pages/man8/e2fsck.8.html)

## 5. 只扩展第二分区

这是第一次写入实际虚拟磁盘。确认前面的备份、试写和只读检查均已通过，再执行。

```bash
(
  set -euo pipefail
  require_unused_disk
  test "$(pvesm path "$VOLID")" = "$DISK"
  sfdisk --dump "$DISK" | diff -u "$BACKUP_DIR/partition-before.sfdisk" -
  dd if="$DISK" bs=512 count=1 status=none |
    cmp "$BACKUP_DIR/mbr-before.bin" -

  printf 'start=%s, size=%s, type=83\n' "$ROOT_START" "$NEW_SECTORS" |
    sfdisk --lock=yes --wipe never --wipe-partitions never -N 2 "$DISK"
  sfdisk --verify "$DISK"
  sfdisk --dump "$DISK" | diff -u "$BACKUP_DIR/partition-planned.sfdisk" -
  dd if="$DISK" bs=512 count=1 status=none |
    cmp -n 462 "$BACKUP_DIR/mbr-before.bin" -
  dd if="$DISK" bs=512 count=1 status=none |
    cmp -i 478 "$BACKUP_DIR/mbr-before.bin" -
)
```

`-N 2` 指定第二个分区项，两个 `--wipe` 选项用于保留已有签名。务必保留第二分区的起始扇区，现有 ext4 的数据仍在那里。前后两次字节比较确保 MBR 第二个表项以外的内容没有变化。[`sfdisk` 手册](https://man7.org/linux/man-pages/man8/sfdisk.8.html)

实际操作中，PVE 曾报告 `Re-reading the partition table failed.: Invalid argument`。这发生在通知宿主机内核重新读取分区表时。先取回磁盘上的 `sfdisk --dump` 结果，与试写结果比较，并执行 `sfdisk --verify`。如果命令返回非零，下面的校验行可能还没有执行，应单独补做校验。只有盘上表项、MBR 和后续新建的映射都与预期一致时才继续；发现差异就停下，避免重复写盘。

## 6. 扩展 ext4 并复查

重新建立分区映射，让 `resize2fs` 看见已经增大的第二分区。接着检查未挂载的文件系统，执行扩容，然后再次用只读检查确认结果。

```bash
(
  set -euo pipefail
  require_unused_disk
  sfdisk --dump "$DISK" | diff -u "$BACKUP_DIR/partition-planned.sfdisk" -
  trap 'kpartx -d -s "$DISK"' EXIT
  kpartx -a -s "$DISK"
  verify_root_mapping "$NEW_SECTORS"
  test "$(blockdev --getro "$ROOT_MAP")" -eq 0

  e2fsck -f -p "$ROOT_MAP"
  resize2fs "$ROOT_MAP"
  e2fsck -f -n "$ROOT_MAP"
  LC_ALL=C tune2fs -l "$ROOT_MAP" | grep -E '^Block (count|size):'
  sync
)
```

`resize2fs` 省略大小参数时会扩展到当前分区的可用大小。本例扩到 `8384384` 个 4096 字节的块，合计 `34342436864` 字节，与 `67075072 × 512` 一致。`df -h` 统计的是文件系统可用来存放文件的空间，因此显示值还会扣除文件系统元数据等开销。[`resize2fs` 手册](https://man7.org/linux/man-pages/man8/resize2fs.8.html)

### 处理扩容后 inode 7 大小不一致

本例在 `resize2fs` 成功后，首次只读复查报告了这样一条问题。

```text
Inode 7, i_size is 29405184, should be 33648640.  Fix? no
```

inode 7 是 ext4 为扩容相关元数据保留的 inode。只有在确认这就是复查发现的问题，并且虚拟机仍关机、分区仍未挂载时，才使用下面的离线修复步骤。对于其他错误，先按实际输出排查。此时文件系统已经扩大，后续操作是修复和复查。不要把分区直接缩回原来的 104 MiB。[Linux 内核 ext4 文档](https://docs.kernel.org/filesystems/ext4/special_inodes.html)

```bash
(
  set -euo pipefail
  require_unused_disk
  sfdisk --dump "$DISK" | diff -u "$BACKUP_DIR/partition-planned.sfdisk" -
  trap 'kpartx -d -s "$DISK"' EXIT
  kpartx -a -s "$DISK"
  verify_root_mapping "$NEW_SECTORS"

  fsck_rc=0
  e2fsck -f -p "$ROOT_MAP" || fsck_rc=$?
  case "$fsck_rc" in
    0|1) ;;
    *) printf 'e2fsck 返回 %s，停止启动流程\n' "$fsck_rc" >&2; exit "$fsck_rc" ;;
  esac

  e2fsck -f -n "$ROOT_MAP"
  LC_ALL=C tune2fs -l "$ROOT_MAP" | grep -E '^Block (count|size):'
  sync
)
```

`e2fsck -p` 会自动处理它可以安全修复的问题。返回码 `1` 表示发现的错误已修复，所以要处理这个退出码，并再跑一次 `e2fsck -f -n`。本例修复后通过了全部五个检查阶段。复查仍报错时，保持虚拟机关机，检查错误或走整机回退。[`e2fsck` 退出码与选项](https://www.man7.org/linux/man-pages/man8/e2fsck.8.html)

## 7. 启动并验证

扩容完成、只读复查通过后，在 PVE 确认临时映射已撤掉，再启动虚拟机。

```bash
require_unused_disk && qm start "$VMID"
qm status "$VMID"
```

重新 SSH 登录 OpenWrt，检查容量、挂载和启动参数。

```bash
df -h
awk '$5 == "/" || $5 == "/boot"' /proc/self/mountinfo
cat /proc/cmdline
cat /sys/class/block/sda2/start
cat /sys/class/block/sda2/size
```

本例的结果如下。根目录保持以 ext4 读写挂载，起始扇区仍是 `33792`，`PARTUUID` 仍为 `011cbbbd-02`。

```text
Filesystem                Size      Used Available Use% Mounted on
/dev/root                31.6G     47.7M     31.5G   0% /
/dev/sda1                15.7M      5.6M      9.8M  37% /boot
```

在管理电脑上用 PVE 保存的校验值验证配置。下列变量在管理电脑的 Bash 会话中设置，备份目录使用步骤 2 打印的真实路径。

```bash
(
  set -euo pipefail
  PVE_HOST=pve.example.net
  OWRT_HOST=openwrt.example.net
  BACKUP_DIR=/var/lib/vz/dump/openwrt-before-resize.REPLACE_ME

  ssh "root@$PVE_HOST" "cat '$BACKUP_DIR/guest-config.sha256'" |
    ssh "root@$OWRT_HOST" 'sha256sum -c -'
)
```

本例的 network、firewall 和 dhcp 三个文件均返回 `OK`。磁盘验收之后，再按设备职责检查应用。例如 OpenWrt 承担网关时，分别检查默认路由、上游连通性、DNS 和内网设备访问。

## 8. 在什么情况下回退

如果在写分区表之前失败，核对磁盘首扇区和分区表仍与备份一致，并撤掉临时映射。确认没有写盘后，可以按原样启动。写入分区表或扩展 ext4 之后发生异常时，先保持虚拟机关机并确认失败发生在哪一步。此时回退以已验证的 PVE 整机备份为准。

更稳妥的恢复方式是用 PVE 的恢复功能把归档恢复到一个空闲 VMID，保留原虚拟机以便检查。在 PVE 上核对可用空间，使用实际归档文件名和空闲 VMID。示例里的 `300` 需要先确认未被占用。

```bash
ARCHIVE=/实际备份目录/vzdump-qemu-100-实际时间.vma.zst
RECOVERY_VMID=300

qmrestore "$ARCHIVE" "$RECOVERY_VMID" --storage local-lvm --start 0
qm set "$RECOVERY_VMID" --onboot 0
qm config "$RECOVERY_VMID"
```

恢复出的虚拟机可能保留原网卡 MAC 和固定 IP。先在 PVE 将恢复机的网卡断开或接入隔离网桥，通过 PVE 控制台验证启动和配置。正式切换时，先确认原虚拟机已停止，避免两台机器同时占用同一地址。配置归档可用于取回个别配置，完整回到扩容前的系统状态则使用整机归档。[Proxmox VE 恢复指南](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf)

遇到类似的容量问题，依次看 PVE 虚拟磁盘、OpenWrt 分区和 `df -h`。哪一层还显示旧容量，就从那一层开始检查。本例的关键是确认虚拟磁盘已有 32 GiB，再保留分区起点、离线扩展 ext4，最后用文件系统复查和重启后的 `df -h` 验证。
