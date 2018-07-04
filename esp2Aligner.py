"""
Lisanne Wiengarten
Matriculation no. 3249897
Master thesis @ Vu
IMS, SuSe 18

Given the output results from espnet, create simple text files as input for the IMS Aligner
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import getopt
import glob
import json
from pprint import pprint
import string


# Usage function
def usage():
	print "Usage of " +sys.argv[0]+":"
	print "python "+sys.argv[0]+" --help shows this message"
	print "For preparing data for Aligner: python "+sys.argv[0]+" --o outputdirectory --d espdecodedirectory"
	

def convert(inputdir, outputdir):

	os.chdir(inputdir)
	for file in glob.glob("*.json"):
		current = open(file, "r")
		lines = current.readlines()
		for i in range(len(lines)):
			if "rec_text" in lines[i]:
				utt = lines[i-4].translate(None, string.punctuation).replace(" ", "").replace("\n", "")
				out = open(outputdir+"/"+utt+".sph.txt", "w")
				out.write(lines[i].replace("rec_text", "").replace("<blank>", "").replace("<eos>", "").replace("  ", "").replace("\n", "").translate(None, string.punctuation))
				out.close()
				
	
### MAIN FUNCTION ###
def main(argv):
	
	outputdir = ""
	# Parse command line arguments and parameters
	try:
		options, remainder = getopt.getopt(argv[1:], 'o:t', ['output=','dir=','help'])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)
		usage()
		sys.exit(2)
	
	if len(options) == 0:
		usage()
		sys.exit(2)

	for opt, arg in options:
	
		# HELP FUNCTION #
		if opt in ('--help', '--h'):
			usage()
			sys.exit(2)
	
		# OUTPUT DIRECTORY #
		if opt in ('--o', '--output'):
			outputdir = arg
	
		# START PROCESS #
		if opt in ('--d', '--dir'):
			if outputdir == "":
				convert(arg, arg)
			else:
				convert(arg, outputdir)
				


		
if __name__ == "__main__":
	main(sys.argv)
