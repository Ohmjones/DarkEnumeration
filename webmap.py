#!/usr/bin/python
import os, sys, subprocess

if len(sys.argv) != 2:
    print "\t[*]Usage: ./webmap.py https://url"
    print "              OR                  "
    print "\t[!]Usage: ./webmap.py http://url:10000"
    exit(0)
elif len(sys.argv) == 2:
     url = sys.argv[1]
     if ":" in url:
         i = url.split("/")[2]
         ip = i.split(':')[0]
     else:
         ip = i

bflist=['/usr/share/wordlists/SecLists/Discovery/Web_Content/common.txt','/usr/share/wordlists/SecLists/Discovery/Web_Content/big.txt', '/usr/share/wordlists/SecLists/Discovery/Web_Content/Logins.fuzz.txt']

def gob(url):
    print "\n[!] Running gobuster on target."
    params = " -e -f -s '307,200,204,301,302' -t 15 -u " + url + " >> /tmp/%s/gobuster.txt" % (ip)
    for i in bflist:
            dirbf = "gobuster -w " + i + params
            print "Syntax: " + dirbf
            scan = os.system(dirbf)

    nikto(url)

def nikto(url):
    print "\n[!] Running nikto on target."
    nk = "nikto -h " + url + " | tee /tmp/%s/nikto.txt" % (ip)
    print "Syntax: " + nk
    nks = os.system(nk)

if __name__=='__main__':
    path = os.path.join("/tmp", ip.strip())
    try:
            print "[!] Checking Results Directory."
            os.mkdir(path)
            print "\t[!] Directory created. Results can be located in: " + path
    except:
            print "\t[!] Directory " + path + " exists."
            pass

    gob(url)
