# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import datetime
from bcy.items import BcyItem

class ExampleSpider(scrapy.Spider):
    #fileobj = open('out.txt','w+')
    name = 'top100'
    allowed_domains = ['bcy.net']
    now = datetime.datetime.now()
    start_urls = []
    #cacth page
    for i in range(0,1):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=i)
        n_days = now - delta
        #print n_days.strftime('%Y%m%d')
        start_urls.append('https://bcy.net/coser/toppost100?type=week&date='+n_days.strftime('%Y%m%d'))
        #print repr(start_urls)

    #parse page
    def parse(self, response):
        for a in response.css('li._box'):
            item = BcyItem()
            item['rank'] = a.css('span::text').extract_first()
            item['title'] = a.css('a::attr(title)').extract_first()
            item['date'] = response.url[-8:]
            if a.css('a::attr(href)').extract_first():
                item['url'] = 'https://bcy.net'+a.css('a::attr(href)').extract()[2]
                item['link'] = a.css('a::attr(href)').extract_first()
                next_page = 'https://bcy.net' + a.css('a::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(next_page, meta={'key':item},callback=self.ablum_parse,dont_filter=True)
            else:
                item['state']=''
                item['city']=''
                item['url']=''
                item['link'] = ''
                item['auth_url']=''
                item['auth_name']=''
                item['cartoon_name'] = ''
                item['following'] = ''
                item['follower'] = ''
                yield item

    def ablum_parse(self,response):
        item = response.meta['key']
        item['auth_url'] = response.url
        print item['auth_url']
        item['auth_name'] = response.css('a.fz14.dib.maxw250.cut::text').extract_first()
        if response.css('a._tag._tag--normal.cut.db::text') :
            item['cartoon_name'] = response.css('a._tag._tag--normal.cut.db::text').extract()[1].strip()
            item['following'] = response.css('a.vhr__item.minor::text').extract_first()[10:].strip()
            item['follower'] = response.css('a.tal.vhr__item.vhr__item--last.minor::text').extract_first()[10:].strip()
        else:
            item['cartoon_name'] = ''
            item['following'] = ''
            item['follower'] = ''
        yield scrapy.Request(item['url'], meta={'key':item},callback=self.auth_parse,dont_filter=True)

    def auth_parse(self,response):
        item = response.meta['key']
        b = response.xpath('//script[@id="tpl-profile-body"]')
        locate = re.findall(r'<p class="text fz14 lh1d4 mb15">(.+?)</p>',str(b.extract_first()))[1].decode()
        #print locate
        #re.findall(r'<p class="text fz14 lh1d4 mb15">(.+?)</p>',str(b.extract()).decode())[1] 
        #locate = response.css('span.fz14::text').extract_first()
        locate_list = []
        locate_list = locate.split()
        item['state']=locate_list[0]
        item['city']=''
        if len(locate_list) >=2:
            item['city']=locate_list[1]

        #item['state']=''
        #item['city']=''
        yield item
 
