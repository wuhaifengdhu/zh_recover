#!/usr/bin/python
# -*- coding: utf-8 -*-


class FeatureExtractor(object):
    def __init__(self, column_list):
        self.data = column_list
        self.feature_list = [self._feature1, self._feature2, self._feature3, self._feature4]

    def generate_features(self):
        return [self.__extract(element) for element in self.data]

    def _feature1(self, element):
        if self._is_pure_digital(element):
            return float(element)
        return -1

    def _feature2(self, element):
        if self._is_pure_digital(element):
            if float(element) <= 1000:
                return 1
            return 0
        return -1

    def _feature3(self, element):
        return 1 if self._is_pure_digital(element) else 0

    @staticmethod
    def _feature4(element):
        return len(str(element))

    @staticmethod
    def _is_pure_digital(element):
        try:
            float(element)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(element)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def __extract(self, element):
        return [feature(element) for feature in self.feature_list]


if __name__ == '__main__':
    test = ["wuhai", "123", 34343, 0]
    extractor = FeatureExtractor(test)
    print(extractor.generate_features())
