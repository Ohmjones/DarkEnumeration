#!/usr/bin/python

import sys, os, subprocess, re, time, socket

if len(sys.argv) != 2:
    print "Usage: ./smtp.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
wl = open('/root/Scripts/offsecusers', 'r')

so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=so.connect((ip_address,25))

print "[*] Giving 5 seconds for server to fully establish the connection...."
time.sleep(5)

#grab banner if there is one
banner=so.recv(1024)
print "[*] " + sys.argv[1] + "  [*]  " + banner

#initiate with HELO
try:		
	so.send('HELO test@thinc.local \r\n')
	HELO = so.recv(1024)
	if (("500" in HELO)):
		so.send('EHLO test@thinc.local \r\n')
		EHLO = so.recv(1024)
		print EHLO
except:
	print HELO

for name in wl:	
	try:
		so.send('VRFY ' + name.strip() + '\r\n')
		result = so.recv(1024)
		if (("250" in result)):
			print "[*] Verified " + result
		elif (("550" in result) or ("user unknown" in result)):
			print result	
		elif (("252" in result)):
			print "[*] Server cannot confirm or deny that " + name + " is valid."
		elif (("251" in result)):
			print "[*] Server suggests " + name + " is forwarded."
#Filter Results
	except:
		pass	

so.close()
print "[*] Script has successfully completed for " + sys.argv[1]
