#!/usr/bin/python
import sys, os, subprocess, re, time

if len(sys.argv) != 2:
    print "Usage: ./snmp.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
community = ["public", "private", "manager"]

def walk(ip_address):
	print "[*] Grabbing SNMP data from " + ip_address
	snmpwalk = "snmpwalk -c public -v1 %s > /tmp/%s/snmpwalk" % (ip_address, ip_address)
	callsnmpwalk = subprocess.Popen(snmpwalk, stdout=subprocess.PIPE, shell=True)
	callsnmpwalk.wait()

def onesixtyone(ip_address):
	print "[*] Grabbing more SNMP data from " + ip_address
	for string in community:
		if ("public" in string):
			rgr = "onesixtyone -c public %s > /tmp/%s/onesixtyone_public" % (ip_address, ip_address)
			subprocess.call(rgr, shell=True)
		elif ("private" in string):
			rgr = "onesixtyone -c private %s > /tmp/%s/onesixtyone_private" % (ip_address, ip_address)
			subprocess.call(rgr, shell=True)
		elif ("manager" in string):
			rgr = "onesixtyone -c manager %s > /tmp/%s/onesixtyone_manager" % (ip_address, ip_address)
			subprocess.call(rgr, shell=True)
def main():
	walk(ip_address)
	onesixtyone(ip_address)

if __name__=='__main__':
	main()
