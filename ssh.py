#!/usr/bin/python

import sys, os, subprocess, re, time

if len(sys.argv) != 2:
    print "Usage: ssh.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
vulnssh = "/root/Scripts/debian_ssh_scan_v4/debian_ssh_scan_v4.py"

def keys(ip_address):
	print "moving into ./debian_ssh_scan_v4 to run script!"
	sshvuln = vulnssh + " " + ip_address
	subprocess.call(sshvuln, shell=True)

def main():
	keys(ip_address)

if __name__=='__main__':
	main()
