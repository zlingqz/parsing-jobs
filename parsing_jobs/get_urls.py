#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import re
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote


URL = 'http://sou.zhaopin.com'   #智联招聘https://www.zhaopin.com
job_type_id = {}
city_list = set()


def find_job_id(url):
    '''find the id of job in http://sou.zhaopin.com'''
    home_content = BeautifulSoup(url, 'lxml')
    for job_type in home_content.find_all('span', class_="availItem"):
        job_span = job_type.prettify()
        # print(job_span)
        m = re.search('this,\[\'(\d+)\',\'([\w|/|（|）]+)\'\]', job_span)
        job_type_id[m.group(2)] = m.group(1)
    print('*********** length of job_type_id:', len(job_type_id), '***********')


def Get_Urls():
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
    browser.close()
    print('city_list', len(city_list))
    print(sorted(city_list))
    link_by_category = set()
    f = open('urls.txt', 'w')
    for city in city_list:
        for job_id in job_type_id.values():
            search_url = URL + '/jobs/searchresult.ashx?bj=' + job_id + '&jl=' + quote(city) + '&sm=0&p=1'
            link_by_category.add(search_url)
            f.write(search_url)
            f.write('\n')
    print('the number of search urls:', len(link_by_category))


if __name__ == "__main__":
    Get_Urls()
