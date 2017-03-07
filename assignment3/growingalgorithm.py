from itertools import izip
from operator import itemgetter

enline_list = []
esline_list = []

def find_intersections(dev_en, dev_es, outfile):
	en = open(dev_en)
	es = open(dev_es)
	for enline, esline in izip(en, es):
		global enline_list, esline_list
		enline_arr = enline.strip().split()
		esline_arr = esline.strip().split()
		enline_list += [enline_arr]
		esline_list += [esline_arr]
		#mergedline_arr = [filter(lambda x : x in esline_arr, sublist) for sublist in enline_arr]
		#mergedline_set = set(esline_arr).intersection(enline_arr)
		#mergedline = mergedline_arr[0] + ' ' + mergedline_arr[1] + ' ' + mergedline_arr[2]
	merge(enline_list, esline_list, outfile)
	#out_file.write("%s\n"% mergedline)

def merge(enline_list, esline_list, outfile):
	out_file = open(outfile, 'w')
	enset = set(repr(e) for e in enline_list)
	esset = set(repr(e) for e in esline_list)
	en_inter_es = esset.intersection(enset)
	en_inter_es_arr = [eval(e) for e in en_inter_es]
	en_inter_es_arr = sorted(en_inter_es_arr, key = itemgetter(0, 1, 2))
	for line_arr in en_inter_es_arr:
		line = line_arr[0] + ' ' + line_arr[1] + ' ' + line_arr[2]
		out_file.write("%s\n"% line)
	

find_intersections('../docs/dev.out', '../docs/dev_es.out', '../docs/dev_merge.out')
