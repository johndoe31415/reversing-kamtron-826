#!/usr/bin/python3

parts = [
	("0_header.bin", 0, 0x10000),
	("1_uboot.bin", 0x10000, 0x50000),
	("2_kernel.bin", 0x60000, 0x2a0000),
	("3_rootfs.bin", 0x300000, 0x600000),
	("4_jffs2.bin", 0x900000, 0x6f0000),
	("5_config.bin", 0xff0000, 0x10000),
]
