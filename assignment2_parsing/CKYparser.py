import json

nonterminals = {}
binaryrules = {}
words = {}
qml_binary = {}
qml_unary = {}
nonterminals_collection = {}
temp_words = {}
pimaxdict = {}

def count_words():
	with open('../docs/cfg.counts') as f:
		for line in f:
			word_group = line.split()
			if(word_group[1] == 'UNARYRULE'):
				temp_words[word_group[3]] = word_group[0]
				#words[word_group[3]] = words.get(word_group[3], 0) + float(word_group[0])
				words[(word_group[2], word_group[3])] = float(word_group[0])
			if(word_group[1] == 'NONTERMINAL'):
				nonterminals[word_group[2]] = float(word_group[0])
			if(word_group[1] == 'BINARYRULE'):
				binaryrules[word_group[2] + " " + word_group[3] + " " + word_group[4]] = float(word_group[0])
				if(nonterminals_collection.has_key(word_group[2])):
					nonterminals_collection[word_group[2]].append((word_group[3], word_group[4]))
				else:
					nonterminals_collection[word_group[2]] = [(word_group[3], word_group[4])]

def qmlbinary():
	for rule, count in binaryrules.items():
		words = rule.split()
		qml_binary[rule] = count / nonterminals[words[0]]
		#print "rule: ", rule, " words[0]: ", words[0], "qml: ", qml_binary[rule], "nonterminals[words[0]]", nonterminals[words[0]]

def qmlunary():
	for rule, count in words.items():
		qml_unary[rule] = count /  nonterminals[rule[0]]
		#print "rule: ", rule, " words[0]: ", rule[0], "qml: ", qml_unary[rule], "nonterminals[words[0]]", nonterminals[rule[0]]
sentence = "in 1200 british convicts populate which colony"
sentence = sentence.split()

def pi1(i, j, X):
	#for nonterminal in nonterminals_collection[X]:
		#for s in range(i, j - 1):
	if i == j : 
		pimax = qml_unary.get((X, sentence[i]), 0)
		print "pimax: ", pimax, "X: ", X, "i: ", i, "sentence[i]: ", sentence[i]
		return pimax
	else :
		print "X: ", X, "i: ", i, "j: ", j
		print "nonterminals:   ", nonterminals_collection[X]
		print "pimax: ", pimax
		pimax = argmax([(i, (qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1], 0)) * pi1(i, s, nonterminal[0]) * pi1(s + 1, j,nonterminal[1])) for nonterminal in nonterminals_collection.get(X, 0) for s in range(i, j - 1) ])
	return pimax

pimaxlist = []

def pi(i, j, X):
	if i == j : 
		#pimax = float(qml_unary.get((X, sentence[i]), 0))
		#print "pimax: ", pimax, "X: ", X, "i: ", i, "sentence[i]: ", sentence[i]
		return float(qml_unary.get((X, sentence[i]), 0))
	else :
		if nonterminals_collection.get(X, 0) == 0:
			return 0.0
		else:
			#print "upper x: ", X#, nonterminals_collection.get(X, 0)
			for nonterminal in nonterminals_collection.get(X, 0):
				#print "i: ", i, "j: ", j,  "nonterminal: ", nonterminal
				for s in range(i, j):
					#print "X: ", X, "i: ", i, "j: ", j
					#print "nonterminals_collection[", X, "]: ", nonterminals_collection[X]
					#print "qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1], 0): ", qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1], 0)
					qmlbinary = qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1], 0.0)
					#print "qml_binary: ", qml_binary
					#print "(pi(i, s, nonterminal[0])): ", 
					#pi0 = (pi(i, s, nonterminal[0]))
					#print "nonterminal[1]: ", nonterminal[1]
					#print "(pi(", s, " + 1,",  j, ",nonterminal[1])): ", 
					#pi1 = (pi(s + 1, j,nonterminal[1]))
					#if isinstance(pi0, float) and isinstance(pi1, float):
					#print "pimaxLower: ", pi0 * pi1 * qmlbinary
					pimax = qmlbinary * pi(i, s, nonterminal[0]) * pi(s + 1, j,nonterminal[1]) 
					pimaxdict[X, i, j, nonterminal[0], nonterminal[1]] = pimax
					#if i == 4 and j == 6:
					#	pimaxlist.append(pimax)
					#else:
					#	print "faulty stuff:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ", nonterminal[0]
					print pimax	
			return pimax	
					#pimax = qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1], 0) * float(pi(i, s, nonterminal[0])) * float(pi(s + 1, j,nonterminal[1]))
	#return pimax


def argmax(ls):
	return max(ls, key = lambda x : x[1])

VP = 'VP'

count_words()
qmlbinary()
qmlunary()
#print "sentence[4]: ",sentence[4], "sentence[5]: ", sentence[5]
print pi(4, 6, 'VP')
#print pimaxlist
#print pimaxdict
#testlist = [nonterminal for nonterminal in nonterminals_collection['SBAR+VP']]
#print "testlist", testlist

