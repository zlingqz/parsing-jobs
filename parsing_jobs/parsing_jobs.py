#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from atexit import register
from random import uniform
from time import sleep, ctime, time
from threading import Thread, Lock


from urllib.request import urlopen, build_opener, HTTPCookieProcessor, Request, ProxyHandler, install_opener
from urllib.parse import quote, unquote
import re
import http.cookiejar
import lxml.html
import lxml.cssselect
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pymysql
from bs4 import BeautifulSoup
# from mongo_queue import MongoQueue



URL = 'http://sou.zhaopin.com'   #智联招聘https://www.zhaopin.com
discard_link = ['http://article.zhaopin.com/', 'http://ceping.zhaopin.com/', '#', 'http://edu.zhaopin.com/',
                'http://www.zhaopin.com/', 'http://special.zhaopin.com/sh/2009/aboutus/about.html',
                'http://www.zhaopin.com/sitemap.html', 'http://special.zhaopin.com/sh/2009/aboutus/law.html',
                'http://special.zhaopin.com/sh/2009/aboutus/secrecy.html', 'http://special.zhaopin.com/sh/2009/aboutus/contact.html',
                'http://jobseeker.zhaopin.com/zhaopin/faq/question.html', 'http://www.miibeian.gov.cn',
                'http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010502002133',
                'http://sou.zhaopin.com/', 'http://passport.zhaopin.com/account/register',
                'https://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2&ps=1', 'http://www.zhaopin.com/citymap.html',
                'http://images.zhaopin.com/2012/other/mobile/mobile.html', 'http://www.zhaopin.com/mobile/',
                'http://my.zhaopin.com/', 'http://xiaoyuan.zhaopin.com/', 'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2&ps=1',
                'http://www.highpin.cn/zhiwei/?fromType=12&utm_source=zpsygdad&utm_medium=cpc&utm_content=zpsygdadtextlink&utm_campaign=zpsygdadanalytics&utm_term=onlinepromo_201402',
                'http://www.zhaopin.com/jobseeker/index_industry.html', 'http://ir.zhaopin.com',
                'http://special.zhaopin.com/sh/2009/aboutus/join.html', 'http://sou.zhaopin.com/jobs/searchresult.ashx?isadv=1',
                'http://sou.zhaopin.com']         #for deleting
lock = Lock()
job_type_id = {}
city_list = set()
statistics = {}
start_time = time()
attr_error = []
db = pymysql.connect("localhost", "root", "root", "PARSING_JOBS", charset='utf8')
cursor = db.cursor()
# cursor.execute("CREATE DATABASE PARSING_JOBS")
cursor.execute("DROP TABLE IF EXISTS job_statistics")
cursor.execute("CREATE TABLE job_statistics(job_location VARCHAR(100), job_field VARCHAR(100), job VARCHAR(100), num INT)")
# Proxies=["101.53.101.172:9999","101.53.101.172:9999","171.117.93.229:8118","119.251.60.37:21387","58.246.194.70:8080"]


# def find_checkboxes(html):
#     '''
#     find the place to set the workplace
#     '''
#     city = html.find('div', attrs={'class': 'city2'})
#     print(city.prettify())
#
#
# def by_city(city):
#     '''
#     set the workplace
#     :param city:
#     :return:
#     '''
#     cj = http.cookiejar.CookieJar()
#     opener = build_opener(HTTPCookieProcessor(cj))
#     html = opener.open(URL).read()
#     data = parse_form(html)
#     data['c7'] = '538'
#     encode_data = urlencode(data)
#     binary_data = encode_data.encode('UTF-8')
#     request = Request(URL, binary_data)
#     response = opener.open(request)
#     print(response.geturl())
#     return response
#
#
# def parse_form(html):
#     tree = lxml.html.fromstring(html)
#     data = {}
#     for e in tree.cssselect('form input'):
#         if e.get('name'):
#             data[e.get('name')] = e.get('value')
#     return data

# def getHtml(url, proxies=Proxies):
#     proxy = choice(proxies)     #随机取一个ip出来使用
#     proxy_support = ProxyHandler({"http": proxy})
#     opener = build_opener(proxy_support)
#     install_opener(opener)
#     html = urlopen(url)
#     return html


def parsing_categary(url):
    '''
    parsing the url and get the job statistics
    :param url:
    :return: job statistics
    '''
    city_quote = re.search('jl=([\w|%|/|（|）]+)&sm=0&p=1', url).group(1)
    city_unquote = unquote(city_quote)
    # cat_page = getHtml(url)
    cat_page = urlopen(url)
    cat_bs4 = BeautifulSoup(cat_page, 'lxml')
    #print(cat_bs4.prettify())
    categary = cat_bs4.find('div', attrs={'class': 'search_newlist_topmain2 fl', 'id': 'search_jobtype_tag'})
    n = 0
    #statistics = {}
    key1 = ''
    print(url)
    try:
        for ty in categary.find_all('a'):
            #print(ty)
            #print(ty.text)
            if n:
                m = re.match('(.*?)\((\d+)\)', ty.text)
                if n == 1:
                    key1 = m.group(1)
                else:
                    # addtwodimdict(statistics, key1, m.group(1), m.group(2))
                    print(city_unquote, key1, m.group(1), m.group(2))
                    try:
                        cursor.execute("INSERT INTO job_statistics(job_location, job_field, job, num) VALUES ('%s', '%s', '%s', '%d')" % (city_unquote, key1, m.group(1), int(m.group(2))))
                    except pymysql.err.InterfaceError:
                        pass
                    # cursor.execute("UPDATE job_statistics SET num = '%d' WHERE (job_location = '%s' and job_field = '%s' and job = '%s')" % (int(m.group(2)), city_unquote, key1, m.group(1)))
            n += 1
    except AttributeError:
        attr_error.append(url)
    sleep(uniform(1, 3))
    #return statistics


def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})



def loop(url):
    lock.acquire()
    parsing_categary(url)
    lock.release()

def find_job_id(url):
    '''find the id of job in http://sou.zhaopin.com'''
    home_content = BeautifulSoup(url, 'lxml')
    for job_type in home_content.find_all('span', class_="availItem"):
        job_span = job_type.prettify()
        # print(job_span)
        m = re.search('this,\[\'(\d+)\',\'([\w|/|（|）]+)\'\]', job_span)
        job_type_id[m.group(2)] = m.group(1)
    print('***********lengh of job_type_id:', len(job_type_id), '***********')


def find_cities(url):
    '''find the cities in http://sou.zhaopin.com'''
    home_content = BeautifulSoup(url, 'lxml')
    for city in home_content.find_all('label', class_="noselItem"):
        city_list.add(city.get_text())

def threaded(links):
    a = 1
    threads = []
    max_threads = 10
    while threads or links:
        for thread in threads:
            if  not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and links:# and a < 1000
            lin = links.pop()
            print(str(a), "    ", lin)
            t = Thread(target=loop, args=(lin,))
            t.start()
            threads.append(t)
            a += 1
    sleep(5)

def main():
    # f = by_city('city')
    # print(url_o)
    browser = webdriver.Chrome()
    browser.get(URL)
    browser.find_element_by_id("buttonSelJobType").click()
    find_job_id(browser.page_source)
    # print('closeButton', len(browser.find_elements_by_css_selector("div.sPopupDiv div.sPopupTitle290 div.sButtonBlock a.closeButton")))
    closeButton = browser.find_elements_by_css_selector("div.sPopupDiv div.sPopupTitle290 div.sButtonBlock a.closeButton")
    closeButton[1].click()
    browser.find_element_by_id("buttonSelCity").click()
    select_city = browser.find_elements_by_css_selector("span.seledCityItem a.seledCityClose")
    # print('select city', len(select_city))
    for a in select_city: a.click()
    orgButton = browser.find_elements_by_css_selector("div.sPopupDiv div.sPopupTitle290 div.sButtonBlock a.orgButton")
    orgButton[1].click()
    browser.find_element_by_id("buttonSelCity").click()
    provinces = browser.find_elements_by_css_selector("table.sPopupTabC span.availItem")#td.blurItem
    print('provinces', len(provinces))
    for province in provinces:
        province.click()
        # WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_css_selector("div.sPopupDivSubJobname.sPopupDivSubCity label.noselItem").is_displayed())
        # cities = browser.find_elements_by_css_selector("div.sPopupDivSubJobname label.noselItem")
        cities = browser.find_elements_by_css_selector("label.noselItem")
        # find_cities(browser.page_source)
        for city in cities:
            if city.text:
                city_list.add(city.text)
    # print('pIconPlus', len(browser.find_elements_by_css_selector("div.pCityTitB span.pIconPlus")))
    # browser.find_element_by_css_selector("div.pCityTitB span.pIconPlus").click()
    # # try:
    # #     WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_css_selector("div.pCityTitB table.sPopupTabC label.noselItem").is_displayed())
    # # except TimeoutException:
    # #     print(TimeoutException.__context__)
    # foriens = browser.find_elements_by_css_selector("label.noselItem")
    # # foriens = browser.find_elements_by_css_selector("div.pCityTitB table.sPopupTabC label.noselItem")
    # for city in foriens:
    #         if city.text:
    #             city_list.add(city.text)
    browser.close()
    print('city_list', len(city_list))
    print(sorted(city_list))
    link_by_category = set()
    link_visited = set()
    print('\n\n*********************************')
    for city in city_list:
        for job_id in job_type_id.values():
            search_url = URL + '/jobs/searchresult.ashx?bj=' + job_id + '&jl=' + quote(city) + '&sm=0&p=1'
            if search_url not in link_visited: link_by_category.add(search_url)
    print('the number of search urls:', len(link_by_category))


    # f = urlopen(URL)
    # home_content = BeautifulSoup(f, 'lxml')
    # o = open('parse_out', 'w', encoding='UTF-8')
    # print(home_content.prettify())       #print html code to screem
    # o.write(home_content.prettify())     #print html code to file
    # print("\n\nall the sorted links in the page by BeautifulSoup:")
    # for lin in home_content.find_all('a'):
    #     find_link = urljoin(URL, lin['href'])
    #     if (find_link not in discard_link) and (not re.match('javascript', find_link)) and (not re.search("sj=\d+", find_link)):
    #         link_by_category.add(find_link)
    # print('\n\n')
    # find_checkboxes(home_content)



    # num_cpus = multiprocessing.cpu_count()
    # print('Starting {} processes'.format(num_cpus))
    # processes = []
    # link_num = len(link_by_category)
    # link_by_category = list(link_by_category)
    # each_pr = link_num//num_cpus
    # for i in range(num_cpus):
    #     link_start = i*each_pr
    #     link_stop = (i + 1)*each_pr
    #     if i == num_cpus-1:
    #         lind_send = link_by_category[link_start:]
    #         print('Process---', len(lind_send))
    #         p = multiprocessing.Process(target=threaded, args=(lind_send,))
    #     else:
    #         lind_send = link_by_category[link_start: link_stop]
    #         print('Process---', len(lind_send))
    #         p = multiprocessing.Process(target=threaded, args=(lind_send,))
    #     p.start()
    #     processes.append(p)
    #     sleep(5)
    # # wait for processes to complete
    # for p in processes:
    #     p.join()


    a = 1
    threads = []
    max_threads = 10
    while threads or link_by_category:
        for thread in threads:
            if  not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and link_by_category:
            lin = link_by_category.pop()
            print(str(a), "    ", lin)
            t = Thread(target=loop, args=(lin,))
            t.start()
            threads.append(t)
            a += 1
    if attr_error:
        print('\n\n************ AttributeError **************')
        for error_url in attr_error:
            print(error_url)
    sleep(10)
    #parsing_categary('http://sou.zhaopin.com/jobs/searchresult.ashx?jl=763&bj=121300')

@register
def _atexit():
    end_time = time()
    print('all done at:', ctime())
    hour = int((end_time - start_time)//360)
    minite = int((end_time - start_time)%360//60)
    sec = int((end_time - start_time)%360%60)
    sp = 'spending ' + str(hour) + 'h' + str(minite) + 'min' + str(sec) + 's'
    print(sp)
    db.close()


if __name__ == "__main__":
    main()
    # db.close()
