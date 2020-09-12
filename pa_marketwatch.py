#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import os
import sys
import time
import urllib
import json

def creatfile(path):
    os.makedirs(path)
# https://www.marketwatch.com/investing/stock/aapl
# "https://api.wsj.net/api/slinger/headlines/806/20?direction=older&datetime=2017-12-31T00:00:00&opProp=symb!~!US:AAPL"
code_list = ['AAPL','VZ', 'AGN', 'PFE', 'CBS', 'PEP', 'UPS', 'JCP', 'MA',
         'HD', 'LMT', 'JNJ', 'TGT', 'S', 'CMG', 'IBM', 'NDAQ',
         'SBUX', 'KR', 'NVDA', 'KSS', 'BMY', 'NKE', 'LUV', 'AMZN',
         'CMCSA', 'GOOG', 'MS', 'WMT', 'INTC', 'GS', 'BLK', 'BAC', 'FB',
         'MSFT', 'NFLX', 'F', 'XOM', 'BA', 'GE', 'DIS', 'M', 'C', 'JPM']
root = '/Users/xiaoxiao/USAnews_2017/'

error_code = []
for code in code_list:
    path = root + code
    '''
    try:
        creatfile(path)
    except:
        print('file exist'''''
    # datetime_update = '2016-08-09T12:28:00'
    datetime_update = '2016-12-31T00:00:00'
    flag = True
    while(flag):
        print(code)
        print(datetime_update)
        url = 'https://api.wsj.net/api/slinger/headlines/806/20?direction=older&datetime=' + datetime_update + '&opProp=symb!~!US:' + code
        req = urllib.Request(url)
        req.add_header("user-agent", "Mozilla/5.0")
        req.add_header("Accept", "application/json")
        request = urllib.urlopen(req)
        news_jsonstr = request.read()

        news_dict = json.loads(news_jsonstr)

        if ('Summary' in news_dict['HeadlinesResponse'][0].keys()):
            summary = news_dict['HeadlinesResponse'][0]['Summary']
            print(len(summary))
        else:
            error_code.append(code)
            break

        for sum in summary:
            news = sum['Headline']
            if(sum['CreateTimestamp']['Value'] == datetime_update and len(summary)==1):
                flag = False

            datetime_update = sum['CreateTimestamp']['Value']
            date = datetime_update[:-9]
            if(date[:-6]!='2015'):

                with open(root + code + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    one = [date, news]
                    print(one)
                    writer.writerow(one)
                '''
                fileObject = open(root + code + '/' + date + '.txt', 'a')
                fileObject.write(news)
                fileObject.write('\n')
                fileObject.close()'''
            else:
                flag = False
                break
        time.sleep(3)
print(error_code)


