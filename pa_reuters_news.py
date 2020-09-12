#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import difflib
import re
import urllib
from bs4 import BeautifulSoup
import datetime

def remove_similar(lists,similarity=0.85):
    i=0
    l=len(lists)
    while i<l:
        j=i+1
        while j<l:
            seq=difflib.SequenceMatcher(None,lists[i],lists[j])
            ratio=seq.ratio()
            if ratio>=similarity:
                del lists[j]
                l=l-1
            else:
                j+=1
        i+=1
    return lists

codelist = ['AAPL','VZ', 'AGN', 'PFE', 'CBS', 'PEP', 'UPS', 'JCP', 'MA',
         'HD', 'LMT', 'JNJ', 'TGT', 'S', 'CMG', 'IBM', 'NDAQ',
         'SBUX', 'KR', 'NVDA', 'KSS', 'BMY', 'NKE', 'LUV', 'AMZN',
         'CMCSA', 'GOOG', 'MS', 'WMT', 'INTC', 'GS', 'BLK', 'BAC', 'FB',
         'MSFT', 'NFLX', 'F', 'XOM', 'BA', 'GE', 'DIS', 'M', 'C', 'JPM']
wrongcode = []
for code in codelist:
    print(code)
    i = 0
    day_num = 0
    dt = '2015-12-31'
    while (i < 365):
        myday = datetime.datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10])) + datetime.timedelta(days=+1)
        # print(myday
        dt = myday.strftime("%Y-%m-%d")
        print(dt)
        date = myday.strftime('%m%d%Y')
        # zhui = ['', 'O', 'OQ', 'N']
        try:
            url = "https://www.reuters.com/finance/stocks/company-news/" + code + "?date=" + date

            req = urllib.Request(url)
            req.add_header("user-agent", "Mozilla/5.0")
            request = urllib.urlopen(req)
            html_doc = request.read()


            soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
            html_doc2 = str(soup.select('#companyNews'))
            soup1 = BeautifulSoup(html_doc2, "html.parser", from_encoding="utf-8")
            links = soup1.find_all('a')
        except:
            print("something wrong")
            wrongcode.append(code)
            print(wrongcode)
            break

        news = []
        for link in links:
            if (str(link.get_text()).__len__() > 20):  # remove "continue reading"

                news.append(str(link.get_text()).encode('utf8'))
        news = list(set(news))

        if len(news):
            day_num = day_num + 1
            with open('/Users/xiaoxiao/USAnews_2016/' + code + '.csv', 'a') as f:
                writer = csv.writer(f)
                news = remove_similar(news)
                for n in news:
                    one = [dt, n]
                    print(one)
                    writer.writerow(one)
            '''
            fileObject = open('/Users/xiaoxiao/news_final_2017/' + code + '/' + dt + '.txt', 'a')
            for n in news:
                fileObject.write(n)
                fileObject.write('\n')
            fileObject.close()'''
            print(day_num)
        i = i + 1
        if(i>=60 and day_num<=5):
            break
    '''
    fileObject2 = open('/Users/xiaoxiao/reuters_news_17/news_days_num.txt', 'a')
    fileObject2.write(code+' '+str(day_num))
    fileObject2.write('\n')
    fileObject2.close()'''
print(wrongcode)


