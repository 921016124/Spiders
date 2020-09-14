import time
from S_HaiGuan_test import HaiGuan
from Spiders.Utils_1 import Util


class HaiGuanCredit:
    def __init__(self):
        self.u = Util()

    def h_list_data(self, da, tags, comp_name):
        if da["socialCreditCode"]:
            id_code = self.u.MD5(da["nameSaic"] + da["socialCreditCode"])
        else:
            id_code = self.u.MD5(da["nameSaic"] + da["regCoCgac"])
        socialCreditCode = da["socialCreditCode"]
        regCoCgac = da["regCoCgac"]
        firstRegDate = da["firstRegDate"]
        depCodeChgName = da["depCodeChgName"]
        nameSaic = da["nameSaic"]
        addressSaic = da["addressSaic"]
        apanageName = da["apanageName"]
        apanageRegionName = da["apanageRegionName"]
        tradeTypeName = da["tradeTypeName"]
        specialTradeZoneName = da["specialTradeZoneName"]
        busiKindName = da["busiKindName"]
        availDate = da["availDate"]
        revokeFlag = da["revokeFlag"]
        annalsDate = da["annalsDate"]
        abnormalCondition = da["abnormalCondition"]
        craw_time = self.u.get_now_time()

        exe_sql = "insert into tmp_haiguan(id, socialCreditCode, regCoCgac,firstRegDate," \
                  "depCodeChgName,nameSaic,addressSaic,apanageName,apanageRegionName," \
                  "tradeTypeName,specialTradeZoneName,busiKindName,availDate,revokeFlag," \
                  "annalsDate,abnormalCondition, tags, craw_time) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                  "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s')" % (id_code, socialCreditCode, regCoCgac,
                                                                       firstRegDate, depCodeChgName, nameSaic,
                                                                       addressSaic, apanageName, apanageRegionName,
                                                                       tradeTypeName, specialTradeZoneName, busiKindName,
                                                                       availDate, revokeFlag, annalsDate, abnormalCondition,tags, craw_time)
        up_sql = "update EXT_INV_ENTP_LST_INF set status = '1' where OVS_INV_NM LIKE '%{}%';".format("%".join([i for i in comp_name]))
        # print(up_sql)
        # self.u.insert2mysql(nameSaic, exe_sql, up_sql)

    def handle_data(self, data, tags, comp_name):
        if "copInfoList" in data.keys():
            for da in data["copInfoList"]:
                self.h_list_data(da, tags, comp_name)
        elif "copInfo" in data.keys(): 
            self.h_list_data(data["copInfo"], tags, comp_name)

    def main(self):
        conn = self.u.MySQL()
        cursor = conn.cursor()

        sql = "select distinct OVS_INV_NM from EXT_INV_ENTP_LST_INF where status = \"0\";"
        cursor.execute(sql)
        title_ls = cursor.fetchall()
        for title in title_ls:
            title = title[0].replace(",","").replace("。","").replace("，","").replace(".","").replace("《","").replace("》","")
            print("-- {} --".format(title))
            hg = HaiGuan(title)
            hg.main()
            time.sleep(5)

