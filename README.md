DarkEnumeration
Automated enumeration

This set of scripts were written in the hopes to alleviate manual enumeration processes the logic of the script is as follows:
  1. Do not actually exploit or automatically obtain footholds on a system
  2. Test all 65,535 ports utilizing Unicornscan
  3. Once Unicornscan completes, take those ports and run a far more intrusive nmap scan on each service/port (standard implementations, only).
  4. Once Unicornscan completes, multi-process the nmap scan so they can be done simultaneously.
  5. Once Unicornscan completes, launch each standalone python script against each standard service/port found.
  6. Each new script/tool that is launched, does so in a new terminal to keep things clean - not all windows will remain open (i.e. those with output flags/redirection).
  7. Thoroughly investigate all output and any errors, bugs or otherwise should be manually investigated by you.
  
#Please do not use this script in any publications (blogs, tutorials, etc...) without giving credit to myself; this script will be useful to many and I'm very proud of my work - thanks. 
(In addition, if you modify/update or otherwise fix these scripts please send any suggested fixes or tweaks that you've made to it, to me, so that it can be reflected in this repository so others can benefit.)

# Try-Harder! and use Google to ask for help - cause Offensive Security won't help you and I may not have the time to help, either.


#Installation for certain scripts to work:
1. All scripts MUST be in /root/Scripts/
2. Go to http://itsecurity.net/ and download http://itsecurity.net/debian_ssh_scan_v4.tar.bz2
3. Unzip debian_ssh_scan_v4.tar.bz2 into /root/Scripts/debian_ssh_scan_v4
4. have fun
