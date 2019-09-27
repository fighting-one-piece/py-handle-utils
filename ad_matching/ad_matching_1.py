# -*- coding:utf-8 -*-

import os
import sys
import enum
from maximum_matching_2 import MaximumMatching

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class AdministrativeDivisionMatching(object):

    def __init__(self):
        # 省、市、县、乡镇、村不同等级的数据初始化
        prefix = os.path.dirname(os.getcwd())
        self.provinces = []
        self.province_abbr_full = {}
        ad_1_file = os.path.join(prefix, 'static', 'ad', 'administrative_division_1.dic')
        AdministrativeDivisionMatching.init_ad_params(ad_1_file, self.provinces, self.province_abbr_full)
        self.cities = []
        self.city_abbr_full = {}
        ad_2_file = os.path.join(prefix, 'static', 'ad', 'administrative_division_2.dic')
        AdministrativeDivisionMatching.init_ad_params(ad_2_file, self.cities, self.city_abbr_full)
        self.counties = []
        self.county_abbr_full = {}
        ad_3_file = os.path.join(prefix, 'static', 'ad', 'administrative_division_3.dic')
        AdministrativeDivisionMatching.init_ad_params(ad_3_file, self.counties, self.county_abbr_full)
        self.towns = []
        self.town_abbr_full = {}
        ad_4_file = os.path.join(prefix, 'static', 'ad', 'administrative_division_4.dic')
        AdministrativeDivisionMatching.init_ad_params(ad_4_file, self.towns, self.town_abbr_full)
        self.villages = []
        self.village_abbr_full = {}
        ad_5_file = os.path.join(prefix, 'static', 'ad', 'administrative_division_5.dic')
        AdministrativeDivisionMatching.init_ad_params(ad_5_file, self.villages, self.village_abbr_full)
        # 行政区划树数据初始化
        self.ads = {}
        ad_file = os.path.join(prefix, 'static', 'ad', 'administrative_division.dic')
        with open(ad_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split(',')
                self.ads[unicode(words[0])] = unicode(words[1])
                self.ads[unicode(words[1])] = unicode(words[2])
                self.ads[unicode(words[2])] = unicode(words[3])
                if len(words) == 5:
                    self.ads[unicode(words[3])] = unicode(words[4])
        # 最大匹配分词初始化
        self.maximum_matching = MaximumMatching(8)

    @staticmethod
    def init_ad_params(dic_path, ad_array, ad_dict):
        with open(dic_path, 'r') as df:
            lines = df.readlines()
            for i in range(0, len(lines), 2):
                abbr = unicode(lines[i].strip())
                full = unicode(lines[i + 1].strip())
                ad_array.append(abbr)
                ad_array.append(full)
                ad_dict[abbr] = full

    # 行政区划缺失补全
    def ad_missing_completion(self, address):
        matching = Matching()
        words = self.maximum_matching.two_way_maximum_matching(address)
        print ' '.join(words)
        for word in words:
            if word in self.provinces:
                if word in self.province_abbr_full.keys():
                    word = self.province_abbr_full[word]
                matching.add_word(MatchingType.PROVINCE, word)
            elif word in self.cities:
                if word in self.city_abbr_full.keys():
                    word = self.city_abbr_full[word]
                matching.add_word(MatchingType.CITY, word)
            elif word in self.counties:
                if word in self.county_abbr_full.keys():
                    word = self.county_abbr_full[word]
                matching.add_word(MatchingType.COUNTY, word)
            elif word in self.towns:
                if word in self.town_abbr_full.keys():
                    word = self.town_abbr_full[word]
                matching.add_word(MatchingType.TOWN, word)
            elif word in self.villages:
                if word in self.village_abbr_full.keys():
                    word = self.village_abbr_full[word]
                matching.add_word(MatchingType.VILLAGE, word)
        matcher_items = matching.matcher_items
        if matcher_items is None:
            return
        # sorted_items = sorted(matcher_items.items(), key=lambda item: item[0], reverse=True)
        full_result = []
        keys = matcher_items.keys()
        keys.sort(reverse=True)
        level = keys[0]
        while level != 0:
            if level in keys:
                result = matcher_items[level][0]
            else:
                pre_level = level + 1
                result = self.ads[matcher_items[pre_level][0]]
                matcher_items[level] = [result]
            level -= 1
            full_result.append(result)
        full_result.reverse()
        return full_result


class MatchingType(enum.Enum):
    PROVINCE = 1
    CITY = 2
    COUNTY = 3
    TOWN = 4
    VILLAGE = 5


class Matching(object):

    def __init__(self):
        self.matcher_items = {}

    def add_word(self, matching_type, word):
        matching_type_value = matching_type.value
        if matching_type_value in self.matcher_items.keys():
            words = self.matcher_items[matching_type_value]
            words.append(word)
        else:
            self.matcher_items[matching_type_value] = [word]


if __name__ == '__main__':
    ad_matching = AdministrativeDivisionMatching()
    print ' '.join(ad_matching.ad_missing_completion(u'北京市'))
    print ' '.join(ad_matching.ad_missing_completion(u'成都市'))
    print ' '.join(ad_matching.ad_missing_completion(u'资中县'))
    print ' '.join(ad_matching.ad_missing_completion(u'鳌头镇'))
    print ' '.join(ad_matching.ad_missing_completion(u'上方山村'))
    print ' '.join(ad_matching.ad_missing_completion(u'四川省资中县'))
    print ' '.join(ad_matching.ad_missing_completion(u'莱芜市上方山村'))
