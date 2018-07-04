"""
Lisanne Wiengarten
Matriculation no. 3249897
Master thesis @ Vu
IMS, SuSe 18

Given a directory with sph files, prepare the utt2spk, spk2utt, wav.scp and text files for espnet
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import getopt
import glob


# Usage function
def usage():
	print "Usage of " +sys.argv[0]+":"
	print "python "+sys.argv[0]+" --help shows this message"
	print "For preparing data for espnet: python "+sys.argv[0]+" --d sphdatadirectory"
	

def convert(inputdir):
	outputdir = inputdir.replace("downloads", "data").replace("/wav", "")
	utt2spk = open(outputdir+"/utt2spk", "w")
	spk2utt = open(outputdir+"/spk2utt", "w")
	wavscp = open(outputdir+"/wav.scp", "w")
	text = open(outputdir+"/text", "w")

	files = [f for f in sorted(os.listdir(inputdir))]
	for file in files:
		if file.endswith(".sph"):
			# utt2spk = filename \t speaker
			utt2spk.write(file.replace(".sph", "")+"\t"+file[0:4]+"\n")
			
			# spk2utt = speaker \t filename
			spk2utt.write(file[0:4]+"\t"+file.replace(".sph", "")+"\n")
			
			# wav.scp = filename /mount/arbeitsdaten40/projekte/asr/wiengale/espnet/egs/an4/asr1/../../../tools/kaldi/tools/sph2pipe_v2.5/sph2pipe -f wav -p -c 1 ./downloads/INPUTDIR/wav/filename.sph |
			wavscp.write(file.replace(".sph", "")+" /mount/arbeitsdaten40/projekte/asr/wiengale/espnet/egs/an4/asr1/../../../tools/kaldi/tools/sph2pipe_v2.5/sph2pipe -f wav -p -c 1 ./"+inputdir[inputdir.find("downloads"):]+"/"+file+" |\n")
			
			# text = filename \t
			text.write(file.replace(".sph", "")+"\t"+"\n")

	utt2spk.close()
	spk2utt.close()
	wavscp.close()
	text.close()
	
	
### MAIN FUNCTION ###
def main(argv):	

	# Parse command line arguments and parameters
	try:
		options, remainder = getopt.getopt(argv[1:], 'o:t', ['dir=','help'])
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
		if opt in ('--d', '--dir'):
			convert(arg)
				
		# HELP FUNCTION #
		elif opt in ('--help', '--h'):
			usage()
			sys.exit(2)


		
if __name__ == "__main__":
	main(sys.argv)
