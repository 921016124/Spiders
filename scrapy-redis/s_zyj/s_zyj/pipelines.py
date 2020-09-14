# -*- coding: utf-8 -*-
import pymysql
import sys
sys.path.append("E:\Spider\Projects\SunLine\scrapy-redis\s_zyj\s_zyj")
from items import SrZyjItem, SrZyjJobItem, SrRzItem
import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SrZyjPipeline(object):
    def __init__(self):
        self.dbparams = {
            'host': settings.MYSQL_HOST,
            'port': settings.MYSQL_PORT,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWD,
            'database': settings.MYSQL_DB,
            'charset': settings.MYSQL_CHARSET
        } 

    def insert2mysql(self, sql, t, conn, cursor):
        try:
            cursor.execute(sql, t)
            conn.commit()
        except pymysql.err.IntegrityError:
            return False
        return True

    def process_item(self, item, spider):
        conn = pymysql.connect(**self.dbparams)
        cursor = conn.cursor()
        # print("数据库连接成功~~~")
        if isinstance(item, SrZyjItem):
            t_sql_info = (
                    item["id_code"],
                    item["title"],
                    item["brief_intro"],
                    item["xingzhi"],
                    item["guimo"],
                    item["hangye"],
                    item["rongzi"],
                    item["quancheng"],
                    item["intro"],
                    item["job_count"],
                    item["comp_code"],
                    item["crawl_time"]
                )
            if self.insert2mysql(self.sql_info, t_sql_info, conn, cursor):
                print("(企业信息) "+item["title"] + " 插入成功")
            else:
                print(item["title"] + " 插入失败，数据重复")
        elif isinstance(item, SrZyjJobItem):
            t_sql_job = (
                item["id_code"],
                item["job_name"],
                item["job_location"],
                item["job_xueli"],
                item["job_year"],
                item["job_xingzhi"],
                item["job_money"],
                item["comp_code"],
                item["crawl_time"]
            )
            if self.insert2mysql(self.sql_job, t_sql_job, conn, cursor):
                print(item["job_name"] + "-{} 插入成功".format(item["job_name"]))
            else:
                print(item["job_name"] + "-{} 插入失败，数据重复".format(item["job_name"]))
        elif isinstance(item, SrRzItem):
            t_sql_rz = (
                item["id_code"],
                item["rz_stage"],
                item["rz_money"],
                item["rz_edate"],
                item["rz_compy"],
                item["comp_code"],
                item["crawl_time"]
            )
            if self.insert2mysql(self.sql_rz, t_sql_rz, conn, cursor):
                print(item["rz_stage"] + "-{} 插入成功".format(item["rz_money"]))
            else:
                print(item["rz_stage"] + "-{} 插入失败，数据重复".format(item["rz_money"]))
        return item

    @property
    def sql_info(self):
        sql_info = """
                insert into tmp_jobui_info_n(id, title, brief_intro, 
                                    xingzhi, guimo, hangye, 
                                    rongzi, quancheng, 
                                    intro, job_count, comp_code, crawl_time) 
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        return sql_info

    @property
    def sql_job(self): 
        sql_job = """
                    insert into tmp_jobui_job_n(id, job_name, job_location, 
                                        job_xueli, job_year, 
                                        job_xingzhi, job_money, comp_code, crawl_time) 
                                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                """
        return sql_job

    @property
    def sql_rz(self):
        sql_rz = """
                insert into tmp_jobui_rz(id, rz_stage, rz_money, rz_edate, 
                                        rz_compy, comp_code, crawl_time) 
                                        values(%s,%s,%s,%s,%s,%s,%s) 
        """
        return sql_rz
