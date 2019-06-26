import json

path = '../../../hw2/ntcir14_test_doc.json'
def average_len():
	fin = open(path, 'r')
	c = 0
	total = 0
	for line in fin:
		data = json.loads(line)
		total += len(data['content_seg'].split())
		c += 1
	return total/c

if __name__ == '__main__':
	print(average_len())