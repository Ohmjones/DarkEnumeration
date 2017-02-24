DarkEnumeration
<br>
Automated enumeration
<br>
This set of scripts is currently being re-worked. Here's the goals:
<br>
1. Start off utilizing unicornscan to quickly perform a full port scan on TCP/UDP services. (This averages ~2.5 minutes for TCP & UDP each)
2. Intrusively scan the asset on the found/given ports via nmap
3. Take the output from nmap and parse that data for sexy datahs.
4. Kick off various other checks through the use of extra scripts that will be added over time.

This is a fairly straight-forward set of scripting. Feel free to do what you will with the code, but at least make an attempt to credit me if you do anything significant to the code.
