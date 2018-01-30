#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import redis
from sys import argv 
import pymysql

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

def dbHandle():
    conn = pymysql.connect(
        host = "10.154.21.83",
        user = "root",
        passwd = "capcom",
        charset = "utf8",
        use_unicode = False
    )
    return conn

def process_sms(message):
    # 短信应用SDK AppID
    appid = 1400064260  # SDK AppID是1400开头
    # 短信应用SDK AppKey
    appkey = "3777a2b8b44f77de3030460a7707d2ce"
    # 需要发送短信的手机号码
    phone_numbers = ["18616356197"]
    # 短信模板ID，需要在短信应用中申请
    template_id = 80067  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
    # 签名
    sms_sign = "DataBro"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`
    sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
    ssender = SmsSingleSender(appid, appkey)
    params = [datetime.datetime.now().strftime('%Y-%m-%d'),message]  # 当模板没有参数时，`params = []`
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
        template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

def process_list(count,top1name,top1title,top2name,top2title,top3name,top3title):

    # 短信应用SDK AppID
    appid = 1400064260  # SDK AppID是1400开头
    # 短信应用SDK AppKey
    appkey = "3777a2b8b44f77de3030460a7707d2ce"
    # 需要发送短信的手机号码
    phone_numbers = ["18616356197"]
    # 短信模板ID，需要在短信应用中申请
    template_id = 83336  # NOTE: 这里的模板ID，真实的模板ID需要在短信控制台中申请
    # 签名
    sms_sign = "DataBro"  # NOTE: 这里的签名，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`
    sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
    ssender = SmsSingleSender(appid, appkey)
    #半次元{1}数据抓取成功,共获取{2}条数据. 第一名{3},作品{4} 第二名{5},作品{6} 第三名{7},作品{8}
    params = [datetime.datetime.now().strftime('%Y-%m-%d'),count,top1name,top1title,top2name,top2title,top3name,top3title]  # 当模板没有参数时，`params = []`
    print count+'.'+top1name+'.'+top1title+'.'+top2name+'.'+top2title+'.'+top3name+'.'+top3title
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
        template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

def process_item():
    dbObject = dbHandle()
    cursor = dbObject.cursor()
    now = datetime.datetime.now().strftime('%Y%m%d')
    cursor.execute("USE bcy")
    sql = "SELECT count(date) as rows,date FROM top_redis where date =%s"
    sql2 ="SELECT title,auth_name FROM top_redis where date =%s and rank<=3 order by rank"
    try:
        cursor.execute(sql,now)
        cursor.connection.commit()
        result = cursor.fetchone()
        daily_get = str(result[0])
        #process_sms(result[0])
    except BaseException as e:
        print("mysql insert error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
        dbObject.rollback()
    try:
        cursor.execute(sql2,now)
        cursor.connection.commit()
        daily_list = cursor.fetchall()
        #process_sms(result[0])
    except BaseException as e:
        print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
        dbObject.rollback()
    #process_sms(daily_get+'第一名:'+daily_list[0][0])
    process_list(daily_get,daily_list[0][0],daily_list[0][1],daily_list[1][0],daily_list[1][1],daily_list[2][0],daily_list[2][1])

process_item()
