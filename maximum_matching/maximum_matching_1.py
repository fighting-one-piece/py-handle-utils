# -*- coding:utf-8 -*-

import os
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class MaximumMatching(object):

    def __init__(self, window_size):
        self.window_size = window_size
        self.dicts = []
        dic_file = os.path.join(os.path.dirname(os.getcwd()), 'static', 'dic', 'main.dic')
        with open(dic_file, 'r') as df:
            lines = df.readlines()
            for line in lines:
                self.dicts.append(line.strip())

    # 正向最大匹配
    def forward_maximum_matching(self, input_word):
        result = []
        while True:
            left_word, right_word = (input_word, "") if self.window_size > len(input_word) \
                else (input_word[0:self.window_size], input_word[self.window_size:])
            left_match_word, right_seg_word = self.get_forward_matching_word(left_word)
            result.append(left_match_word)
            input_word = right_seg_word + right_word
            if input_word == "":
                break
        return result

    # 逆向最大匹配
    def reverse_maximum_matching(self, input_word):
        result = []
        while True:
            left_word, right_word = ("", input_word) if self.window_size > len(input_word) \
                else (input_word[0:len(input_word)-self.window_size], input_word[len(input_word)-self.window_size:])
            left_seg_word, right_match_word = self.get_reverse_matching_word(right_word)
            result.append(right_match_word)
            input_word = left_word + left_seg_word
            if input_word == "":
                break
        result.reverse()
        return result

    # 双向最大匹配
    # 比较正向最大匹配和逆向最大匹配结果
    # 如果分词数量结果不同:那么取分词数量较少的那个
    # 如果分词数量结果相同:分词结果相同可以返回任何一个 分词结果不同返回单字数比较少的那个
    def two_way_maximum_matching(self, input_word):
        forword_result = self.forward_maximum_matching(input_word)
        reverse_result = self.reverse_maximum_matching(input_word)
        forword_result_len = len(forword_result)
        reverse_result_len = len(reverse_result)
        if forword_result_len != reverse_result_len:
            return forword_result if forword_result_len < reverse_result_len else reverse_result
        else:
            fr_single_word_count = 0
            for result in forword_result:
                if len(result) == 1:
                    fr_single_word_count = fr_single_word_count + 1
            rr_single_word_count = 0
            for result in reverse_result:
                if len(result) == 1:
                    rr_single_word_count = rr_single_word_count + 1
            return forword_result if fr_single_word_count <= rr_single_word_count else reverse_result

    def get_forward_matching_word(self, input_word):
        for i in range(len(input_word), 1, -1):
            prefix = input_word[0:i]
            if prefix in self.dicts:
                return prefix, input_word[i:]
        return input_word[0:1], input_word[1:]

    def get_reverse_matching_word(self, input_word):
        for i in range(0, len(input_word)):
            suffix = input_word[i:]
            if suffix in self.dicts:
                return input_word[0:i], suffix
        return input_word[0:-1], input_word[-1]


def do_maximum_matching(maximum_matching_obj, input_word):
    print '----------forward----------'
    f_results = maximum_matching_obj.forward_maximum_matching(input_word)
    for f_result in f_results:
        print f_result
    print '----------reverse----------'
    r_results = maximum_matching_obj.reverse_maximum_matching(input_word)
    for r_result in r_results:
        print r_result
    print '----------two-way----------'
    tw_results = maximum_matching_obj.two_way_maximum_matching(input_word)
    for tw_result in tw_results:
        print tw_result


if __name__ == '__main__':
    maximum_matching = MaximumMatching(4)
    do_maximum_matching(maximum_matching, u'中国移动联合华为完成独立5G网络下视频通话')
    do_maximum_matching(maximum_matching, u'大龄程序员该如何规划未来的人生')
    do_maximum_matching(maximum_matching, u'民族从此站起来了')