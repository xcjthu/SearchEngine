import json
from metric import n_dcg, q_measure, n_err
import numpy as np

pred_filepath = '../../query_likelihood.json'
f = open(pred_filepath, 'r', encoding = 'utf8')
pred_dict = json.loads(f.read())
f.close()

print('read pred label finished')

true_dict = {}
true_filepath = '../../ntcir14_test_label.txt'
f = open(true_filepath, 'r', encoding = 'utf8')
for i in range(1, 81):
    true_dict[str(i)] = {}
line = f.readline()
line = f.readline()
while line:
    segments = line.split('\t')
    qid = segments[0]
    uid = segments[1]
    relevance = int(segments[2])
    true_dict[qid][uid] = relevance
    line = f.readline()
f.close()

print('read true label finished')


output_filepath = 'result_query_likelihood.txt'
f = open(output_filepath, 'w', encoding = 'utf8')

ks = [5, 10, 20]

for k in ks:
    n_dcg_list = []
    n_err_list = []
    q_measure_list = []
    for query in pred_dict.keys():
        print('query id:', query)
        pred_list = []
        true_list = []
        pred_dict_query = pred_dict[query]
        true_dict_query = true_dict[str(int(query))]
        for doc_pair in pred_dict_query:
            uid = doc_pair[0]
            pred_relevance = doc_pair[1]
            true_relevance = 0
            if uid in true_dict_query.keys():
                true_relevance = true_dict_query[uid]
            pred_list.append(pred_relevance)
            true_list.append(true_relevance)
        if np.max(true_list) == 0:
            n_dcg_list.append(0)
            n_err_list.append(0)
            q_measure_list.append(0)
        else:
            n_dcg_list.append(n_dcg(pred_list, true_list, k = k))
            n_err_list.append(n_err(pred_list, true_list, k = k))
            q_measure_list.append(q_measure(pred_list, true_list, k = k))
        print(n_dcg_list[-1], n_err_list[-1], q_measure_list[-1])
        
    print(np.mean(n_dcg_list), np.mean(n_err_list), np.mean(q_measure_list))
    f.write('k: '+str(k)+', n_dcg: '+str(np.mean(n_dcg_list))+', n_err: '+str(np.mean(n_err_list))+', q_measure: '+str(np.mean(q_measure_list))+'\n')

# label_range = 4  # 4级相关性标注（0，1，2，3）
# print(n_dcg([0, 1, 2, 3], [1, 2, 3, 0], k=3))  # y_pred: 预测的分数, y_true: 对应的relevance, k: cutoff
# print(q_measure([0, 1, 2, 3], [1, 2, 3, 0], k=3))
# print(n_err([0, 1, 2, 3], [1, 2, 3, 0], k=3))

# f.write('mean: '+str(np.mean(n_dcg_list))+'\n')
# for i in range(len(n_dcg_list)):
#     f.write(str(i+1)+' '+str(n_dcg_list[i])+'\n')
f.close()