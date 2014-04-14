#!/usr/bin/env python
from os import path
import sys
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("input_tagged", help="Input generated from tagger")
parser.add_argument("golden_tagged", help="Input gold")
args = parser.parse_args()

def levenshtein(s1, s2):
    #print "LEVENSHTEIN!\ns1={}\ns2={}".format(s1, s2)
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

golden_f = open(args.golden_tagged, 'r')
input_f = open(args.input_tagged, 'r')

c = 0
new_sentence = True
buf1 = []
buf2 = []
buf3 = []

end = False
print "Original\tgolden\ttagged"
while not end:
    in1 = golden_f.readline()
    in2 = input_f.readline()

    if in1 == in2 == "":
        break

    if (in1 == "\n") != (in2 == "\n"):
        print "Unexpected end of sentence!\n"
        sys.exit(2) # wrong tagged.txt

    if in1 == in2 == "\n":
        for i, word in enumerate(buf1):
            print "{}\t{}\t{}".format(buf1[i], buf2[i], buf3[i])
        #print "end of sentence.\nbuf1={}\nbuf2={}\nbuf3={}".format(buf1, buf2, buf3)

        phrase_len = len(buf1)
        
        # temporarly remove nulls from buffers, until we'll have a nullifier
        i = 0
        while i < len(buf2):
            if buf2[i] == 'null':
                del buf2[i]
                del buf3[i]
            else:
                i += 1
        print "---{edit_d}---{CER}---\n".format(edit_d=levenshtein(buf2, buf3), CER=levenshtein(buf2, buf3)/float(phrase_len))

        buf1 = []
        buf2 = []
        buf3 = []
        continue

    if (in1 == "") != (in2 == ""):
        c += 1

    buf1.append(in1.split()[0])
    buf2.append(in1.split()[1])
    buf3.append(in2.split()[1])

    #print buf1[-1] + "\t" + buf2[-1]

sys.exit(c)
