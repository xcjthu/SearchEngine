import json
import numpy as np

class BM25:
	def __init__(self, idf_path, k1 = 2, b = 0.75):
		self.idf = json.loads(open(idf_path, 'r', encoding = 'utf8').read())# idf
		self.k1 = k1
		# self.k2 = k2
		self.b = b

		self.average_len = 1260.7

	def score(self, query, doc):
		words = query.split()
		doc_words = doc.split()

		K = self.k1 * (1 - self.b + self.b * len(doc_words) / self.average_len)

		words = set(words)
		words_num = {}
		for w in words:
			words_num[w] = 0

		for w in doc_words:
			if w in words_num:
				words_num[w] += 1

		ans = 0
		for w in set(words):
			if not w in self.idf:
				ans += 3 * words_num[w] * (self.k1 + 1) / (words_num[w] + K)
				continue
			ans += self.idf[w] * words_num[w] * (self.k1 + 1) / (words_num[w] + K)
		return ans

	def similarity(self, query, doces):
		ans = np.zeros((len(doces)))
		for i in range(len(doces)):
			ans[i] = self.score(query, doces[i])
		return ans