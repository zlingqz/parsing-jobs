#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pandas as pd
import pymysql
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

def group_and_sort(dafr=None, order=''):
    grouped = dafr.groupby(order).sum(axis=1)
    sorted = grouped.sort_values(by='num', ascending=False)
    return sorted#.iloc[: , 2]


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, "%s" % float(height))


def main():
    db = pymysql.connect("localhost", "root", "root", "PARSING_JOBS", charset='utf8')
    df = pd.read_sql("SELECT * from job_statistics", db)
    print('\n\n************    city_sum_sorted    ************')
    city_sum_sorted = group_and_sort(dafr=df, order='job_location')
    print(city_sum_sorted.shape)
    print(city_sum_sorted.head(20))
    print(type(city_sum_sorted.head(20)))
    zhfont1 = FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
    rect = plt.bar(city_sum_sorted.head(20).index.values.tolist(), city_sum_sorted.head(20).values[:, 2].tolist(), width=0.5, align="center", alpha=0.4, color='b')
    plt.xlabel('城市', fontproperties=zhfont1)
    plt.ylabel('招聘数', fontproperties=zhfont1)
    plt.xticks(city_sum_sorted.head(20).index.values.tolist(), city_sum_sorted.head(20).index.values.tolist(), fontproperties=zhfont1)
    # autolabel(rect)
    plt.show()
    print(city_sum_sorted.head(20).index.values.tolist())
    print(type(city_sum_sorted.head(20).index.values.tolist()))
    print(city_sum_sorted.head(20).values[:, 2].tolist())
    print(type(city_sum_sorted.head(20).values[:, 2].tolist()))
    print(city_sum_sorted.columns.values)
    # print('\n\n************    job_sum_sorted    ************')
    # job_sum_sorted = group_and_sort(dafr=df, order='job')
    # print(job_sum_sorted.head(20))
    # print('\n\n************    job_field_sum_sorted    ************')
    # job_field_sum_sorted = group_and_sort(dafr=df, order='job_field')
    # print(job_field_sum_sorted.head(20))


if __name__ == '__main__':
    main()
# city_sum = df.groupby('job_location').sum(axis=1)
# print(city_sum.head(5))
# print(city_sum.shape)
# print('\n\n************    city_sum_sorted    ************\n\n\n')
# city_sum_sorted = city_sum.sort_values(by='num', ascending=False)
# print(city_sum_sorted.head(20))

# job_sum = df.groupby('job').sum(axis=1)
# print(job_sum.head(5))
# print(job_sum.shape)
# print('\n\n************    job_sum_sorted    ************\n\n\n')
# job_sum_sorted = job_sum.sort_values(by='num', ascending=False)
# print(job_sum_sorted.head(20))
