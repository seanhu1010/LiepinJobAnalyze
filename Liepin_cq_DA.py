# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   Liepin_cq_DA
   Description: 
   Author:      LOVE
   Date:        2018/3/28
-------------------------------------------------
   Change Activity:
                2018/3/28:
-------------------------------------------------
"""

from pyspider.libs.base_handler import *
import pymongo
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    client = pymongo.MongoClient('localhost')
    db = client['job']

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(
            'https://www.liepin.com/zhaopin/?industries=&dqs=040&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=08982c32ef66927e&d_headId=78641e553d7a3a94cb77c60a9c48bc0a&d_ckId=83d998f7b7a01118732e8a5513e78fca&d_sfrom=search_unknown&d_curPage=0&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~DnIK07pheM0dUfyGVexLMQ&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90',
            callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.job-info > h3 > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        next = response.doc('.pagerbar >a.last').prev().attr.href
        self.crawl(next, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        name = response.doc('.title-info >h1').text()
        company = response.doc('h3 > a').text()
        salary = re.findall(r'.*(?=\s)', response.doc('.job-item-title').text())
        salary = salary[0] if salary else None
        ack = response.doc('.job-item-title .blue').text()
        location = response.doc('.basic-infor > span > a').text()
        publishtime = response.doc('.basic-infor > time').attr.title
        qualifications = response.doc('.job-qualifications').text()
        tag_list = response.doc('.tag-list').text()
        description = response.doc('.content-word').text()
        other_info_temp = response.doc('.job-item.main-message .content li')
        other_info_key = [i.text().strip('：') for i in other_info_temp.items('span')]
        other_info_value = [i.text() for i in other_info_temp.items('label')]
        other_info = dict(zip(other_info_key, other_info_value))
        company_info = response.doc('.info-word').text()

        return {
            "url": url,
            "name": name,
            "company": company,
            "salary": salary,
            "ack": ack,
            "location": location,
            "publishtime": publishtime,
            "qualifications": qualifications,
            "tag_list": tag_list,
            "description": description,
            "other_info": other_info,
            "company_info": company_info
        }

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        if self.db['liepin_cq_DA'].insert(result):
            print('saved to mongo', result)
