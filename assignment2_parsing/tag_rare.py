import json
words = {}
rares = []
temp_words = {}

def count_words():
	with open('../docs/cfg_vert.counts') as f:
		for line in f:
			word_group = line.split()
			if(word_group[1] == 'UNARYRULE'):
				temp_words[word_group[3]] = word_group[0]
				words[word_group[3]] = words.get(word_group[3], 0) + int(word_group[0])

def find_rares():
	for word, count in words.items():
		if (count < 5):
			rares.append(word)
			rares.append(count)

def replace_leaves(*branch):
	if (isinstance(branch[0], basestring)): 
		if (rares.count(branch[0]) > 0):
			branch[2][1] = "_RARE_" 
	else:
		replace_leaves(branch[0][1], 1, branch[0])
		if (len(branch[0]) > 2):
			replace_leaves(branch[0][2], 2, branch[0])
	return branch

def traverse_file(infile, outfile):
	new_file = open(outfile, 'w')
	for line in infile:
		new_tree = json.loads(line)
		replace_leaves(new_tree)	
		jasondata = json.dumps(new_tree, outfile)
		new_file.write("%s\n"% jasondata)

	new_file.close()

count_words()
find_rares()
all_trees = open("../docs/parse_train_vert.dat")
outfile = "../docs/parse_train_vert1.dat"

traverse_file(all_trees,outfile)

