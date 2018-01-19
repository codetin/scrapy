# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
def dbHandle():
    conn = pymysql.connect(
        host = "10.154.21.83",
        user = "root",
        passwd = "capcom",
        charset = "utf8",
        use_unicode = False
    )
    return conn


class BcyRedisPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE bcy")
        sql = "INSERT INTO top_redis(location,rank,url,date,link,title,auth_url,auth_name,cartoon_name,following,follower) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print repr(item)
        try:
            cursor.execute(sql,(item['location'],item['rank'],item['url'],item['date'],item['link'],item['title'],item['auth_url'],item['auth_name'],item['cartoon_name'],item['following'],item['follower']))
            cursor.connection.commit()
        except BaseException as e:
            print("mysql insert error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
            dbObject.rollback()


        return item
