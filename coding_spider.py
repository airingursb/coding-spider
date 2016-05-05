# -*-coding:utf8-*-

import requests
import json
import time
import MySQLdb
from multiprocessing.dummy import Pool as ThreadPool
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

urls = []

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}

time1 = time.time()
for i in range(1000, 5000):
    url = 'https://coding.net/api/public/all?page=' + str(i) + '&pageSize=1'
    urls.append(url)

def getsource(url):
    jscontent = requests.get(url, headers=head, verify=True).content
    time2 = time.time()
    jsDict = json.loads(jscontent)
    if jsDict['code'] == 0:
        jsList = jsDict['data']
        jsData = jsList['list'][0]
        id = jsData['id']
        name = jsData['name']
        url = jsData['https_url']
        description = jsData['description']
        print "Succeed: " + str(id) + "\t" + str(time2 - time1)
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8')
            cur = conn.cursor()
            conn.select_db('python')
            cur.execute('INSERT INTO coding VALUES (%s,%s,%s,%s)',
                        [int(id), name, url, description])
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        print "Error: " + url


pool = ThreadPool(8)
try:
    results = pool.map(getsource, urls)
except Exception:
    print 'ConnectionError'
    time.sleep(300)
    results = pool.map(getsource, urls)

pool.close()
pool.join()
