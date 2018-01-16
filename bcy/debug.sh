#!/bin/bash
cd /root/scrapy/bcy
scrapy parse --spider=top100 -c parse -v https://bcy.net/coser/toppost100 --depth 2
