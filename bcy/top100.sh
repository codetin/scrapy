#!/bin/bash
cd /root/scrapy/bcy
scrapy crawl top100 #-o top100.json -s FEED_EXPORT_ENCODING=utf-8
