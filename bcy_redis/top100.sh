#!/bin/bash
cd /root/scrapy/bcy_redis/bcy_redis
scrapy crawl top100_redis 
#-o top100.json -s FEED_EXPORT_ENCODING=utf-8
