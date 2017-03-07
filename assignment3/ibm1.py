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
			if enword in tparams:
				if esword in tparams[enword]:
					tparams[enword][esword] += 1
				else:
					tparams[enword][esword] = 1
			else :
				tparams[enword] = {esword : 1}

def initialize_tparams():
	global NULL_tparam
	for ekey in tparams:
		for fkey in tparams[ekey]:
			tparams[ekey][fkey] = 1 / float(len(tparams[ekey]))
	NULL_tparam = 1/ float(len(tparams['NULL']))

def ibm1(esfile, enfile, t):
	for iteration in range(t):
		print 'iteration: ', iteration
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
		print 'length of en_es: ', len(countof_en_es)
		print 'length of en: ', len(countof_en)
		update_tparams()
		#get_max_tparams()
	
def calculate_counts(esline_arr, enline_arr):
	for esword in esline_arr:
		total_esword_trans = get_total_esword_trans(esword, enline_arr)
		for enword in enline_arr:
			delta = tparams[enword][esword]/total_esword_trans
			if (enword, esword) in countof_en_es:
				countof_en_es[(enword, esword)] += delta
			else:	
				countof_en_es[(enword, esword)] = delta 			
			if enword in countof_en:
				countof_en[enword] += delta
			else:
				countof_en[enword] = delta

def resetcounts():
	global countof_en_es
	global countof_en
	countof_en_es = {}
	countof_en = {}

		
def get_total_esword_trans(esword, enline_arr):
	total = 0.0
	for enword in enline_arr:
		total += tparams[enword][esword]
	return total

def update_tparams():
	for  en_es in countof_en_es:
		if countof_en[en_es[0]] > 0.0:
			tparams[en_es[0]][en_es[1]] = countof_en_es[en_es]/countof_en[en_es[0]]

def save_tparams(outfile):
	pickle.dump(tparams, open(outfile, "wb"))
 
fromfiles('../docs/corpus.es', '../docs/corpus.en')

initialize_tparams()

ibm1( '../docs/corpus.en', '../docs/corpus.es', 5)

#outfile = '../docs/tparams_es.p'

#save_tparams(outfile)

