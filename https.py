#!/usr/bin/python
import sys, os, subprocess, re, time
if len(sys.argv) != 2:
    print "Usage: ./http.py <targetip>"
    sys.exit(0)

ip_address = str(sys.argv[1])
url =  "https://" + ip_address

wordlists = ["/usr/share/dirb/wordlists/big.txt", "/usr/share/dirb/wordlists/vulns/cgis.txt"]
wfuzzlist = ["/usr/share/wfuzz/wordlist/general/big.txt", "/usr/share/wfuzz/wordlist/vulns/cgis.txt"]

def gobuster(url):
	if ("big" in wordlists[0]):
		print "[!] Starting gobuster big scan for " + url
		gobuster = "gobuster -u " + url + " -w " +  str(wordlists[0]) + " -s '200,204,301,302,307,403,400'"
		callbigscan = subprocess.Popen(gobuster, stdout=subprocess.PIPE, shell=True)
		callbigscan.wait()
		for line in callbigscan.stdout:
			print line.strip()
		print '\n'
		if ("cgis" in wordlists[1]):
			print "[!] Starting gobuster cgi scan for " + url
			gobuster = "gobuster -u " + url + " -w " +  str(wordlists[1]) + " -s '200,204,301,302,307,400,403'"
			callcgiscan = subprocess.Popen(gobuster, stdout=subprocess.PIPE, shell=True)
			callcgiscan.wait()
			for line in callcgiscan.stdout:
				print line.strip()
			print '\n'
	wfuzz(url)
	
def wfuzz(url):
	if ("big" in wfuzzlist[0]):
		print "[!] Starting wfuzz big scan for " + url
		wfuzz = "wfuzz --hc 404,403,400 -c -z file," + str(wfuzzlist[0]) + " " + url + "/FUZZ"
		callwfuzzbigscan = subprocess.Popen(wfuzz, stdout=subprocess.PIPE, shell=True)
		callwfuzzbigscan.wait()
		for line in callwfuzzbigscan.stdout:
			print line.strip()
		print '\n'
		if ("cgis" in wfuzzlist[1]):
			print "[!] Starting wfuzz cgi scan for " + url
			wfuzz = "wfuzz --hc 404,403,400 -c -z file," + str(wfuzzlist[1]) + " " + url + "/FUZZ"
			callwfuzzcgiscan = subprocess.Popen(wfuzz, stdout=subprocess.PIPE, shell=True)
			callwfuzzcgiscan.wait()
			for line in callwfuzzcgiscan.stdout:
				print line.strip()
			print '\n'
	nse(url)

def nse(url):
	fileuploader = "nmap -p443 --script http-fileupload-exploiter.nse " + ip_address
	callfuscan = subprocess.Popen(fileuploader, stdout=subprocess.PIPE, shell=True)
	callfuscan.wait()	
	for line in callfuscan.stdout:
		print line.strip()
	time.sleep(60)
	nikto(url)
		
def nikto(url):
	cmd = "nikto -h " + url
	os.system("gnome-terminal -e 'bash -c \"" + cmd + "\";bash'")

def main():
	gobuster(url)

if __name__=='__main__':
	main()
