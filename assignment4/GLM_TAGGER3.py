from __future__ import division
import sys
from math import *
import re

#to store weights of the features
class WEIGHT:
	def __init__(self):
		self.weight = {}

	def getweight(self):
		return self.weight

weight = WEIGHT()

#get features open the dev file and use viterbi 
#algorithm for both parameter estimation(estimating weights)
#and decoding
class GML_VITERBI:
	def __init__(self, handle, outfile, choice, iteration):
		#number of times to run the 
		#algorithm to estimate weights through
		#perceptron
		self.iteration = iteration
		self.choice = choice
		self.features = FEATURES(choice)
		self.sentence = []
		self.y = []
		self.weight = weight.getweight()
		self.f_of_y = {}
		self.f_of_z = {}
		#files to write results on
		self.newfile = open(outfile, 'w')
		for h in range(0, self.iteration):
			#open the training file in case of
			#using this function for parameter
			#estimation through perceptron
			self.handle = open(handle)	
			print 'h:::', h
			counter = 0
			for l in self.handle:
				counter += 1
				self.line_arr = l.strip().split()
				if len(self.line_arr) == 0 and len(self.sentence) > 0:
					self.viterbi(self.sentence, self.newfile)
					del self.sentence[:]
					del self.y[:]
				else:
					self.sentence.append(self.line_arr[0])
					if self.choice == 'suffix':
						self.y.append(self.line_arr[1])
			self.handle.close()
		self.newfile.close()
	def K(self, k):
		if k in range(-1, 1):
			return ['*']
		else:
			return self.tags
	#take a list of pairs, return the pair with highest second member
	#comparing the second member of each pair 
	def argmax(self, ls):
		return max(ls, key = lambda x: x[1])

	#go through each sentence word by word
	def viterbi(self, sentence, newfile):
		n = len(sentence)
		z = [""] * (n + 1)
		sentence = [""] + sentence
		self.bp = {}
		self.PI = {}
		self.tags = ['O', 'I-GENE']
		for k in range(1, n + 1):
			self.PI[(0.0, '*', '*')] = 0.0
			#t is the tag on the word before the current		
			for t in self.K(k - 1):
				#u is the tag on the current word
				for u in self.K(k):
					self.bp[(k, t, u)], self.PI[(k, t, u)] = self.argmax([(s, self.PI[(k - 1, s, t)] + \
					sum(self.weight.get(l, 0.0) * val for l, val in g.iteritems())) for s in self.K(k - 2)\
					for g in self.features.getgs(s, t, u, sentence[k])])
		#find the last two tags and then find the rest of the tags going backwards 
		(z[n - 1], z[n]), p = self.argmax([((s,t), self.PI.get((n, s, t), 0.0) + \
		sum(self.weight.get(l, 0.0) * val for l, val in g.iteritems())) for s in self.K(n - 1) for t in self.K(n)\
		for g in self.features.getgs(s, t, 'STOP', sentence[k])])
		for k in range(n - 2, 0, -1):
			z[k] = self.bp[(k + 2, z[k + 1], z[k + 2])]
		z[0] = '*'
		# if the instance of the class is used for parameter estimation(choice is 'suffix') use perceptron
		if self.features.choice == 'suffix':
			z.pop(0)
			z.append('STOP')
			self.y.append('STOP') 
			self.perceptron(self.sentence, z, n)
		#if the parameter estimation is already done and want to decode, the argument will be set to 'gml'
		if self.choice == 'gml':	
			for i in range(1, n + 1):
				l = sentence[i] + " " + z[i]
				self.newfile.write( "%s\n"% l)
			self.newfile.write("\n")
		self.PI.clear()
		self.bp.clear()	

	#based on golden tag sequence and best tag sequence(estimated by viterbi)
	#find the global feature vector and factor them in the weight vector(it's actually just a map from features to weights)
	def perceptron(self, sentence, z, n):
		if (self.equal(self.y, z) == False):		
			#get the feature vector for the golden tag sequence(retrieved from training dataset)
			y = self.calculate_global_f(self.y, self.sentence, n)
			#get the feature vector for the best tag sequence (estimated by viterbi)
			z = self.calculate_global_f(z, self.sentence, n)
			#go through local vectors
			for g in y:
				if g in self.weight:
					self.weight[g] += y[g]
				else:
					self.weight[g] = y[g]
			for g in z:
				if g in self.weight:
					self.weight[g] -= z[g]
				else:
					self.weight[g] = -z[g]

	def calculate_global_f(self, tags, sentence, n):
		gs = {}
		for i in range(1, n):
			if i == 1:
				s = '*' 
				t = '*'
			elif i == 2:
				s = '*'
				t = tags[i - 1]
			else :
				s = tags[i - 2]
				t = tags[i - 1]
			g = self.features.getgs(s, t, tags[i], sentence[i])
			for feature in g[0]:
				if feature in gs:
					gs[feature] += 1
				else:
					gs[feature] = 1
		return gs 
	
	#see if the golden tag sequence and the best tag sequence(estimated by viterbi)
	#are the same if not perceptron will be called to adjust the weights
	def equal(self, y, z):
		for i in range(0, len(y)):
			if y[i] != z[i]:
				return False	
		return True
									
#here is were you should add new features depending on the set you want to 
#tag (have to look at the words you want to tag and see what features do they have in common
#for instance many gene names have capital letters in them that's why I used CAP feature here)
class FEATURES:
	def __init__(self, choice):
		self.choice = choice
	def getgs(self,s, t, u, word):
		self.f = {}
		wordlen = len(word)
		for j in range(1, 4):
			if wordlen - j > 0:
				suffix = word[wordlen - j:]
				if ('SUFF:', suffix, ':', j, ':', u) in self.f:
					self.f[('SUFF:', suffix, ':', j, ':', u)] += 1
				else:
					self.f[('SUFF:', suffix, ':', j, ':', u)] = 1
                
		for j in range(1, 4):
			if wordlen - j > 0:
				prefix = word[:j]
				if ('PREF:', prefix, ':', j, ':', u) in self.f:
					self.f[('PREF:', prefix, ':', j, ':', u)] += 1
				else:
					self.f[('PREF:', prefix, ':', j, ':', u)] = 1
                
		self.f[('TRIGRAM:' + str(s) + ':' + str(t) + ':' + str(u))] = 1
		self.f[('TAG:' + str(word) + ':' + str(u))] = 1
		#see if there are words with one letter only(I added this after 
		#going through the dev set and noticing that some of the lines 
		#had just '-' in them and were all tagged as I-GENE by my perceptron algorithm
		#while in the training set they are actually just labeled 'O')
		if wordlen == 1:
				if ('MONO:', u) in self.f:
					self.f[('MONO:', u)] += 1
				else:
					self.f[('MONO:', u)] = 1
	
		letters = [l for l in word if l.isupper()]
		len_letters = len(letters)
		if len(letters) >= len(word):
				if ('CAP:', len_letters, ':', u) in self.f:
					self.f[('CAP:', len_letters, ':', u)] += 1
				else:
					self.f[('CAP:', len_letters, ':', u)] = 1
			

		return [self.f]

#train weights
perceptron_viterbi = GML_VITERBI('../docs/gene.train', '../docs/gene_dev.p3.out', 'suffix', 5)

weightfile = open('../docs/weights', 'w')

#write the weights obtained by above instance of GML_VITERBI class to the weightfile(../docs/weights)
weights = perceptron_viterbi.weight
for feature, wt in weights.iteritems():
	weightstring = str(feature) + ' ' + str(wt)
	weightfile.write("%s\n"% weightstring)

#decode
gml_viterbi = GML_VITERBI('../docs/gene.dev', '../docs/gene_dev.p3.out', 'gml', 1)

