import json

term_path = '../../term_idf.txt'
term_file = open(term_path, 'r', encoding = 'utf-8')
term_dict = {}
line = term_file.readline()
while line:
    segments = line.split('\t')
    # print(segments)
    term = segments[0]
    freq = float(segments[1])
    term_dict[term] = freq
    line = term_file.readline()
term_file.close()
term_keys_prev = term_dict.keys()

term_dict_new = {}

doc_path = '../../ntcir14_test_doc.json'
doc = open(doc_path, 'r', encoding='utf-8')
line = doc.readline()
count = 0
while line:
    doc_dict = json.loads(doc.readline())
    #dict_keys(['content', 'title_seg', 'content_seg', 'uid', 'title'])
    doc_contents = (doc_dict['content_seg']).split(' ')
    doc_title = (doc_dict['title_seg']).split(' ')
    for content in doc_contents:
        if content in term_keys_prev:
            term_dict_new[content] = term_dict[content]
    for title in doc_title:
        if title in term_keys_prev:
            term_dict_new[title] = term_dict[title]
    count = count + 1
    if count % 1000 == 0:
        print(count)
    line = doc.readline()
doc.close()
print(len(term_dict_new.keys()))

term_new_path = '../../term_idf_new.json'
term_new = open(term_new_path, 'w', encoding = 'utf-8')
term_new.write(json.dumps(term_dict_new, ensure_ascii=False, indent=2))
term_new.close()