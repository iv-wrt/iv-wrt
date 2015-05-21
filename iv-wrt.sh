#!/bin/bash

#if no image file is passed, choose iv-wrt.elf
if [ "$#" = 0 ]; then
        image='image.elf'
else
	image=$1
fi

#start qemu
qemu-system-mipsel -kernel $image -nographic -m 512 -net tap,ifname=tap0,script=no,downscript=no -net nic,model=e1000 -net tap,ifname=tap1,script=no,downscript=no -net nic,model=e1000