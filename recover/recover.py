#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn import tree
from zh_segment import *
import random

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
    predict_item(clf1, clf2, clf3, clf4)
    # print clf1.predict(item_feature((39600)))

def predict_item2(clf1, clf2, clf3, clf4):
    model_list = [clf1, clf2, clf3, clf4]
    raw_data = pd.read_excel("Predicting2.xlsx", 0).values.tolist()

    # step 1, make error tag
    error_tag = [[0 for i in range(4)] for j in range(200)]
    for i in range(200): # for each row
        for j in range(4):   # for each column
            if model_list[j].predict(item_feature(raw_data[i][j]))[0] == 1:
                error_tag[i][j] = 1

    # step 2, collect the error cell into the error knowledge base
    error_knowledge_base = [[raw_data[i][j] for j in range(4) if error_tag[i][j] == 1] for i in range(200)]
    #TODO here need to segment_phrase(raw_data[i][j]) in the future

    # step 3, recover from the error knowledge base
    for i in range(200):  # for each row
        for j in range(4): # for each column
            if error_tag[i][j] == 1:
                raw_data[i][j] = get_recover_data(model_list[j], error_knowledge_base[i])
                error_knowledge_base.pop(raw_data[i][j])  # remove the data from knowledge base


def get_recover_data(model, knowledge_base):
    candidates = []
    for phrase in knowledge_base:
        if model.predict(phrase)[0] == 0:
            candidates.append(phrase)
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        return None
    else:
        # TODO change to more respect method to choose from the candidate
        random.choice(candidates)






def predict_item(clf1, clf2, clf3, clf4):
    data_frame = pd.read_excel("Predicting2.xlsx", 0)
    column1 = list(data_frame['funded_amnt_inv'])
    column2 = list(data_frame['emp_title'])
    column3 = list(data_frame['addr_state'])
    column4 = list(data_frame['total_acc'])

    error = [[0 for i in range(4)] for j in range(200)]

    error1 = []
    error2 = []
    error3 = []
    error4 = []
    #针对第一列判断
    for item1 in column1:
        # print clf1.predict(item_feature(item1))
        error1.append(int(clf1.predict(item_feature((item1)))))
    for item2 in column2:
        error2.append(int(clf2.predict(item_feature((item2)))))
    for item3 in column3:
        error3.append(int(clf3.predict(item_feature((item3)))))
    for item4 in column4:
        error4.append(int(clf4.predict(item_feature((item4)))))
    for i in range(200):
        error[i][0] = error1[i]
        error[i][1] = error2[i]
        error[i][2] = error3[i]
        error[i][3] = error4[i]
    # print error1
    # print error2
    # print error3
    # print error4
    print error
    words = []
    recordj = []

    for i in range(200):
        for j in range(4):
            if(error[i][j] == 1 ):
                recordj.append(j+1)
                words.append(data_frame.iloc[i, j])
        # print words
        # print recordj
    result = []
    for w in words:
         for j in recordj:
             if (j == 1):








        # words = []
        # recordj = []



# parse_excel("Training.xlsx")
pro = parse_file('probability.dic')
words_to_parse = '11996.241,24'

print segment_phrase("dept of corrections st. of ct.", pro, 0.000001)

# a = []
# a.append(1)
# a.append(2)
# a.append(3)
# print a
#
# print a.pop()
# print a

# print max(0.1,0.2,0.3,0.4)

######next 找出4个index里边交叉的，取出这些值，然后分词，然后填回去