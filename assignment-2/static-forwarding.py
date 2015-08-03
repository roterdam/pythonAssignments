#!/usr/bin/python

" Assignment 2 - static-forwarding.py - \
    First part of the assignment. This is to create a static-forwarding table."


from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from helpers import *


class StaticSwitch(Policy):
    def __init__(self):
        """ 
        Initialization of static switch. Set up your forwarding tables  here.
        You need to key off of Switch and MAC address to determine forwarding
        port.
        Suggested routes: 
          - Array with switch as index, dictionary for MAC to switch port
          - dictionary of dictionaries
        """

        # Initialize the parent class
        super(StaticSwitch, self).__init__()

        # TODO: set up forwarding tables. Create this however you wish. As
        # a suggestion, using a list of tuples will work.

        self.forwardTable = [(1,"00:00:00:00:00:02",2),(1,"00:00:00:00:00:01",1),(1,"00:00:00:00:00:04",3),(1,"00:00:00:00:00:03",3),(2,"00:00:00:00:00:03",1),(2,"00:00:00:00:00:04",2),(2,"00:00:00:00:00:01",3),(2,"00:00:00:00:00:02",3)]
		


    def build_policy(self):
        """ 
        This creates the pyretic policy. You'll need to base this on how you 
        created your forwarding tables. You need to compose the policies 
        in parallel. 
        """

        # TODO: Rework below based on how you created your forwarding tables.
        
        subpolicies = []
        open_log("static-forwarding.log")
	for rule in (self.forwardTable):
            subpolicies.append (match(switch=int(rule[0]), dstmac=(rule[1])) >> fwd(rule[2]))
	    write_forwarding_entry(int(rule[0]), int(rule[2]), rule[1])
	    #next_entry()
        finish_log()

        # NOTE: this will flood for MAC broadcasts (to ff:ff:ff:ff:ff:ff).
        # You will need to include something like this in order for ARPs to 
        # propogate. xfwd() is like fwd(), but will not forward out a port a 
        # packet came in on. Useful in this case.
        subpolicies.append(match(switch=1, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)]))
        subpolicies.append(match(switch=2, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)]))

        # This returns a parallel composition of all the subpolicies you put
        # together above.
        return parallel(subpolicies)
            
        
        
        
def main():
    return StaticSwitch().build_policy()
