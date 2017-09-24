#!/usr/bin/python
import os, sys, time, subprocess, re, webbrowser

if len(sys.argv) != 2:
    print "[*]Usage: ./webmap.py protocol://hostname[:port]/[path/]"
    exit(0)

elif len(sys.argv) == 2:
     url = sys.argv[1]
     if (":" and "/") in url:
         i = url.split("/")[2]
         ip = i.split(':')[0]
     else:
         ip = i

bflist=['/usr/share/wordlists/SecLists/Discovery/Web_Content/big.txt', '/usr/share/wordlists/SecLists/Discovery/Web_Content/Logins.fuzz.txt']

def gob(url):
    print "\n\t[!] Running gobuster on target."
    params = " -e -f -s '307,200,204,301,302' -t 20 -u " + url + " >> /tmp/%s/gobuster.txt" % (ip)
    for i in bflist:
            dirbf = "gobuster -w " + i + params
            print "Syntax: " + dirbf
            os.system(dirbf)

    review()
    
def nikto(url):
    print "\n\t[!] Running nikto on target."
    port2 = ip[1]
    if port2:
        nk = "nikto -h " + url + " -evasion 1 -port " + port2 + " -Tuning x 8 --no404 | tee /tmp/%s/nikto" % (ip)
    else:
        nk = "nikto -h " + url + " -evasion 1 -Tuning x 6 --no404 | tee /tmp/%s/nikto" % (ip) 
    print "Syntax: " + nk
    nks = os.system(nk)

def review():
    print "\n\t[*] Opening tangible resources in the default web browser..."
    hits = []
    inf = "/tmp/%s/gobuster.txt" % (ip)
    f = open(inf,'r')
    for l in f:
        if re.search('http.',l):
            if "[+]" in l:
                pass
            else:
                x = l.split(' ')[0]
                hits.append(x)
    for i in hits:
        if i in hits:
            hits.remove(i)

    for url in hits:
        str(url)
        webbrowser.open(url, new=1, autoraise=False)
        time.sleep(1)

    nikto(url)

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
 #   review()
