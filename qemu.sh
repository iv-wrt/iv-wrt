#!/bin/bash
qemu-system-mipsel -kernel $1 -nographic -m 256 -net tap,ifname=tap0,script=no,downscript=no -net nic,model=e1000
