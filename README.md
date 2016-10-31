DarkEnumeration
Automated enumeration
<br>
This set of scripts were written in the hopes to alleviate manual enumeration processes. 
The logic of the script is as follows:
  1. Do not actually exploit or automatically obtain footholds to a system.
  2. Test all 65,535 ports utilizing Unicornscan (currently doesn't support threading, waiting for Unicornscan to follow nmap's footsteps in that regard)
  3. Once Unicornscan completes:
      - Take those ports and run a far more intrusive nmap scan on each service/port (standard implementations, only).
      - Multi-process the nmap scan so they can be done simultaneously.
      - launch each standalone python script against each standard service/port found.
  4. Each new script/tool that is launched, does so in a new terminal to keep things clean - not all windows will remain open (i.e. those with output flags/redirection that do not break the script).
  5. Thoroughly investigate all output and any errors, bugs or otherwise should be manually investigated by you.
<br>
Please do not use this script in any publications (blogs, tutorials, etc...) without giving credit to myself; this script will be useful to many and I'm very proud of my work - thanks. (In addition, if you modify/update or otherwise fix these scripts please send any suggested fixes or tweaks that you've made to it, to me, so that it can be reflected in this repository so others can benefit.)

#Installation for certain scripts to work:
1. All scripts MUST be in /root/Scripts/
2. Go to http://itsecurity.net/ and download http://itsecurity.net/debian_ssh_scan_v4.tar.bz2
3. Unzip debian_ssh_scan_v4.tar.bz2 into /root/Scripts/debian_ssh_scan_v4 (/root/Scripts/debian_ssh_scan_v4/debian_ssh_scan_v4.py target should execute the script)
4. have fun


Understanding usage:<br>
  ./darkenum.py 192.168.1.1
#WARNING: This script is pretty hefty, I do NOT recommend running it on anymore than 4 systems at any one time.
