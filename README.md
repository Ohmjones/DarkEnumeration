Dark Enumeration

This is my collection of scripts that I use to tackle most vulnerable VM's and the OSCP examination systems, including PWK labs.

This is a work in progress, as I always find something cooler than what I was doing on the last system.

For those who code:
  I have intentionally left this set of scripts to run interdependant of eachother. I keep getting caught up on what I want it to automate, so I figure that's best left for you to make a "glue-script" that will run things as you see fit.
  
For those who don't:
  These set of scripts are meant to be run in any order, however - on a 'blackbox' target it should be something like this.
    ./darkenum.py target
    review results
    ./webmap.py http://target:10000 
    review results
    ./smbfun.py target
    review results
    so forth...
    so on...
