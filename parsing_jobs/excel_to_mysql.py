#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymysql
import openpyxl


print('connect to MySQL db')
db = pymysql.connect("localhost", "lianne", "1q2w3e!Q@W#E", "BAIDUINDEX", charset='utf8')
cursor = db.cursor()
# cursor.execute("CREATE TABLE trends(id INT, keyword VARCHAR(100), area VARCHAR(50), time DATE, search_index INT, pc_index INT, phone_index INT)")
# cursor.execute("CREATE TABLE demand_map(id INT, keyword VARCHAR(100), time DATE, relate_keyword VARCHAR(100), zhonghexiangguangdu INT, quxiangxiangguangdu INT, laiyuanxiangguandu INT, search_index INT, rise_index INT)")
# cursor.execute("CREATE TABLE information_index(id INT, keyword VARCHAR(100), time DATE, information_index INT)")
# cursor.execute("DROP TABLE renqunhuaxiang")
# cursor.execute("CREATE TABLE renqunhuaxiang(id INT, keyword VARCHAR(100), start_time INT, end_time INT, type VARCHAR(50), section VARCHAR(50), percent INT)")


wb = openpyxl.load_workbook("就业 高考.xlsx")
# sheet = wb['趋势']
# print('transfer 趋势 to mysql')
# n = 0
# for row in sheet.rows:
#     if n == 0:
#         n = n + 1
#         continue
#     insert_sql = 'insert into trends (id, keyword, area, time, search_index, pc_index, phone_index) values (%s, %s, %s, %s, %s, %s, %s)'
#     cursor.execute(insert_sql,(n,row[1].value,row[2].value,row[3].value,row[4].value,row[5].value,row[6].value))
#     db.commit()
#     n = n + 1


# print('transfer 需求图谱 to mysql')
# sheet = wb['需求图谱']
# n = 0
# for row in sheet.rows:
#     if n == 0:
#         n = n + 1
#         continue
#     insert_sql = "INSERT INTO demand_map(id, keyword, time, relate_keyword, zhonghexiangguangdu, quxiangxiangguangdu, laiyuanxiangguandu, search_index, rise_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     cursor.execute(insert_sql,(n,row[0].value,row[1].value,row[2].value,row[3].value,row[4].value,row[5].value,row[6].value,row[7].value))
#     db.commit()
#     n = n + 1
#
#
# print('transfer 资讯指数 to mysql')
sheet = wb['资讯指数']
n = 0
for row in sheet.rows:
    if n == 0:
        n = n + 1
        continue
    insert_sql = "INSERT INTO information_index(id, keyword, time, information_index) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_sql,(n,row[1].value,row[2].value,row[3].value))
    db.commit()
    n = n + 1


print('transfer 人群画像 to mysql')
sheet = wb['人群画像']
n = 0
for row in sheet.rows:
    if n == 0:
        n = n + 1
        continue
    insert_sql = "INSERT INTO renqunhuaxiang(id, keyword, start_time, end_time, type, section, percent) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_sql,(n,row[0].value,row[1].value,row[2].value,row[3].value,row[4].value,row[5].value))
    db.commit()
    n = n + 1

db.close()
