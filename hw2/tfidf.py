import numpy as np
import json
import math

class TFIDF:
	def __init__(self, idf_path):
		self.idf = json.loads(open(idf_path, 'r', encoding = 'utf8').read())# idf
		'''
		idf = json.loads(open(idf_path, 'r', encoding='utf-8').read())# idf
		self.idf = []
		self.vocabulay = {}
		for v in idf:
			self.vocabulay[v] = len(self.vocabulay)
			self.idf.append(idf[v])
		'''

	def score(self, query, doc):
		words = query.split()
		doc_words = doc.split()

		q_tf = {}
		doc_tf = {}
		for w in words:
			if w in q_tf:
				q_tf[w] += 1
			else:
				q_tf[w] = 1

		for w in doc_words:
			if w in doc_tf:
				doc_tf[w] += 1
			else:
				doc_tf[w] = 1

		dot = 0
		for w in q_tf:
			if w in doc_tf:
				if w in self.idf:
					dot += (doc_tf[w] / len(doc_words)) * (q_tf[w] / len(words)) * self.idf[w] * self.idf[w]
				else:
					dot += (doc_tf[w] / len(doc_words)) * (q_tf[w] / len(words)) * 16


		q_l = 0
		for w in q_tf:
			if w in self.idf:
				q_l += (q_tf[w]/len(words)) * (q_tf[w]/len(words)) * self.idf[w] * self.idf[w]
			else:
				q_l += (q_tf[w]/len(words)) * (q_tf[w]/len(words)) * 16

		d_l = 0
		for w in doc_tf:
			if w in self.idf:
				d_l += (doc_tf[w] / len(doc_words)) * (doc_tf[w] / len(doc_words)) * self.idf[w] * self.idf[w]
			else:
				d_l += (doc_tf[w] / len(doc_words)) * (doc_tf[w] / len(doc_words)) * 16

		return dot / math.sqrt(q_l) / math.sqrt(d_l)

	def similarity(self, query, doces):
		# doc_vec = np.linalg.norm(self.transform(doces), axis = 1)
		# query_vec = np.linalg.norm(self.transform([query]), axis = 1)
		ans = np.zeros((len(doces)))
		for i in range(len(doces)):
			ans[i] = self.score(query, doces[i])

		return ans
