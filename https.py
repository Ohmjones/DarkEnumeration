#!/usr/bin/python
import sys, os, subprocess, re, time
if len(sys.argv) != 2:
    print "Usage: ./https.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
url =  "https://" + ip_address

wordlists = ["/usr/share/dirb/wordlists/big.txt", "/usr/share/dirb/wordlists/vulns/cgis.txt"]
wfuzzlist = ["/usr/share/wfuzz/wordlist/general/big.txt", "/usr/share/wfuzz/wordlist/vulns/cgis.txt"]

def gobuster(url):
	print "[!] Starting gobuster scan for " + url
	if ("big" in wordlists[0]):
		time.sleep(15)
		gobuster = "gobuster -u " + url + " -w " +  str(wordlists[0]) + " -s '200,204,301,302,307,403,500'"
		os.system("gnome-terminal -e 'bash -c \"" + gobuster + "\";bash'")
		if ("cgis" in wordlists[1]):
			time.sleep(30)
			gobuster = "gobuster -u " + url + " -w " +  str(wordlists[1]) + " -s '200,204,301,302,307,403,500'"
			os.system("gnome-terminal -e 'bash -c \"" + gobuster + "\";bash'")
			
	time.sleep(300) # Let's give Gobuster 5 minutes to complete or near completion before we hammer port 443 some more.
	wfuzz(url)
	
def wfuzz(url):
	print "[!] Starting wfuzz scan for " + url
	if ("big" in wfuzzlist[0]):
		time.sleep(15)
		wfuzz = "wfuzz --hc 404,403 -c -z file," + str(wfuzzlist[0]) + " " + url + "/FUZZ"
		os.system("gnome-terminal -e 'bash -c \"" + wfuzz + "\";bash'")
		if ("cgis" in wfuzzlist[1]):
			time.sleep(30)
			wfuzz = "wfuzz --hc 404,403 -c -z file," + str(wfuzzlist[1]) + " " + url + "/FUZZ"
			os.system("gnome-terminal -e 'bash -c \"" + wfuzz + "\";bash'")
		
def nikto(url):
	cmd = "nikto -h " + url
	os.system("gnome-terminal -e 'bash -c \"" + cmd + "\";bash'")
	time.sleep(300) # Let's give Nikto 5 minutes to complete or near completion before we hammer port 443 some more.
	gobuster(url)

def main():
	nikto(url)

if __name__=='__main__':
	main()
