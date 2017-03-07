
# the only difference between this file and CKYparser3.py is that different files
# are passed to count_words() function for populating counts data structures (dictionaries), namely nonterminals
# binaryrules and wordscounts.
import json
import decimal

nonterminals = {}
binaryrules = {}
wordscounts = {}
qml_binary = {}
qml_unary = {}
nonterminals_collection = {}
words = []

def count_words(countsfile):
	with open(countsfile) as f:
		for line in f:
			word_group = line.strip().split()
			if(word_group[1] == 'UNARYRULE'):
				wordscounts[(word_group[2], word_group[3])] = decimal.Decimal(word_group[0])
				words.append(word_group[3])
			if(word_group[1] == 'NONTERMINAL'):
				nonterminals[word_group[2]] = decimal.Decimal(word_group[0])
			if(word_group[1] == 'BINARYRULE'):
				binaryrules[word_group[2], word_group[3], word_group[4]] = decimal.Decimal(word_group[0])
				if(nonterminals_collection.has_key(word_group[2])):
					nonterminals_collection[word_group[2]].append((word_group[3], word_group[4]))
				else:
					nonterminals_collection[word_group[2]] = [(word_group[3], word_group[4])]

def qmlbinary():
	for rule, count in binaryrules.items():
		qml_binary[rule] = count / nonterminals[rule[0]]

def qmlunary():
	for rule, count in wordscounts.items():
		qml_unary[rule] = decimal.Decimal(count /  nonterminals[rule[0]])

pi = {}
bp = {}
pitemp = []
twoandfours = []

def CKY(sentence):
	for k in range(1 , len(sentence) + 1):
		for X, count in nonterminals.items():
			word = ''	
			if sentence[k - 1] not in words:
				word = '_RARE_'
			else:
				 word = sentence[k - 1]
			pi[k, k, X] = qml_unary.get((X, word), 0)
			if(pi[k, k, X] != 0):
				bp[k, k, X] = (X, word)
	for l in range(1, len(sentence) + 1):
		for i in range(1, len(sentence) + 1):
			j = i + l
			if j <= len(sentence):
				for X, count in nonterminals.items():
					if nonterminals_collection.get(X, 0) != 0:
						for nonterminal in nonterminals_collection[X]:
							for s in range(i, j):
								if decimal.Decimal(pi.get((i, s, nonterminal[0]), 0)) > 0 and decimal.Decimal(pi.get((s + 1, j, nonterminal[1]), 0)) > 0:
									pitemp.append(((X, (i, s, nonterminal[0]), (s + 1, j, nonterminal[1])), qml_binary.get((X, nonterminal[0], nonterminal[1]), 0) * decimal.Decimal(pi[i, s, nonterminal[0]]) * decimal.Decimal(pi[s + 1, j,nonterminal[1]])))
						if pitemp:
							bp[i, j, X], pi[i, j, X] = argmax(pitemp)				
						del pitemp[:]

						#bp[i, j, X], pi[i, j, X] = argmax([((X, nonterminal[0], nonterminal[1]), qml_binary.get((X, nonterminal[0], nonterminal[1]), 0) * pi.get((i, s, nonterminal[0]), 0) * pi.get((s + 1, j,nonterminal[1]), 0)) for nonterminal in nonterminals_collection[X] for s in range(i, j)])
					#bp[i, j, X], pi[i, j, X] = argmax([(X, qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1]), 0) * pi.get((i, s, nonterminal[0]), 0) * pi.get((s + 1, j,nonterminal[1]), 0) for nonterminal in nonterminals_collection[X] for s in range(i, j)])

def argmax(ls):
	return max(ls, key = lambda x : x[1])


count_words('../docs/parse_train_vert.counts.out')
qmlbinary()
qmlunary()

def buildparsetree(backpointer):
	if isinstance(backpointer[1], basestring):
		return [backpointer[0], backpointer[1]]
	else:	
		return [backpointer[0], buildparsetree(bp[backpointer[1]]),buildparsetree(bp[backpointer[2]])] 


def parsefile(filetobeparsed, bp):
	new_file = open(outfile, 'w')
	with open(filetobeparsed) as f:
		for line in f:
			sentence = line.strip().split()
			CKY(sentence)
			jasondata = json.dumps(buildparsetree(bp[1, len(sentence), 'SBARQ']), outfile)
			new_file.write("%s\n"% jasondata)
			pi.clear()
			bp.clear()

	new_file.close()

outfile = '../docs/parse_dev1.out' 
parsefile('../docs/parse_dev.dat', bp)

