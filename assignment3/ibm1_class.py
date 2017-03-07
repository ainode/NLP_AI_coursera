#class translator:
#	def __init__(file1, file2)

from itertools import izip
import pickle
import sys

#get translation parameters	
class TP:
	def __init__(self, file1, file2):
		self.tparams = {}
		self.NULL_tparam = 0
		self.tparams['NULL'] = {}
		self.countof_en_es = {}
		self.countof_en = {}
		self.enfile = file1
		self.esfile = file2
	#fill tparams dict with words as key their possible translations and their probability as dict values
	#initialize them with initial values 
	def fromfiles(self):
		self.en = open(self.enfile)
		self.es = open(self.esfile)
		for enline, esline in izip(self.en, self.es):
			self.enline_arr = enline.strip().split()
			self.esline_arr = esline.strip().split()
			self.enline_arr = ['NULL'] + self.enline_arr 
			self.fill_tparams(self.enline_arr, self.esline_arr)
		self.es.close()
		self.en.close()
		self.initialize_tparams()
	#fills tparams dict with words as keys and their possible translation 
	#in a dict as value
	def fill_tparams(self, arr1, arr2):
      		for enword in arr1:
			for esword in arr2:
				if enword in self.tparams:
					if esword in self.tparams[enword]:
						self.tparams[enword][esword] += 1
					else:
						self.tparams[enword][esword] = 1
				else :
					self.tparams[enword] = {esword : 1}
	#initialize tparams with the probability that is
	#calculated as 1/ number of words that could be a translation of the word
	def initialize_tparams(self):
		global NULL_tparam
		for ekey in self.tparams:
			for fkey in self.tparams[ekey]:
				self.tparams[ekey][fkey] = 1 / float(len(self.tparams[ekey]))
		NULL_tparam = 1/ float(len(self.tparams['NULL']))
	#calculate delta
	def calculate_counts(self, esline_arr, enline_arr):
		for esword in esline_arr:
			total_esword_trans = self.get_total_esword_trans(esword, enline_arr)
			for enword in enline_arr:
				delta = self.tparams[enword][esword]/total_esword_trans
				if (enword, esword) in self.countof_en_es:
					self.countof_en_es[(enword, esword)] += delta
				else:	
					self.countof_en_es[(enword, esword)] = delta 			
				if enword in self.countof_en:
					self.countof_en[enword] += delta
				else:
					self.countof_en[enword] = delta
	#reset the counts of words of the to 
	#corpuses after each iteration
	def resetcounts(self):
		self.countof_en_es.clear()
		self.countof_en.clear()
	#get total of probability of all words of the line
	#to be translation of the word
	def get_total_esword_trans(self, esword, enline_arr):
		total = 0.0
		for enword in enline_arr:
			total += self.tparams[enword][esword]
		return total
	#update probabilities in tparams dict after each iteration
	def update_tparams(self):
		for  en_es in self.countof_en_es:
			if self.countof_en[en_es[0]] > 0.0:
				self.tparams[en_es[0]][en_es[1]] = self.countof_en_es[en_es]/self.countof_en[en_es[0]]
#use ibm1 method to calculate the translation parameter		
def ibm1(esfile, enfile, tp, t):
	for iteration in range(t):
		print 'iteration: ', iteration
		tp.resetcounts()
		es = open(esfile)
		en = open(enfile)
		for esline, enline in izip(es, en):
			esline_arr = esline.strip().split()
			enline_arr = enline.strip().split()
			enline_arr = ['NULL'] + enline_arr	
			tp.calculate_counts(esline_arr, enline_arr)
		es.close()
		en.close()
		print 'length of en_es: ', len(tp.countof_en_es)
		print 'length of en: ', len(tp.countof_en)
		tp.update_tparams()
		#get_max_tparams()
	
#save tparams to a file
def save_tparams(outfile):
	pickle.dump(tparams, open(outfile, "wb"))
 
#get input from the user. arg1 file to be translated and arg2 translation
def main(file1, file2):
	#tp = TP('../docs/corpus.es', '../docs/corpus.en')
	tp = TP(file1, file2)
	tp.fromfiles()
	print len(tp.tparams)
	#ibm1( '../docs/corpus.en', '../docs/corpus.es', tp, 5)
	ibm1(file2, file1, tp, 5)
if __name__ == "__main__" :
	main(sys.argv[1], sys.argv[2])

