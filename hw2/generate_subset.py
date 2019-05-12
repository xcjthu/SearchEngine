import json

source_file_path = '../../query_likelihood.txt'

f = open(source_file_path, 'r', encoding = 'utf8')

result_file_path = '../../subset_query_likelihood.txt'
g = open(result_file_path, 'w', encoding = 'utf8')

line = f.readline()
while line:
    segment = line.split(' ')
    if int(segment[3]) <= 20:
        g.write(line)
    line = f.readline()

f.close()
g.close()
