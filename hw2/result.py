from tfidf import TFIDF
from bm25 import BM25
from query_likelihood import Query_Likelihood
import json

path = '../../term_idf_new_new.json'
tfidf = TFIDF(path)

query_filepath = '../../ntcir14_test_query.json'
query_file = open(query_filepath, 'r', encoding='utf-8')
queries = []
query_line = query_file.readline()
while query_line:
	query_json = json.loads(query_line)
	queries.append([query_json['query_seg'], query_json['qid']])
	query_line = query_file.readline()
	# break
query_file.close()
# print(queries)

print('read query finished')
count = 0

doc_filepath = '../../ntcir14_test_doc.json'
doc_file = open(doc_filepath, 'r', encoding = 'utf-8')
line = doc_file.readline()
docs_content = []
docs_id = []
while line:
	doc_json = json.loads(line)
	doc_contents = (doc_json['content_seg'])
	doc_title = (doc_json['title_seg'])
	doc_id = doc_json['uid']
	docs_content.append(doc_contents+' '+doc_title)
	docs_id.append(doc_id)
	# count = count + 1
	# if count == 250:
	# 	break
	line = doc_file.readline()
doc_file.close()
# print(docs_id)
tot_scores = {}
docs_len = len(docs_content)

print('read doc finished')

PACK = 1000
round = int(docs_len / PACK)
print(round)

for query_pair in queries:
	query = query_pair[0]
	query_id = query_pair[1]
	scores = {}
	for i in range(round):
		print(query_id, i)
		score = tfidf.similarity(query, docs_content[i*PACK: (i+1)*PACK])
		for j in range(len(score)):
			scores[docs_id[i*PACK + j]] = score[j]
	score = tfidf.similarity(query, docs_content[round*PACK:])
	for j in range(len(score)):
		scores[docs_id[round*PACK + j]] = score[j]
	tot_scores[query_id] = sorted(scores.items(), key=lambda item:item[1], reverse=True)

output_path = '../../tfidf.json'
output_file = open(output_path, 'w', encoding='utf-8')
output_file.write(json.dumps(tot_scores, ensure_ascii=False, indent=2))
output_file.close()