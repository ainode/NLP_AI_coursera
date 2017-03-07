from itertools import izip
import pickle
tparams = {}
qparams = {}
countof_j_i_l_m = {}
countof_i_l_m = {}
countof_en_es = {}
countof_en = {}

def get_tparams(dictfile):	
	global tparams
	tparams = pickle.load(open(dictfile))	

def fillqparams(enfile, esfile):
	en = open(enfile)
	es = open(esfile)
	for enline, esline in izip(en, es):
		enline_arr = enline.strip().split()
		esline_arr = esline.strip().split()
		enline_arr = ['NULL'] + enline_arr
		initialize_qparams(enline_arr, esline_arr)
	en.close()
	es.close()

def initialize_qparams(enline_arr, esline_arr):
	l = len(enline_arr)
	m = len(esline_arr)
	for j in range(l):
		for i in range(1, m + 1):
			if j in qparams:				
				qparams[j][(i, l, m)] = 1.0 / l
			else:
				qparams[j] = {(i, l, m) : 1.0 / l}

def ibm2(esfile, enfile, t):
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
		update_params()

def resetcounts():
	countof_en_es.clear()
	countof_en.clear()
	countof_j_i_l_m.clear()
	countof_i_l_m.clear()

def calculate_counts(esline_arr, enline_arr):
	m = len(esline_arr)
	l = len(enline_arr)
	for i, esword in enumerate(esline_arr):
		i += 1
		total_esword_trans = get_total_params(esword, enline_arr, (i, l, m))
		for j, enword in enumerate(enline_arr):
			delta = qparams[j][(i, l, m)] * tparams[enword][esword]/total_esword_trans
			if (j, i, l, m) in countof_j_i_l_m:
				countof_j_i_l_m[(j, i, l, m)] += delta
			else:	
				countof_j_i_l_m[(j, i, l, m)] = delta 			
			if (i, l, m) in countof_i_l_m:
				countof_i_l_m[(i, l, m)] += delta
			else:
				countof_i_l_m[(i, l, m)] = delta
			if (enword, esword) in countof_en_es:
				countof_en_es[(enword, esword)] += delta
			else:	
				countof_en_es[(enword, esword)] = delta 			
			if enword in countof_en:
				countof_en[enword] += delta
			else:
				countof_en[enword] = delta

def get_total_params(esword, enline_arr, (i, l, m)):
	total = 0.0
	for j, enword in enumerate(enline_arr):
		total += tparams[enword][esword] * qparams[j][(i, l, m)]
	return total

def update_params():
	for  en_es in countof_en_es:
		if countof_en[en_es[0]] > 0.0:
			tparams[en_es[0]][en_es[1]] = countof_en_es[en_es]/countof_en[en_es[0]]
	for jtom in countof_j_i_l_m:
		if countof_i_l_m[(jtom[1], jtom[2], jtom[3])] > 0:
			qparams[jtom[0]][(jtom[1], jtom[2], jtom[3])] = countof_j_i_l_m[jtom] / countof_i_l_m[(jtom[1], jtom[2], jtom[3])]	

def find_alignment(dev_es, dev_en, outfile):
	es = open(dev_es)
	en = open(dev_en)
	linecount = 0
	out_file = open(outfile, 'w')
	for esline, enline in izip(es, en):
		esline_arr = esline.strip().split()
		enline_arr = enline.strip().split()
		enline_arr = ['NULL'] + enline_arr
		l = len(enline_arr)
		m = len(esline_arr)
		linecount += 1
		for inx, esword in enumerate(esline_arr):
			if not enline_arr:
				enline_arr.append('NULL')
			if enline_arr:
				maxelements = argmax([(tparams[enword][esword] * qparams[indx][(inx + 1, l, m)], enword, indx) for indx, enword in enumerate(enline_arr)])
				align_line = str(linecount) + ' ' + str(inx + 1) + ' ' + str(maxelements[2]) 
				out_file.write("%s\n"% align_line)
	out_file.close()

def argmax(ls):
	return max(ls, key = lambda x : x[0])

get_tparams('../docs/tparams_es.p')

fillqparams('../docs/corpus.es', '../docs/corpus.en') 

ibm2('../docs/corpus.en', '../docs/corpus.es', 5)

find_alignment('../docs/dev.en', '../docs/dev.es', '../docs/dev_es.out')

