import numpy as np
import json

class TFIDF:
	def __init__(self, idf_path):
		idf = json.loads(open(idf_path, 'r', encoding='utf-8').read())# idf
		self.idf = []
		self.vocabulay = {}
		for v in idf:
			self.vocabulay[v] = len(self.vocabulay)
			self.idf.append(idf[v])

	def transform(self, doces):
		ans = np.zeros((len(doces), len(self.idf)))
		for i in range(len(doces)):
			doc = doces[i]
			words = doc.split()
			for w in words:
				if w in self.idf:
					ans[i][self.vocabulay[w]] += self.idf[self.vocabulay[w]]/len(words)
		return ans


	def similarity(self, query, doces):
		doc_vec = np.linalg.norm(self.transform(doces), axis = 1)
		query_vec = np.linalg.norm(self.transform([query]), axis = 1)

		score = query_vec * np.transpose(doc_vec)
		return score
