#!/usr/bin/python

import collections

def recursePrint(struct, tab=""):
	if type(struct) == type(""):
		print "%s%s" % (tab,struct.replace("\n","\n"+tab))
	elif type(struct) == type([]):
		count = 0
		for item in struct:
			print "%sList index %d" % ( tab, count)
			recursePrint(item, tab+"\t")
			count += 1
	elif type(struct) == type({}) or type(struct) == type(collections.OrderedDict()):
		for key in struct:
			print "%s%s" % ( tab, key)
			recursePrint(struct[key],tab+"\t")
	else:
		print "%s%s" %( tab, str(struct).replace("\n","\n"+tab) )