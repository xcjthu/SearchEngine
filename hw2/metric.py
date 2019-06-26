# coding=utf-8
import random
from pyNTCIREVAL import Labeler
from pyNTCIREVAL.metrics import nERR, QMeasure, MSnDCG, nDCG

label_range = 4

def data_process(y_pred, y_true):
    qrels = {}
    ranked_list = []
    c = list(zip(y_pred, y_true))
    random.shuffle(c)
    c = sorted(c, key=lambda x:x[0], reverse=True)
    for i in range(len(c)):
        qrels[i] = c[i][1]
        ranked_list.append(i)
    grades = range(1, label_range+1)

    labeler = Labeler(qrels)
    labeled_ranked_list = labeler.label(ranked_list)
    rel_level_num = len(grades)
    xrelnum = labeler.compute_per_level_doc_num(rel_level_num)
    return xrelnum, grades, labeled_ranked_list

def n_dcg(y_pred, y_true, k):
    xrelnum, grades, labeled_ranked_list = data_process(y_pred, y_true)
    metric = nDCG(xrelnum, grades, cutoff=k, logb=2)
    result = metric.compute(labeled_ranked_list)
    return result


def q_measure(y_pred, y_true, k, beta=1.0):
    xrelnum, grades, labeled_ranked_list = data_process(y_pred, y_true)
    metric = QMeasure(xrelnum, grades, beta, cutoff=k)
    result = metric.compute(labeled_ranked_list)
    return result


def n_err(y_pred, y_true, k):
    xrelnum, grades, labeled_ranked_list = data_process(y_pred, y_true)
    metric = nERR(xrelnum, grades, cutoff=k)
    result = metric.compute(labeled_ranked_list)
    return result

if __name__ == '__main__':
    label_range = 4  # 4级相关性标注（0，1，2，3）
    print (n_dcg([0, 1, 2, 3], [1, 2, 3, 0], k=3))  # y_pred: 预测的分数, y_true: 对应的relevance, k: cutoff
    print (q_measure([0, 1, 2, 3], [1, 2, 3, 0], k=3))
    print (n_err([0, 1, 2, 3], [1, 2, 3, 0], k=3))

'''
注意在每个query内部根据给出的文档列表计算以上评价指标，最后汇报在全部query上的平均值
'''