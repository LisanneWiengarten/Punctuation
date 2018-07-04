"""
Lisanne Wiengarten
Matriculation no. 3249897
Master thesis @ Vu
IMS, SuSe 18

Given a .words file created by IMS Aligner, convert it into a .align file that can be used as input for Proscripter
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import wave


# Usage function
def usage():
	print "Usage of " +sys.argv[0]+":"
	print "python "+sys.argv[0]+" --help shows this message"
	print "For converting from .words to .align: python "+sys.argv[0]+" --f imsoutput.words"
	

def convert(inputfile):
	
	input = open(inputfile, "r")
	filename = inputfile[inputfile.rfind('/')+1:].replace(".words", "")
	out = open(inputfile.replace(".words", ".align"), "w")
	out.write("conv\tspk\tpart\tsid\tchno\tstarttime\tendtime\tword.id\twavfile\tword\n")
	
	counter = 0
	lines = input.readlines()
	for i in range(1,len(lines)):
	
		# Ignore _SIL_ and brth
		if "_SIL_" not in lines[i] and "brth" not in lines[i] and "<P>" not in lines[i]:
			counter += 1
	
			# conv = filename
			out.write(filename+"\t")
		
			# spk = speaker unknown/unimportant
			out.write("UNK\t")
		
			# part = speaker unknown/unimportant
			out.write("UNK\t")
		
			# sid = running number of ids from 1
			out.write(str(counter)+"\t")
		
			# chno = NA
			out.write("NA\t")
		
			# starttime
			split = lines[i].split(" ")
			start = float(split[0])
			out.write(str(round(start, 2))+"\t")
		
			# endtime
			# if the file ends with silence, we can use this time step as end
			if i < len(lines)-1:
				splitnext = lines[i+1].split(" ")
				end = float(splitnext[0])
				out.write(str(round(end, 2))+"\t")
				
			# else, we need to see how long the wav-file is
			else:
				wfile = wave.open("../Aligner/"+filename+".wav", "r")
				time = (1.0 * wfile.getnframes ()) / wfile.getframerate ()
				out.write(str(round(float(time), 2))+"\t")
			
			# word.id = conv + UNK + words + i
			wordid = filename + ".UNK.words" + str(counter)
			out.write(wordid+"\t")
		
			# wavfile
			out.write(filename+".wav"+"\t")
		
			# word
			out.write(split[2].lower())
			
	out.close()
	
	
	
### MAIN FUNCTION ###
def main(argv):	

	# Parse command line arguments and parameters
	try:
		options, remainder = getopt.getopt(argv[1:], 'o:t', ['file=','help'])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)
		usage()
		sys.exit(2)
	
	if len(options) == 0:
		usage()
		sys.exit(2)

	for opt, arg in options:
	
		# START PROCESS #
		if opt in ('--f', '--file'):
			convert(arg)
				
		# HELP FUNCTION #
		elif opt in ('--help', '--h'):
			usage()
			sys.exit(2)


		
if __name__ == "__main__":
	main(sys.argv)
