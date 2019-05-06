# implement query likelihood model with the simplest language model
import json
import numpy as np


class Query_Likelihood:
	def __init__(self, idf_path):
		# use idf to replace the language model in whole collection
		self.idf = json.loads(open(idf_path, 'r', encoding = 'utf8').read())
		self.lamb = 0.1

	def score(self, query, doc):
		words = doc.split()
		qwords = query.split()
		cw = {}
		
		for w in set(words):
			cw[w] = 0

		for w in words:
			if w in cw.keys():
				cw[w] += 1

		ans = 0
		for w in query:
			if w not in cw.keys():
				cw[w] = 0
			if w in self.idf:
				# print(w)
				# print(self.idf[w])
				# print(cw[w])
				p = (1 - self.lamb) * cw[w] / len(words) + self.lamb / self.idf[w]
			else:
				p = self.lamb / 4
			ans += p

		return ans

	def similarity(self, query, doces):
		ans = np.zeros((len(doces)))
		for i in range(len(doces)):
			ans[i] = self.score(query, doces[i])
		return ans
