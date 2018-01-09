#!/bin/bash
>listtop.json
scrapy crawl listtop -o listtop.json -s FEED_EXPORT_ENCODING=utf-8
