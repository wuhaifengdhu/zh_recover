#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from feature_extractor import FeatureExtractor


class LabelHelper(object):
    def __init__(self, column_features):
        self.data = column_features

    def get_label(self):
        k_mean = KMeans(n_clusters=2)
        k_mean.fit(self.data)
        if sum(k_mean.labels_) > len(k_mean.labels_) / 2.0:  # Guarantee: 0 for common, 1 for error
            return [1 - label for label in k_mean.labels_]
        return k_mean.labels_

if __name__ == '__main__':
    # 0 for most common, 1 for less common label
    raw_data = [2, 2, 2, 2, 4, 2, 2, 3, 2, 2]
    _label = LabelHelper(FeatureExtractor(raw_data).generate_features())
    print(_label.get_label())
