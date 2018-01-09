import datetime
global urls 
urls = []
'''
for i in range(0,30):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=i)
    n_days = now - delta
    print n_days.strftime('%Y%m%d')
    urls.append('https://bcy.net/coser/toppost100?type=week&date='+n_days.strftime('%Y%m%d'))
    print urls[i]
'''
str1 = 'Subscribe 143'
str2 = 'Followers 43196'
print str1[10:]
print str2[10:]
