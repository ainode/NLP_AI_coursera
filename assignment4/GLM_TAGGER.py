from __future__ import division
import sys
from math import *
import re

class counts:
	def __init__(self, handle):
		self.features = {}
		self.v = {}
		self.handle = handle
		for l in handle:
			line_arr = l.strip().split()
			self.v[line_arr[0]] = float(line_arr[1])
		handle.close()

class GML_VITERBI:
	def __init__(self, handle, counts, outfile, choice, k):
		self.counts = counts
		self.features = FEATURES(choice)
		self.sentence = []
		self.newfile = open(outfile, 'w')		
		for i in range(0, k):
			for l in handle:
				self.line_arr = l.strip()
				if len(self.line_arr) == 0 and len(self.sentence) > 0:
					#print self.sentence
					self.viterbi(self.sentence, self.newfile)
					del self.sentence[:]
				else:
					self.sentence.append(self.line_arr)
			self.newfile.close()
	def K(self, k):
		if k in range(-1, 1):
			return ['*']
		else:
			return self.tags
	def argmax(self, ls):
		#print ls
		return max(ls, key = lambda x: x[1])

	def viterbi(self, sentence, newfile):
		#print 'sentence::', sentence
		n = len(sentence)
		y = [""] * (n + 1)
		sentence = [""] + sentence
		#print 'sentence::', sentence
		self.bp = {}
		self.PI = {}
		self.tags = ['O', 'I-GENE']
		for k in range(1, n + 1):
			self.PI[(0, '*', '*')] = 0.0		
			for t in self.K(k - 1):
				for u in self.K(k):
					#print 'k::', k
					self.bp[(k, t, u)], self.PI[(k, t, u)] = self.argmax([(s, self.PI[(k - 1, s, t)] + \
					sum(self.counts.v.get(l, 0.0) * val for l, val in g.iteritems())) for s in self.K(k - 2)\
					for g in self.features.getgs(s, t, u, sentence[k])])
					#for S in self.tags:
					#	print 'PI[(',k - 1, ',', S, ',', t,')]: ', self.PI.get((k - 1, S, t), 0)
					#print 'PIS::', self.PI[(k, t, u)]
					#print 'BPS::', self.bp[(k, t, u)]
		(y[n - 1], y[n]), p = self.argmax([((s,t), self.PI.get((n, s, t), 0.0) + \
		sum(self.counts.v.get(l, 0.0) * val for l, val in g.iteritems())) for s in self.K(n - 1) for t in self.K(n)\
		for g in self.features.getgs(s ,t , 'STOP', sentence[k])])
		#print 'ys::: ', y[n - 1], y[n], p
		for k in range(n - 2, 0, -1):
			#print 'y[k + 1]', y[k + 1], 'k: ', k
			y[k] = self.bp[(k + 2, y[k + 1], y[k + 2])]
		y[0] = '*'
		#print y		
		for i in range(1, n + 1):
			l = sentence[i] + " " + y[i]
			self.newfile.write( "%s\n"% l)
		self.newfile.write("\n")
		self.PI.clear()
		self.bp.clear()	

	def getgs(self, s, t, u, word):
		#print 'getgs::', [{('TRIGRAM:' + str(s) + ':' + str(t) + ':' + str(u)) : 1, ('TAG:' + str(u) + ':' + word) : 1}]
		return [{('TRIGRAM:' + str(s) + ':' + str(t) + ':' + str(u)) : 1.0, ('TAG:' + str(word) + ':' + str(u)) : 1.0}]

test_counts = counts(open('../docs/tag.model'))
#print test_counts.v

class FEATURES:
	def __init__(self, choice):
		self.choice = choice
	
	def getgs(self, s, t, u, word):
		wordlen = len(word)
		features = {('TRIGRAM:' + str(s) + ':' + str(t) + ':' + str(u)) : 1.0, ('TAG:' + str(word) + ':' + str(u)) : 1.0}
		if self.choice == 'simple': 	
			return 	[features]
		if self.choice == 'suffix':
			for j in range(2, 5):
				suffix = word(wordlen - j, wordlen - 1)
				features[('SUFF:', suffix, ':', j, ':', u)] = 1
			return [features]
		
test_gml_viterbi = GML_VITERBI(open('../docs/gene.dev'), test_counts, '../docs/gene_dev.p1.out', 'simple', 1)


#print test_gml_viterbi.bp
#if __name__ == "__main()__" :
#	main()
