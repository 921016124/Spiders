# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SrZyjItem(scrapy.Item):
    # spider jobui Item
    id_code = scrapy.Field()  # 标题
    title = scrapy.Field()  # 标题
    brief_intro = scrapy.Field()  # 简介
    xingzhi = scrapy.Field()  # 性质
    guimo = scrapy.Field()  # 规模
    hangye = scrapy.Field()  # 行业
    rongzi = scrapy.Field()  # 融资
    quancheng = scrapy.Field()  # 全称
    intro = scrapy.Field()  # 介绍
    job_count = scrapy.Field()  # 招聘数量
    comp_code = scrapy.Field()  # 职友集中公司的代码
    crawl_time = scrapy.Field()  # 采集时间


class SrZyjJobItem(scrapy.Item):
    # spider jobui_job
    id_code = scrapy.Field()
    job_name = scrapy.Field()  # 工作名称
    job_location = scrapy.Field()  # 工作地点
    job_xueli = scrapy.Field()  # 工作学历
    job_year = scrapy.Field()  # 工作年限
    job_xingzhi = scrapy.Field()  # 工作性质
    job_money = scrapy.Field()   # 工作薪资
    comp_code = scrapy.Field()  # 职友集中公司的代码
    crawl_time = scrapy.Field()  # 采集时间


class SrRzItem(scrapy.Item):
    # spider jobui rongzi
    id_code = scrapy.Field()
    rz_stage = scrapy.Field()  # 融资阶段
    rz_money = scrapy.Field()  # 融资金额
    rz_edate = scrapy.Field()  # 融资时间
    rz_compy = scrapy.Field()  # 融资方
    comp_code = scrapy.Field()  # 职友集中公司的代码
    crawl_time = scrapy.Field()  # 采集时间
