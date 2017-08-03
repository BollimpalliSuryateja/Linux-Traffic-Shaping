#! /usr/bin/python

# this python script automatically detect new interfaces in the host system

import os, subprocess

cmd = subprocess_checkoutput("ls /system/class/net/", shell=True)
interfaces = []
interfaces = cmd.splitlines()
