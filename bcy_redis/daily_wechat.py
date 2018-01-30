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
import string
import itchat

#class MyTemplate(string.Template):    
#    delimiter = '%'
#    idpattern = '[a-z]+_[a-z]+'

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
#    params = [datetime.datetime.now().strftime('%Y-%m-%d'),count,top1name,top1title,top2name,top2title,top3name,top3title]  # 当模板没有参数时，`params = []`
    params = [datetime.datetime.now().strftime('%Y-%m-%d'),count,top1name.decode('utf-8')[0:16].encode('utf-8'),top1title,top2name.decode('utf-8')[0:16].encode('utf-8'),top2title,top3name.decode('utf-8')[0:16].encode('utf-8'),top3title]  # 当模板没有参数时，`params = []`
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
        template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    print result['result']
    print result['errmsg'].encode('utf-8')

def process_item():
    dbObject = dbHandle()
    cursor = dbObject.cursor()
    now = datetime.datetime.now().strftime('%Y%m%d')
    cursor.execute("USE bcy")
    sql = "SELECT count(date) as rows,date FROM top_redis where date =%s"
    sql2 ="SELECT title,auth_name FROM top_redis where date =%s and rank<=3 order by rank"
    sql3 =u"SELECT cartoon_name,count(id) AS counts FROM top_redis where date=%s GROUP BY    cartoon_name ORDER BY counts DESC limit 10"
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
    try:
        cursor.execute(sql3,now)
        cursor.connection.commit()
        topics = cursor.fetchall()
        #process_sms(result[0])
    except BaseException as e:
        print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
        dbObject.rollback()

    #process_sms(daily_get+'第一名:'+daily_list[0][0])
    #process_list(daily_get,daily_list[0][0],daily_list[0][1],daily_list[1][0],daily_list[1][1],daily_list[2][0],daily_list[2][1])
    template_text = ''' 
$now
抓取 : $get_count 条
第一 : 【$st_title】
第二 : 【$nd_title】
第三 : 【$rd_title】 
    '''
    template_list = '''
 【 题材 】 | 【 今日作品数 】
--------------------------
1.【$top_1】 | $top1_count
2.【$top_2】 | $top2_count
3.【$top_3】 | $top3_count
4.【$top_4】 | $top4_count
5.【$top_5】 | $top5_count
'''
    t=string.Template(template_text) 

    daily={
'now':now,
'get_count':daily_get,
'st_title':daily_list[0][0],
'nd_title':daily_list[1][0],
'rd_title':daily_list[2][0]}

    t2=string.Template(template_list)

    topic_daily={
'top_1':topics[0][0],
'top1_count':topics[0][1],
'top_2':topics[1][0],'top2_count':topics[1][1],
'top_3':topics[2][0],'top3_count':topics[2][1],
'top_4':topics[3][0],'top4_count':topics[3][1],
'top_5':topics[4][0],'top5_count':topics[4][1]
}
    
#    msg = daily_get+daily_list[0][0]+daily_list[0][1]+daily_list[1][0]+daily_list[1][1]+daily_list[2][0]+daily_list[2][1]
    msg = t.safe_substitute(daily)
    msg_topic = t2.safe_substitute(topic_daily)
#    print daily
#    print msg_topic

    itchat.auto_login(hotReload=True,enableCmdQR=2)


    groups = itchat.search_chatrooms(name='CP666 All工作群')
    group=groups[0]
    username=group.get('UserName')

    groups = itchat.search_chatrooms(name='CP666研发')
    group=groups[0]
    workgroup=group.get('UserName')
    itchat.send(msg,'filehelper')
    itchat.send(msg, username)
    itchat.send(msg_topic, username)
    itchat.send(msg, workgroup)
    itchat.send(msg_topic, workgroup)
#    chatlist= itchat.get_chatrooms()
#    chatlist = itchat.search_chatrooms(name='CP666')
#    print str(chatlist)


process_item()
