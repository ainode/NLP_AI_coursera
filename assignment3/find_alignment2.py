
from itertools import izip
import pickle

tparams = {}

def get_tparams(dictfile):	
	global tparams
	tparams = pickle.load(open(dictfile))	
	#f = open(dictfile, 'r')
	#tparams = eval(f.read())

def find_alignment(dev_es, dev_en, outfile):
	es = open(dev_es)
	en = open(dev_en)
	linecount = 0
	out_file = open(outfile, 'w')
	for esline, enline in izip(es, en):
		esline_arr = esline.strip().split()
		enline_arr = enline.strip().split()
		enline_arr = ['NULL'] + enline_arr
		#print enline_arr
		linecount += 1
		for inx, enword in enumerate(enline_arr):
			maxelements = argmax([(tparams[enword][esword], esword, indx) for indx, esword in enumerate(esline_arr)])
			align_line = str(linecount) + ' ' + str(inx + 1) + ' ' + str(maxelements[2] + 1)
			print str(linecount) + ' - ' + enword + ': ' + maxelements[1] + ': ' + str(tparams[enword][esword])
			if tparams[enword][esword] > tparams['NULL'][maxelements[1]]:
				out_file.write("%s\n"% align_line)
			enline_arr.remove(enword)
			#print 'hello'
	out_file.close()

def argmax(ls):
	return max(ls, key = lambda x : x[0])

get_tparams('../docs/tparams.p')

find_alignment('../docs/dev.es', '../docs/dev.en', '../docs/dev.out')

print tparams['callanan']['respecto']
print tparams['regard']['respecto'] 
print tparams['callanan']['callanan']
print tparams['callanan']['respecto'] < tparams['callanan']['callanan']
print tparams['NULL']['de'] > tparams['NULL']['grupo']
def argmax1(ls):
	return max(ls, key = lambda x : x[1])

#print argmax1(tparams['regard'])

print 'tparams length: ', len(tparams)
totallength = 0
for es in tparams:
	totallength += len(es)
print totallength
