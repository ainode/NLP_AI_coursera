#class translator:
#	def __init__(file1, file2)

from itertools import izip
import pickle

tparams = {}
NULL_tparam = 0
tparams['NULL'] = {}
countof_en_es = {}
countof_en = {}

def fromfiles(enfile, esfile):
	en = open(enfile)
	es = open(esfile)
	for enline, esline in izip(en, es):
		enline_arr = enline.strip().split()
		esline_arr = esline.strip().split()
		enline_arr = ['NULL'] + enline_arr 
		fill_tparams(enline_arr, esline_arr)
	es.close()
	en.close()

def fill_tparams(arr1, arr2):
	for enword in arr1:
		for esword in arr2:
			#fill_NULL_tparams(enword)
			if enword in tparams:
				if esword in tparams[enword]:
					tparams[enword][esword] += 1
				else:
					tparams[enword][esword] = 1
			else :
				tparams[enword] = {esword : 1}

def fill_NULL_tparams(es_word):
	if es_word in tparams['NULL']:	
		tparams['NULL'][es_word] += 1
	else:
		tparams['NULL'][es_word] = 1

def initialize_tparams():
	global NULL_tparam
	for ekey in tparams:
		for fkey in tparams[ekey]:
			tparams[ekey][fkey] = 1 / float(len(tparams[ekey]))
	#initializing NULL value for every foreign word
	#print 'NULL_tparams', NULL_tparam
	#NULL_tparam = 1/ float(len(tparams['NULL']))
	#print 'real NULL_tparams ', NULL_tparam

def ibm1(esfile, enfile, t):
	for iteration in range(t):
		resetcounts()
		es = open(esfile)
		en = open(enfile)
		for esline, enline in izip(es, en):
			esline_arr = esline.strip().split()
			enline_arr = enline.strip().split()
			enline_arr = ['NULL'] + enline_arr	
			calculate_counts(esline_arr, enline_arr)
		es.close()
		en.close()
		update_tparams()
		#get_max_tparams()
	
def resetcounts():
	global countof_en_es
	global countof_en
	countof_en_es = {}
	countof_en = {}		

def calculate_counts(esline_arr, enline_arr):
	for esword in esline_arr:
		for enword in enline_arr:
			delta = tparams[enword][esword]/get_total_esword_trans(esword, enline_arr)
			if (enword, esword) in countof_en_es:
				countof_en_es[(enword, esword)] += delta
			else:	
				countof_en_es[(enword, esword)] = delta 			
			if enword in countof_en:
				countof_en[enword] += delta
			else:
				countof_en[enword] = delta
		
def get_total_esword_trans(esword, enline_arr):
	total = 0.0
	for enword in enline_arr:
		total += tparams[enword][esword]
	return total

def update_tparams():
	for  en_es in countof_en_es:
		tparams[en_es[0]][en_es[1]] = countof_en_es[en_es]/countof_en[en_es[0]]

def save_tparams(outfile):
	pickle.dump(tparams, open(outfile, "wb"))
	#f = open(outfile, 'w')
	#f.write(str(tparams))
	#f.close()
	#dictfile = open(outfile, 'r')
	#new_tparams = eval(dictfile.read())

 
fromfiles('../docs/corpus.en', '../docs/corpus.es')

initialize_tparams()

ibm1( '../docs/corpus.es', '../docs/corpus.en', 5)

outfile = '../docs/tparams.p'

save_tparams(outfile)


#print 'tparams[resumption]: ', tparams['resumption']
#print 'tparams[session]: ', tparams['session']
#print 'tparams[session][sesiones]: ', tparams['session']['sesiones'], 'tparams[session][del] :', tparams['session']['del']

