#coding: utf-8
import pandas as pd
from sklearn import tree
import math
import unicodedata
import numpy
import random
from zh_segment import *
import os
#######################
# 1.若为数字， 为数字的值， 若为文字，置为-1
# 2.是否大于1000，大于为0，小于为1，若不为数字为-1
# 3.是否为数字， 0 代表是， 1代表不是
# 4.长度，数字就看位数

#判断是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_lable(i):  #i represent the lable number
    data_frame = pd.read_excel("lable.xlsx", 0)
    if(i == 1):
        return list(data_frame['funded_amnt_inv'])
    elif(i == 2):
        return  list(data_frame['emp_title'])
    elif(i == 3):
        return list(data_frame['addr_state'])
    elif(i == 4):
        return list(data_frame['total_acc'])
    else:
        return -1


# input a nnumber or string , get its feature
def item_feature(item):
    temp = []
    value = -1
    range = -1 # 1 represent less than 1000, 0 represent more than 1000
    isnumber = -1
    length = -1
    try:
        item = str(item).lower()
    except UnicodeEncodeError:
        item = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore')

    length = len(str(item))

    if (item.__eq__("nan")):
        # print "find nan"
        value = -1
        isnumber = 1
        range = -1
        length = 0
    else:
        if (is_number(item) == True):
            isnumber = 0
            value = item
            if (item > 1000):
                range = 0
            else:
                range = 1
        else:
            isnumber = 1
            value = -1
            range = -1
    temp.append(isnumber)
    temp.append(value)
    temp.append(range)
    temp.append(length)
    return temp

# get the feature for a attribute
def generate_feature(attribute):
    feature = []

    for item in attribute:
        temp = item_feature(item)
        feature.append(temp)
        # print value
    return feature

def make_decisiontree(X, Y):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    return clf
    # print clf

def parse_excel(excel_file_name):
    data_frame = pd.read_excel(excel_file_name, 0)

    column1 = list(data_frame['funded_amnt_inv'])
    column2 = list(data_frame['emp_title'])
    column3 = list(data_frame['addr_state'])
    column4 = list(data_frame['total_acc'])

    # 获取每一列的label
    Y1 = get_lable(1)
    Y2 = get_lable(2)
    Y3 = get_lable(3)
    Y4 = get_lable(4)

    X1 = generate_feature(column1)
    X2 = generate_feature(column2)
    X3 = generate_feature(column3)
    X4 = generate_feature(column4)

    # print X1
    # print Y1
    clf1 = make_decisiontree(X1,Y1)
    clf2 = make_decisiontree(X2, Y2)
    clf3 = make_decisiontree(X3, Y3)
    clf4 = make_decisiontree(X4, Y4)
    #print clf.predict([0,39600,0,5])
    predict_item2(clf1, clf2, clf3, clf4)
    # print clf1.predict(item_feature((39600)))


def write_records_to_excel(excel_writer, dic_data, sheet_name):
    data_frame = pd.DataFrame(dic_data)
    data_frame.to_excel(excel_writer, sheet_name=sheet_name)


def predict_item2(clf1, clf2, clf3, clf4):
    model_list = [clf1, clf2, clf3, clf4]
    raw_data = pd.read_excel("Predicting2.xlsx", 0).values.tolist()

    # step 1, make error tag
    error_tag = [[0 for i in range(4)] for j in range(200)]
    for i in range(200):  # for each row
        for j in range(4):  # for each column
            if model_list[j].predict(item_feature(raw_data[i][j]))[0] == 1:
                error_tag[i][j] = 1

    # step 2, collect the error cell into the error knowledge base
    probability_dic = parse_file('probability.dic')
    flatten = lambda l: [item for sublist in l for item in sublist if len(item) > 0]
    seg = lambda x: segment_phrase(str(x), probability_dic, 0.000001)
    error_knowledge_base = [flatten(map(seg, [raw_data[i][j] for j in range(4) if error_tag[i][j] == 1]))
                            for i in range(200)]

    print error_knowledge_base

    for i in range(200):
        for j in range(4):
            if error_tag[i][j] == 1:
                best_candidate = get_recover_data(model_list[j], error_knowledge_base[i])
                if best_candidate is not None:
                    raw_data[i][j] = best_candidate
                    error_knowledge_base[i].remove(raw_data[i][j])  # remove the data from knowledge base
                else:
                    print "Can not find suitable error test for (%i, %i)" % (i, j)

    # step 3, write data to output excel
    out_put_excel = os.path.join(os.getcwd(), 'output', 'recover.xls')
    writer = pd.ExcelWriter(out_put_excel, engine='xlsxwriter')
    write_records_to_excel(writer, raw_data, "raw_data")
    writer.close()


def get_recover_data(model, knowledge_base):
    candidates = []
    for phrase in knowledge_base:
        if model.predict(item_feature(phrase)) == 0:
            candidates.append(phrase)
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        return None
    else:
        # TODO change to more respect method to choose from the candidate
        random.choice(candidates)

parse_excel("Training.xlsx")
# pro = parse_file('probability.dic')
# words_to_parse = '11996.241,24'
#
# print segment_phrase("dept of corrections st. of ct.", pro, 0.000001)
