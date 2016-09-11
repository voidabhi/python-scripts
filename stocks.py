
# get stocks data for handle
# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib2
import re

def getkabuka(code):
   url='http://stocks.finance.yahoo.co.jp/stocks/detail/?code='+str(code)+'.T&d=1y'
   f=urllib2.urlopen(url)
   txt=f.read()
   txt=unicode(txt,"utf-8")  #unicodeに変換
   string=u'>現在値<strong>(.+?)</strong>.+<span class="yjFL">([-0-9,]+?)</span>.+>前日比</span>.+?>([-+,0-9]+?)</strong>'
   m=re.search(string,txt, re.DOTALL)
   print m.group(1),m.group(2),m.group(3)
   return m.group(1),m.group(2),m.group(3)

kabuka= getkabuka(4689)
print kabuka[0],u"の株価は",kabuka[1],u"円で、",kabuka[2],u"円変化しました"
