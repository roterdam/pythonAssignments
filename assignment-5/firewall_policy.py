#!/usr/bin/python

"Assignment 5 - This creates the firewall policy. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets

def make_firewall_policy(config):
    # TODO - This is where you need to write the functionality to create the
    # firewall. What is passed in is a list of rules that you must implement
    # using the Pyretic syntax that was used in Assignment 2. 

    # feel free to remove the following "print config" line once you no longer need it
    # print config # for demonstration purposes only, so you can see the format of the config

    rules = []
    for entry in config:
        # TODO - build the individual rules

        # examples: 
        # rule = match(dstport=entry['dstport'])
        # rule = match(srcmac=MAC(entry['srcmac']))
        #rule = match(srcip=entry['srcip'])
	#rule = match(srcip=entry['dstip'])
        # rule = match(dstmac=MAC(entry['dstmac']), srcport=entry['srcport'])


	matches = match(protocol=6)
	matches = matches & match(ethtype=0x0800)

	if entry['dstport'] != '*':
		matches = matches & match(dstport=int(entry['dstport']))

	if entry['srcport'] != '*':
		matches = matches & match(srcport=int(entry['srcport']))

	if entry['srcip'] != '*':
		matches = matches & match(srcip=entry['srcip'])

	if entry['dstip'] != '*':
		matches = matches & match(dstip=entry['dstip'])

	if entry['dstmac'] != '*':
		matches = matches & match(dstmac=entry['dstmac'])

	if entry['srcmac'] != '*':
		matches = matches & match(srcmac=entry['srcmac'])
		

        rules.append(matches)
        pass
    
    print rules;
    allowed = ~(union(rules))
    return allowed
