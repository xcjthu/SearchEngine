import json

source_file_path = '../../query_likelihood.json'

f = open(source_file_path, 'r', encoding = 'utf8')
source_dict = json.loads(f.read())
f.close()

result_file_path = '../../query_likelihood.txt'
g = open(result_file_path, 'w', encoding = 'utf8')

queries = source_dict.keys()
print(queries)
for query in queries:
    print(query)
    reslen = len(source_dict[query])
    for rank in range(reslen):
        doc_pair = source_dict[query][rank]
        g.write(query+' Q0 '+doc_pair[0]+' '+str(rank+1)+' '+str(doc_pair[1])+' query_likelihood\n')
g.close()
