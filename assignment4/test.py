class FEATURES:
	def __init__(self, choice):
		self.choice = choice
		self.f = {}
	def getgs(self, u, word):
		wordlen = len(word)
		print 'word:::', word
		if self.choice == 'suffix':
			for j in range(1, 4):
				if wordlen - j > 0:
					print j
					suffix = word[wordlen - j:]
					print suffix
					if ('SUFF:', suffix, ':', j, ':', u) in self.f:
						self.f[('SUFF:', suffix, ':', j, ':', u)] += 1
					else:
						self.f[('SUFF:', suffix, ':', j, ':', u)] = 1
			return [self.f]

features = FEATURES('suffix')

class CAL_GLOB:
	def calculate_global_f(self, tags, sentence, n):
		gs = {}
		for i in range(0, n):
			g = features.getgs(tags[i], sentence[i])
			for feature in g[0]:
				if feature in gs:
					gs[feature] += 1
				else:
					gs[feature] = 1
			#print 'gs::', gs
		return gs 
	
	def equal(self, y, z):
		for i in range(0, len(y)):
			if y[i] != z[i]:
				return False	
		return True

cal_glob = CAL_GLOB()
cal_glob.calculate_global_f(['O', 'I-GENE', 'O', 'I-GENE', 'O', 'I-GENE'], ['Pharmacologic', 'aspects', 'of', 'neonatal', 'hyperbilirubinemia', '.'], 6)
cal_glob.calculate_global_f(['O', 'I-GENE', 'O', 'I-GENE', 'O', 'I-GENE'], ['Pharmacologic', 'aspects', 'of', 'neonatal', 'hyperbilirubinemia', '.'], 6)

print features.f
