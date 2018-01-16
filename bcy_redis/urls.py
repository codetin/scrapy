#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import redis

r = redis.Redis(host='127.0.0.1', port=6379,db=0)

#start_urls = []
for i in range(0,1):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=i)
    n_days = now - delta
    #print n_days.strftime('%Y%m%d')
    #start_urls.append('https://bcy.net/coser/toppost100?type=week&date='+n_days.strftime('%Y%m%d'))
    #print repr(start_urls)
    url = 'https://bcy.net/coser/toppost100?type=week&date='+n_days.strftime('%Y%m%d')
    r.lpush("RedisSpider:start_urls",url)
    print url
