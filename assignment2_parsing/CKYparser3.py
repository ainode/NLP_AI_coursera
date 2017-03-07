# this file does the first and second part of the assignment
# it implements CKY algorithem using Chomsky normal form input
# for natural language processing(context free). 

import json
import decimal

nonterminals = {}
binaryrules = {}
wordscounts = {}
qml_binary = {}
qml_unary = {}
nonterminals_collection = {}
words = []
pi = {}
bp = {}
pitemp = []


# get the counts file as the arguement and calculate the 
# counts of the words and the number of the occurance of
# the rules (Nonterminals and others)
def count_words(countsfile):
	with open(countsfile) as f:
		for line in f:
			word_group = line.strip().split()
			if(word_group[1] == 'UNARYRULE'):
				# set rule in form of a tuple as key and number of occurance as value(showing how many times a word appears under a specific tag)
				wordscounts[(word_group[2], word_group[3])] = decimal.Decimal(word_group[0])
				words.append(word_group[3])
			if(word_group[1] == 'NONTERMINAL'):
				# nonterminal as key and number of occurance as value
				nonterminals[word_group[2]] = decimal.Decimal(word_group[0])
			if(word_group[1] == 'BINARYRULE'):
				# rule as key, number of occurance as value (ex: VP VERB NP as key and 232 as value)
				binaryrules[word_group[2], word_group[3], word_group[4]] = decimal.Decimal(word_group[0])
				if(nonterminals_collection.has_key(word_group[2])):
					# nonterminal as key childs added into array as value (ex: VP as key and (VP , VERB) and (VERB, NOUN) appended to the array as value)
					nonterminals_collection[word_group[2]].append((word_group[3], word_group[4]))
				else:
					nonterminals_collection[word_group[2]] = [(word_group[3], word_group[4])]

# devide the occurance of a rule (VP VERB NOUN) by the total number of the occurance of the parent(total number of VP as nonterminal) 
def qmlbinary():
	for rule, count in binaryrules.items():
		qml_binary[rule] = count / nonterminals[rule[0]]

# devide the occurance of the word under a rule by the total number of occurance of the word 
def qmlunary():
	for rule, count in wordscounts.items():
		qml_unary[rule] = decimal.Decimal(count /  nonterminals[rule[0]])

# implement CKY algoritem finding maximum pi for different nonterminals at defferent spans (example: pi(1, 8, VP))
# and saving them in different data structures
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
						if ptemp:
							bp[i, j, X], pi[i, j, X] = argmax(pitemp)				
						del pitemp[:]

						#bp[i, j, X], pi[i, j, X] = argmax([((X, nonterminal[0], nonterminal[1]), qml_binary.get((X, nonterminal[0], nonterminal[1]), 0) * pi.get((i, s, nonterminal[0]), 0) * pi.get((s + 1, j,nonterminal[1]), 0)) for nonterminal in nonterminals_collection[X] for s in range(i, j)])
					#bp[i, j, X], pi[i, j, X] = argmax([(X, qml_binary.get(X + " " + nonterminal[0] + " " + nonterminal[1]), 0) * pi.get((i, s, nonterminal[0]), 0) * pi.get((s + 1, j,nonterminal[1]), 0) for nonterminal in nonterminals_collection[X] for s in range(i, j)])

# input a list of all the rules parented by a specific nonterminal for all different spans
# out put the back pointer and maximum pi( back pointer consisting of parent children or child in case of terminal words)
def argmax(ls):
	return max(ls, key = lambda x : x[1])


count_words('../docs/parse_train.counts.out')
qmlbinary()
qmlunary()

# recursively go through backpointers starting at SBARQ
# and forming the parsed text
def buildparsetree(backpointer):
	if isinstance(backpointer[1], basestring):
		return [backpointer[0], backpointer[1]]
	else:	
		return [backpointer[0], buildparsetree(bp[backpointer[1]]),buildparsetree(bp[backpointer[2]])] 

# open the file to be parsed(parse_dev.dat), run CKY to populate the bp dict(dictionary of backpointers)
# and pi and then build the parsed text to write it to the new file (parse_test.dat)
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

outfile = '../docs/parse_test.out' 
parsefile('../docs/parse_dev.dat', bp)

	
