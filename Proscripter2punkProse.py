"""
Lisanne Wiengarten
Matriculation no. 3249897
Master thesis @ Vu
IMS, SuSe 18

Given a .csv file created by Proscripter, convert it into a .csv file that can be used as input for punkProse

Also creates vocabulary.txt and pos_vocabulary.txt needed for punkProse
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import wave
from pattern.en import parse


# Usage function
def usage():
	print "Usage of " +sys.argv[0]+":"
	print "python "+sys.argv[0]+" --help shows this message"
	print "For converting from Proscripter to punkProse: python "+sys.argv[0]+" --f proscripteroutput.csv"
	

def convert(inputfile):

	vocabulary = set()
	pos_voc = set()
	
	input = open(inputfile, "r")
	filename = inputfile[inputfile.rfind('/')+1:]
	out = open(inputfile.replace(".proscript", ""), "w")
	out.write("word|punctuation_before|pos|pause_before|f0_mean|f0_range|f0_birange|f0_sd|i0_mean|i0_range|i0_birange|i0_sd|speech_rate_norm\n")

	lines = input.readlines()
	for i in range(1,len(lines)):
		parts = lines[i].split("\t")
		if len(parts) > 2:
			pos = "|NaN"
				
			# word
			out.write(parts[0]+"|")
			
			vocabulary.add(parts[0])
			
			# punctuation_before
			# punctuation is unknown, since this is what we want to detect!
			# for testing, we need to recover the correct punctuation from the goldstandard
			''' if gold_exists:
					textfile = open(+filename.replace(".proscript.csv", ".txt"), "r")
					textlines = textfile.readlines()
					text = textlines[0].split(" ")
			
					for j in range(len(text)):
						if re.sub('[^0-9a-zA-Z]+', '', text[j]) == parts[0]:
							if "..." in text[j-1]:
								out.write("...|")
							elif "." in text[j-1]:
								out.write(".|")
							elif "," in text[j-1]:
								out.write(",|")
							elif "?" in text[j-1]:
								out.write("?|")
							elif "!" in text[j-1]:
								out.write("!|")
							elif "-" in text[j-1]:
								out.write("-|")
							elif ";" in text[j-1]:
								out.write(";|")
							else:
								out.write("|")
							break
							
						if j == len(text)-1:
							out.write("|")
			else: '''
			out.write("|")		
			
			# pos
			# pos tag is unknown so far, so we need to do pos tagging
			# the pattern parser offers up to three tags it deems likely, but we only choose the first one
			tags = parse(parts[0].replace("\n", ""))
			splittags = tags.split("/")
			pos = splittags[1]
			out.write(pos+"|")
			
			pos_voc.add(pos)
				
			# pause_before
			# the other parts can simply be copied from the proscripter file
			out.write(parts[4]+"|")
				
			# f0_mean
			out.write(parts[6]+"|")
				
			# f0_range
			out.write(parts[12]+"|")
				
			# f0_birange = ???
			out.write("0.0|")
				
			# f0_sd
			out.write(parts[10]+"|")
				
			# i0_mean
			out.write(parts[7]+"|")
				
			# i0_range
			out.write(parts[13]+"|")
				
			# i0_birange = ???
			out.write("0.0|")
				
			# i0_sd
			out.write(parts[11]+"|")
				
			# speech_rate_norm
			out.write(parts[5]+"\n")
						
	# <END>|.|<END>|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0
	out.write("<END>|.|<END>|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0\n")
							
	out.close()
	
	# Create the vocabulary.txt and pos_vocabulary.txt needed for punkProse
	vocabfile = open("vocabulary.txt", "w")
	vocabfile.write("<END>\n<UNK>\n<EMP>\n")
	for item in sorted(vocabulary):
		vocabfile.write(item+"\n")
	vocabfile.close()
		
	posfile = open("pos_vocabulary.txt", "w")
	posfile.write("<END>\n<UNK>\n<EMP>\n")
	for item in sorted(pos_voc):
		posfile.write(item+"\n")
	posfile.close()
	
	
	
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
