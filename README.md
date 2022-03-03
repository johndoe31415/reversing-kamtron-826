# Kamtrom "Wireless IP Camera" 826 Reverse Engineering
This is a brief writeup of a lecture I gave on offensive security on which we
dissected a Wireless IP camera.

## Model/Type
It already gets odd with the name of the camera. It was purchased from Amazon
on 2022-02-07 as the "Surveillance Camera WiFi - HD WLAN IP Camera with
350°/100° Swivel, Home and Baby Monitor with Motion Detection, Two-Way Audio,
Night Vision, Supports Remote Alarm and Mobile App Control, Black"
("Überwachungskamera WiFi - HD WLAN IP Kamera mit 350°/100°Schwenkbar,Home und
Baby Monitor mit Bewegungserkennung, Zwei-Wege-Audio, Nachtsicht, unterstützt
Fernalarm und Mobile App Kontrolle,Schwarz") and lists as a brand "CAMNRK".
Lower in the offering, the vendor was listed as "KAMTR0ND".

The buying price of the camera was 23.99€ on amazon.de and the Amazon ASIN was
B09FT7T1T2.

On the actual box I cannot see "CAMNRK" anywhere, but the label "KAMTRON" has
been glued over with black sticker (sic!).

The manufacturer is listed on the package as:

```
ShenZhen Fujikam Industry Development Co., Ltd
6F. West, 1st Building, Innovative Industrial Park,
Nashan Cloud Valley, No. 1183, Liuxian Avenue,
Nashan Distric, ShenZhen, China
```

The product information label on the device states:

```
Name: Wireless IP Camera
Model No: 826
```

The German importer is Like Sun GmbH, Planckstr. 59, 45147 Essen.

## Serial console
The device offers an USART console on three pins that are easily solderable.
The configuration is 115200 8N1 3.3V. The three pins (viewed from the Camera
perspective are):

```
1 GND (square pin)
2 TX (white in the image)
3 RX (yellow in the image)
```

![USART Pinout](https://raw.githubusercontent.com/johndoe31415/reversing-kamtron-826/master/usart.jpg)

## Firmware extraction
The root console is locked by default (protected with password). The bootloader
does not seem to respond to character input (even though U-Boot says that it
can be cancelled):

```
�~0昀���x�昘��x�����mode 3
Version 1.0.6
SPI NOR ID code:0x68 0x40 0x18
SPI jump setting is 3 bytes mode
Boot image offset: 0x10000. size: 0x50000. Booting Image .....


U-Boot 2013.01-svn324 (Aug 21 2019 - 19:48:14)

I2C:   ready
DRAM:  64 MiB
ROM CODE has enable I cache
SPI mode
MMC:   FTSDC021: 0
SF: Got idcodes
00000000: 68 40 18 68    h@.h
use default flash params
SF: Detected default with page size 64 KiB, total 16 MiB
flash is 3byte mode
*** Warning - bad CRC, using default environment

In:    serial
Out:   serial
Err:   serial

-------------------------------
ID: 8136110
AC: 200  HC: 200  P1: 860  P2: 600  P3: 540
C6: 860  DR:1146
J: 286   H1: 286
-------------------------------
Net:   GMAC set RMII mode
reset PHY
eth0
Warning: eth0 MAC addresses don't match:
Address in SROM is         65:6d:3d:31:32:38
Address in environment is  00:42:70:00:30:22

SF: Got idcodes
00000000: 68 40 18 68    h@.h
use default flash params
SF: Detected default with page size 64 KiB, total 16 MiB
flash is 3byte mode
0 [0x10000 0x50000]
1 [0x60000 0x2a0000]
2 [0x300000 0x600000]
3 [0x900000 0x6f0000]
4 [0xff0000 0x10000]
Card did not respond to voltage select!
** Bad device mmc 0 **
sd card not exist
Press xxx to abort autoboot in 3 seconds
Hit any key to stop autoboot:  0 
watchdog start...
SF: Got idcodes
00000000: 68 40 18 68    h@.h
use default flash params
SF: Detected default with page size 64 KiB, total 16 MiB
flash is 3byte mode
## Booting kernel from Legacy Image at 02000000 ...
   Image Name:   gm8135
   Image Type:   ARM Linux Kernel Image (uncompressed)
   Data Size:    1430056 Bytes = 1.4 MiB
   Load Address: 02000000
   Entry Point:  02000040
   Verifying Checksum ... OK
   XIP Kernel Image ... OK
OK
Not define this ID
: mem=64M gmmem=30M console=ttyS0,115200 user_debug=31 init=/squashfs_init root=/dev/mtdblock2 rootfstype=squashfs

Starting kernel ...

Uncompressing Linux... done, booting the kernel.
Booting Linux on physical CPU 0
Linux version 3.3.0 (root@debian) (gcc version 4.4.0 20100318 (experimental) (Buildroot 2012.02) ) #79 PREEMPT Thu Jun 14 09:07:58 CST 2018
CPU: FA6 [66056263] revision 3 (ARMv5TE), cr=0000397f
CPU VIPT aliasing data cache, VIPT aliasing instruction cache
Machine: Grain-Media GM8136 series
Memory policy: ECC disabled, Data cache writeback
Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 16256
Kernel command line: mem=64M gmmem=30M console=ttyS0,115200 user_debug=31 init=/squashfs_init root=/dev/mtdblock2 rootfstype=squashfs
PID hash table entries: 256 (order: -2, 1024 bytes)
Dentry cache hash table entries: 8192 (order: 3, 32768 bytes)
Inode-cache hash table entries: 4096 (order: 2, 16384 bytes)
Memory: 64MB = 64MB total
Memory: 61204k/61204k available, 4332k reserved, 0K highmem
Virtual kernel memory layout:
    vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    fixmap  : 0xfff00000 - 0xfffe0000   ( 896 kB)
    vmalloc : 0x84800000 - 0xff000000   (1960 MB)
    lowmem  : 0x80000000 - 0x84000000   (  64 MB)
    modules : 0x7f000000 - 0x80000000   (  16 MB)
      .text : 0x80008000 - 0x8035c1d4   (3409 kB)
      .init : 0x8035d000 - 0x80375000   (  96 kB)
      .data : 0x80376000 - 0x803918e0   ( 111 kB)
       .bss : 0x80391904 - 0x803a275c   (  68 kB)
NR_IRQS:64
gm_jiffies_init, system HZ: 100, pClk: 100000000 
console [ttyS0] enabled
Calibrating delay loop... 858.52 BogoMIPS (lpj=4292608)
pid_max: default: 32768 minimum: 301
Mount-cache hash table entries: 512
CPU: Testing write buffer coherency: ok
Setting up static identity map for 0x28a288 - 0x28a2d0
devtmpfs: initialized
FMEM: 7680 pages(0x1e00000 bytes) from bank0 are reserved for Frammap. 
FMEM: Logical memory ends up at 0x84000000, init_mm:0x80004000(0x4000), PAGE_OFFSET:0x80000000(0x0), 
FMEM: FA726 Test and Debug Register: 0x0 
FMEM Idle Process Up. 
NET: Registered protocol family 16
PMU: Mapped at 0xfe000000 
IC: GM8135, version: 0x1 
iotable: VA: 0xfe000000, PA: 0x90c00000, Length: 4096 
iotable: VA: 0xfe001000, PA: 0x90700000, Length: 4096 
iotable: VA: 0xfe002000, PA: 0x90800000, Length: 4096 
iotable: VA: 0xfe003000, PA: 0x90900000, Length: 4096 
iotable: VA: 0xfe004000, PA: 0x90d00000, Length: 4096 
iotable: VA: 0xfe005000, PA: 0x96000000, Length: 4096 
bio: create slab <bio-0> at 0
usbcore: registered new interface driver usbfs
usbcore: registered new interface driver hub
usbcore: registered new device driver usb
Switching to clocksource fttmr010:1
NET: Registered protocol family 2
IP route cache hash table entries: 1024 (order: 0, 4096 bytes)
TCP established hash table entries: 2048 (order: 2, 16384 bytes)
TCP bind hash table entries: 2048 (order: 1, 8192 bytes)
TCP: Hash tables configured (established 2048 bind 2048)
TCP reno registered
UDP hash table entries: 256 (order: 0, 4096 bytes)
UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
NET: Registered protocol family 1
RPC: Registered named UNIX socket transport module.
RPC: Registered udp transport module.
RPC: Registered tcp transport module.
RPC: Registered tcp NFSv4.1 backchannel transport module.
Video Timer(timer3) Max 42000ms in 0xfa56ea00 HZ.
ftdmac020 ftdmac020.0: DMA engine driver: irq 1, mapped at 0x84804000
GM CPU frequency driver
CPUFREQ support for gm initialized
squashfs: version 4.0 (2009/01/31) Phillip Lougher
JFFS2 version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
msgmni has been set to 119
io scheduler noop registered
io scheduler deadline registered (default)
gpiochip_add: registered GPIOs 0 to 31 on device: ftgpio010.0
probe ftgpio010.0 OK, at 0x84856000
gpiochip_add: registered GPIOs 32 to 63 on device: ftgpio010.1
probe ftgpio010.1 OK, at 0x84858000
Serial: 8250/16550 driver, 3 ports, IRQ sharing disabled
serial8250: ttyS0 at I/O 0xfe001000 (irq = 21) is a 16550A
serial8250: ttyS1 at I/O 0xfe002000 (irq = 22) is a 16550A
serial8250: ttyS2 at I/O 0xfe003000 (irq = 25) is a 16550A
brd: module loaded
loop: module loaded
Not for SPI-NAND pin mux
SPI020 init
SPI020 uses AHB DMA mode
FTSPI020 enable DMA handshake 0x3
SPI020 gets DMA channel 0
ftspi020 ftspi020.0: Faraday FTSPI020 Controller at 0x92300000(0x8485a000) irq 54.
spi spi0.0: setup: bpw 8 mode 0
CLK div field set 1, clock = 30000000Hz
SPI_FLASH spi0.0: unrecognized JEDEC id 684018
Creating 6 MTD partitions on "nor-flash":
0x000000010000-0x000000060000 : "UBOOT"
0x000000060000-0x000000300000 : "LINUX"
0x000000300000-0x000000900000 : "FS"
0x000000900000-0x000000ff0000 : "USER0"
0x000000ff0000-0x000001000000 : "USER1"
0x000000000000-0x000001000000 : "ALL"
Probe FTSPI020 SPI Controller at 0x92300000 (irq 54)
GMAC version 2.3, queue number tx = 128, rx = 32
ftgmac100-0-mdio: probed
ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
FOTG2XX Controller Initialization
Enter Device A
Drive Vbus because of ID pin shows Device A
fotg210 fotg210.0: FOTG2XX
fotg210 fotg210.0: new USB bus registered, assigned bus number 1
fotg210 fotg210.0: irq 9, io mem 0x93000000
fotg210 fotg210.0: USB 2.0 started, EHCI 1.00
hub 1-0:1.0: USB hub found
hub 1-0:1.0: 1 port detected
i2c /dev entries driver
ftiic010 ftiic010.0: irq 18, mapped at 84860000
GM I2C Driver Version: 1.0.0
sdhci: Secure Digital Host Controller Interface driver
sdhci: Copyright(c) Pierre Ossman
mmc0: SDHCI controller on ftsdc021.0 [ftsdc021.0] using ADMA
sdhci-pltfm: SDHCI platform and OF driver helper
TCP cubic registered
NET: Registered protocol family 17
VFS: Mounted root (squashfs filesystem) readonly on device 31:2.
devtmpfs: mounted
Freeing init memory: 96K
usb 1-1: new high-speed USB device number 2 using fotg210
busybox: /linuxrc: Read-only file system
Mounting root fs rw ...
Mounting other filesystems ...
mount: mounting none on /proc/bus/usb failed: No such file or directory
Setting hostname ...
Bringing up interfaces ...
/bin/sh: run-parts: not found
Mounting user's MTD partion
[1970-01-01 08:00:03 rc.devinit] run /etc/init.d/monitor_cdm_init
[1970-01-01 08:00:03 rc.devinit] run /etc/init.d/dev_init.sh
WDT base virtual address = 84886000
hwclock: can't open '/dev/misc/rtc': No such file or directory
mnvram usage: insmod mnvram.ko [options]
	mnvram_paddr_mode=1 [mnvram_mem_size=] :gm IPC using frammap begin phy mem 
	mnvram_paddr_mode=2 [mnvram_mem_size=] [mnvram_paddr] fh IPC using the designated mem
mnvram ver:1.1.1

mnvram_paddr: 0x1800000, mnvram_paddr_mode: 1, mnvram_mem_size: 64 K
mnvram_check_crc fail for magic match!!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:155
crc fail when check binary buf!!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:402
mnvram_check_crc fail for magic match!!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:155
crc fail when check json buf!!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:415
nvram tv_sec: 0, tv_usec: 0 !!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:433
kernel tv_sec: 42949377, tv_usec: 9575 !!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:434
uptime tv_sec: 4, tv_usec: 76533 !!. /root/device_unchanged/project/src/kernel/module/mnvram/mnvram_new.c:438
mnvram_init OK !!
sbull usage: insmod sbull.ko [options]
     [mode=0]      gm8136/gm8136 mode,using physical memory reserved by gmmem
      mode=1 [hardseet_size=] [nsectors=]    :using kernel memory
      mode=2 paddr=  psize=                  :using physical memory

paddr:01810000,psize:31391744
 sbulla: unknown partition table
Frammap: 496 pages in DDR0 are freed. 
Frammap: DDR0: memory base=0x1810000, memory size=0x1c00000, align_size = 4K. 
Frammap: version 1.1.2, and the system has 1 DDR.
hwclock: can't open '/dev/misc/rtc': No such file or directory
dev_init.sh run /project/apps/app/ipc/data/sh/dev_start.sh
ln: /bin/hostapd: File exists
ln: /bin/hostapd_cli: File exists
ln: /project/platforms/gm8135_v2-linux-armv5/data/ipc_data: File exists
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x20 timeout!
Fail to send dati2c i2c-0: NAK!
a
i2c i2c-0: I2C RX MSG set address timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x20 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x21 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send dati2c i2c-0: NAK!
a
i2c i2c-0: I2C RX MSG set address timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send dati2c i2c-0: NAK!
a
i2c i2c-0: I2C RX MSG set address timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send dati2c i2c-0: NAK!
a
i2c i2c-0: I2C RX MSG set address timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x61 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x6c timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x6d timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x6c timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x6d timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x8c timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x8d timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x88 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x89 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x88 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x89 timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x6c timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x6d timeout!
Fail to receive data
Fail to finish this I2C transaction
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x90 timeout!
Fail to send data
i2c i2c-0: I2C RX data 0x91 timeout!
Fail to receive data
Fail to finish this I2C transaction
LOG uses config_path="/mnt/mtd/gmlib.cfg"
log.ko: Apr 14 2017 09:37:38 (mmap 0x83430000 size 0xc000)

LOG base 0x8373c000 size 4K (start pointer 0x7f01b210)
PAGE_OFFSET(0x80000000) VMALLOC START(0x84800000) HZ(100)
ms: module license 'GM' taints kernel.
Disabling lock debugging due to kernel taint
ms.ko v1.41 Jun 29 2017 12:09:02
em.ko v1.4.1 Apr 14 2017 09:37:30
em_user v1.1 Apr 14 2017 09:37:30
Start OSG job thread 0(osg_callback) with nice -20
Start EM putjob (em_putjob) with nice -20
Start EM thread 0(em_callback) with nice -20
gm2d_module_init
** GM2D VER:2.7 ** gm2d_drv_probe done, vbase 0x8492C000, pbase 0x92200000 0x83577840 (1)

Welcome to use sar_adc_drv VER:2.5
 * module_init_func
 * register_driver
 * driver_probe
 * dev_data_alloc_specific done
 * ADDA paddr=90b00000 vaddr=8493a000 tve paddr=93500000 vaddr=8493c000
 * set_pinmux set as 0xB8 0xFFECF278 OK
 * register_cdev
driver_probe done, io_vadr 0x8492E000, io_padr 0x90A00000 0x8373A9E0
driver_probe done,runmod:0x4,0x0,0x0,0x0,poll_mode=0
fe_common version 140714
platform_init
ADDA308 current use MCLK=24571428
adda308_init_one [0] version 150324
FT3DNR200 Version 2017_0703_1600
request IRQ42 with ft3dnr_interrupt() ok!
FT3DNR sp.0 buf size 0x3000 width 1280 height 720 phy addr 0x1828000
FT3DNR mot.0 buf size 0x210 width 1280 height 720 phy addr 0x182b000
FT3DNR mot.1 buf size 0x210 width 640 height 368 phy addr 0x182c000
FT3DNR var.0 buf size 0x108 width 1280 height 720 phy addr 0x182d000
FT3DNR var.1 buf size 0x60 width 640 height 368 phy addr 0x182e000
FT3DNR ref.0 buf size 0x1c2000 width 1280 height 720 phy addr 0x182f000
FT3DNR ref.1 buf size 0x73000 width 640 height 368 phy addr 0x19f1000
ft3dnr200: using tasklet for vg jobs processing!
ISP328 v1.66, built @ Nov 11 2016 17:21:38
USE_DMA_CMD: TRUE
ISP Alogrithm v2.10
Register [0][GM_AE]
Register [1][GM_AWB]
Register [2][GM_AF]
EXT_CLK output ==> 27000000Hz
CAP driving capacity = 48
[VCAP_INFO]: VCAP300 Version: 0.3.13
[ISP_INFO]: Sensor Interface : PARALLEL
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
sensor_i2c_transfer fail: i2c_transfer not OK 
[ISP_ERR]: failed to initial soih42!
[ISP_ERR]: [ISP] failed to initial soih42
[ISP_INFO]: Found [GM_AE]
[ISP_INFO]: Found [GM_AWB]
[ISP_INFO]: Found [GM_AF]
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
sensor_i2c_transfer fail: i2c_transfer not OK 
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
sensor_i2c_transfer fail: i2c_transfer not OK 
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
sensor_i2c_transfer fail: i2c_transfer not OK 
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0x60 timeout!
sensor_i2c_transfer fail: i2c_transfer not OK 
[ISP_WARN]: [AWB_M2] $grey_cx_boundary$ is not found!!
[VCAP_INFO]: Register ISP Input Device
MCP100 GM8136, built @ Sep 21 2016 10:48:40
FAVC Encoder v2.0.3.1, built @ Sep 27 2016 13:59:14 (GM8136)
H264 rate control(VG) version: 1.1.13, built @ Feb 14 2017 13:46:58
GM8136 MJPEG, encoder v4.2.0, decoder v4.0.9, built @ Aug 26 2016 14:20:35
osg canvas is dynammic allocate mode
SWOSG ver 0.0.2
SCALER version 141119, temp_width: 0, temp_height: 0 
fscaler300_init_one [0] NCNB
audio_init: audio driver is inserted, minor version: 0224_1619
Record(SSP:0): stream->dma_buffer = 8dc000(ffde8000), size:800, dma_ch: 1 
Playback(SSP:0): stream->dma_buffer = 8c8000(ffde0000), size:800, dma_ch: 2
gs.ko v1.6b Apr 14 2017 09:37:05
GS driver, log: level(0) category(0) bmp width(64)
videograph ioctl v1.4
vpd.ko v1.5.1 Jul 12 2017 14:20:19
VPD uses config_path="/mnt/mtd/gmlib.cfg"
vplib v3.1 Jul 12 2017 14:20:21
config_init v1.1 Jul 12 2017 14:20:27 /mnt/mtd/gmlib.cfg
bufferSea_ddr0     7927 KB + 0 KB(reserved)
-----------------------------------------------------------------------
enc_cap_out_ddr0 DDR0(4528KB)
                  DDR0 pool free size 3399KB.
enc_scl_out_ddr0 DDR0(1802KB)
                  DDR0 pool free size 1597KB.
enc_out_ddr0 DDR0(1537KB)
                  DDR0 pool free size 60KB.
au_encode_ddr0 DDR0(30KB)
                  DDR0 pool free size 30KB.
au_playback_ddr0 DDR0(30KB)
                  DDR0 pool free size 0KB.
datain v1.2 (minors 2 : 0x2 + 2) Jul 12 2017 14:20:32
dataout v1.2 (minors 5 : 2x2 + 1) Jul 12 2017 14:20:31
osd_mg_database_init......osd_type:0
osd_mg_database_init......osd_type:1
osd_mg_database_init......osd_type:2
usr_decode v1.1 Jul 12 2017 14:20:35
usr_snapshot v1.1.2b Jul 12 2017 14:20:34 (640x360, 256KB)
usr_cap_source v1.1 Jul 12 2017 14:20:36
usr_process v0.1 Jul 12 2017 14:20:33
usr_osg v1.9 Jul 12 2017 14:20:38
usr_osg: (ch_table) 4 ,-1 ,

Frammap: 3866 pages in DDR0 are freed. 
Set EM debug level(0) (0:quiet 1:get/put 2:property 3:semaphore)
Set GS debug level 0: all flow disable.
Set MemoryService debug level(0).
Set datain debug level(0)
Set dataout debug level(0)
Set VPD debug level(0).
Debug Level:0
HW reset
RTL871X: module init start
RTL871X: rtl8188fu v4.3.23.4.2_19108.20160818_pDeinit
RTL871X: build time: Oct 27 2020 17:42:53
RTL871X: hal_com_config_channel_plan chplan:0x41
RTL871X: rtw_ndev_init(ra0) if1 mac_addr=b4:ad:a3:76:73:07
usbcore: registered new interface driver rtl8188fu
RTL871X: module init ret=0
phy speed is 10, half duplex
HW reset
WDT base virtual address = 853d8000

Welcome to 1jfiegbrmeg3q@28450@m@u (armv5tel-Linux-3.3.0@/dev/ttyS0/b)
Grain Media ARM Linux 3.3

Released under GNU GPL

1jfiegbrmeg3q@28450@m@u login: i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
13 May 10:23:40 ntpdate[2011]: no servers can be used, exiting
RTL871X: set bssid:00:00:00:00:00:00
RTL871X: set ssid [g�isQ�J�)ͺ����F|�T��vZ.c3�ɚ8��P`*���] fw_state=0x00000008
RTL871X: indicate disassoc
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
i2c i2c-0: NAK!
i2c i2c-0: I2C TX data 0xb4 timeout!
RTL871X: indicate disassoc

## Apply Au_Grab_1 1 (0ms) ##
audio info: change rec sample rate to 16000
audio info: change rec channel type to mono

## Apply Au_Render_2 1 (0ms) ##
initial mute_samples = 4096
sample_size = 16
, ratio = 10000
, adjusted mute_samples = 8192



Welcome to 1jfiegbrmeg3q@28450@m@u (armv5tel-Linux-3.3.0@/dev/ttyS0/b)
Grain Media ARM Linux 3.3

Released under GNU GPL

1jfiegbrmeg3q@28450@m@u login: 
```

Note that the I2C error messages are likely because it is trying to either
communicate with the camera or motor assembly and those periperals have been
disconnected.

The CPU seems to be a Grain GM8135.

## Firmware extraction
We therefore tried to extract the firmware. It's stored on a BY25Q128 chip (128
MBit flash memory, 16 MiB). To easily be able to re-flash new firmwares we
decided to build a makeshift socket for the chip:


![Makeshift socket](https://raw.githubusercontent.com/johndoe31415/reversing-kamtron-826/master/makeshift_socket.jpg)


## Image disassembly
As also visible from the bootloader, there are five partitions:

```
0 [0x10000 0x50000]			U-Boot
1 [0x60000 0x2a0000]		Linux Kernel
2 [0x300000 0x600000]		Root FS (SquashFS)
3 [0x900000 0x6f0000]		User0 (JFFS2)
4 [0xff0000 0x10000]		User1 (raw config data)
```

The script `decompose_firmware` decomposes a firmware binary into its compoents.

Then you can call `edit_firmware` which will unsquashfs/mount the rootfs/JFFS
and recompile it back together to a firmware image.

## Telnet
By writing the file `flag_debug_telnet` inside the root of the JFFS2
(`/dev/mtdblock2`), you can activate a telnet server on port 9527.

## Root password
The root password is randomly set on each boot and seems to depend on several factors:

1. The device ID ("1jfiegbrmeg3q")
2. Some random "context" value, seems to be a small integer that is displayed
   on the login prompt: "28450"
3. Some internal secret values, not sure if they're shared across a family of
   devices, called the "pass.up" with value "1vOsNdbzrDXW86w11vOsNQ" and the
   "pass.mp" with value "d4BwZ8nVU2mgfHDeOJhyjQ". Possibly "user password" and
   "master password"?

When copying the whole root FS and JFFS into a environment and symlinking
busybox to /bin/sh, you can simply chroot into that image on a Raspberry Pi.
Then, in the login prompt, you will see the device ID and randomized context
value:


```
sniffpi [~]: telnet 192.168.42.108 9527
Trying 192.168.42.108...
Connected to 192.168.42.108.
Escape character is '^]'.

1jfiegbrmeg3q@4598@m@u@e.192.168.42.108 login: 

```

As you can see, my device ID is `1jfiegbrmeg3q` and the context ID is `4598`.
Then, in the Raspberry Pi chroot image, simply do:

```
sniffpi [/fs_1/project/apps/app/ipc/data/sh]: ../../../../../platforms/gm8135_v2-linux-armv5/bin/mipc_tool -cmd pass -devid 1jfiegbrmeg3q -prompt /tmp/prompt.debug -pass /tmp/pass.debug -ctx 4598 -mp d4BwZ8nVU2mgfHDeOJhyjQ -up MEJLfM11UhRkaCvcFt1GyQ && cat /tmp/pass.debug 
7eb2534df0f0d5af7481e485bf76ade4
```

This hash value, `7eb253...` is the current root password:

```
1jfiegbrmeg3q@4598@m@u@e.192.168.42.108 login: root
Password: 
login: can't chdir to home directory '/root'

|---------------------------------------------------------------------------|
| Welcome to                                                                |
|                                                                           |
|                    A                                                      |   
|                   AAA                                                     |   
|                  AAAAA                                                    |   
|                 AAAAAAA                                                   |   
|                AAAA   AA                                                  |   
|         A     AAAA     AA                                                 |   
|        AAA   AAAA       AA          AAA   AAAAA    AAA   AAAAA    AAAAA   |   
|       AAAAA AAAA         AA              AA   AA        AA   AA  AA   AA  |
|      AAAAAAAAAA           AA        AAA  AA   AA   AAA  AA   AA  AA   AA  |
|     AAAAA AAAA             AA       AAA  AA   AA   AAA  AA   AA  AA   AA  |
|    AAAAA    A               AA      AAA  AA   AA   AAA  AA   AA   AAAAAA  |
|   AAAAA                      AA     AAA  AA   AA   AAA  AA   AA       AA  |
| AAAAAA                        AAAA  AAA  AA   AA   AAA  AA   AA  AAAAAA   |   
|===========================================================================|
|                                                                           |   
|                                             http://www.shenzhenmining.com |
|                                           power by (C)shenzhenmining 2015 |
|---------------------------------------------------------------------------|


Mar  3 20:28:01 login[2202]: root login on 'ttyS0'


BusyBox v1.20.1 (2015-03-29 21:56:34 HKT) built-in shell (ash)
Enter 'help' for a list of built-in commands.

[root@1jfiegbrmeg3q@4598@m@u@e.192.168.42.108]# 
```

I've also tried overwriting the `dev_passwd.sh` script to always set "admin" as
the root password, but for some reason that I don't understand (yet), this
script is subsequently restored -- possibly from the .tar.lzma blob in the
rootfs directory.

![First successful shell](https://raw.githubusercontent.com/johndoe31415/reversing-kamtron-826/master/first_shell.jpg)

## Re-flashing a new image
When you've modified an image, you can re-flash it. Note that the MiniPro
TL866CS which I'm using cannot write using the BY25Q128, but using a Winbond W25Q128 with the `-y` option works:

```
$ minipro -p "W25Q128FV@SOIC8" -w new_firmware.bin -y --skip_verify
Found TL866CS 03.2.86 (0x256)
WARNING: Chip ID mismatch: expected 0xEF4018, got 0x684018 (BY25Q128AS)
Erasing... 47.03Sec OK
Protect off...OK
Writing Code...  247.74Sec  OK
Protect on...OK
```

## Further work
  * It would be interesting to dissect the `mipc_tool` binary to see exactly
    how it performs key derivation of the root password.
  * It would be interesting to see if the videostream is properly encrypted --
    preliminary data makes it seem like this is maybe not the case.
