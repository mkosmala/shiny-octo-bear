#!/usr/bin/python

import sys
import codecs


if len(sys.argv) < 3 :
    print ("format: convert_file <input_file> <output_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

with codecs.open(infilename,'r',encoding='cp1252') as infile, codecs.open(outfilename,'w',encoding='utf-8') as outfile:

    for line in infile:
        outfile.write(line)
        
