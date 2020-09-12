import time
import nltk
import csv
import operator
import string
import sys
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def insert_data(each, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        one = each
        writer.writerow(one)

def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
def preprocess(text):
    text = re.sub('http://[a-zA-Z0-9.?/&=:]*', '', text)
    text = re.sub('https://[a-zA-Z0-9.?/&=:]*', '', text)
    text = re.sub('pic\.[a-zA-Z0-9.?/&=:]*', '', text)
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = re.sub('\s+', ',', text)
    word = ''
    finallist = []
    for each in text:
        if (each != ','):
            word = word + each
        else:

            word = string.lower(word)
            if (word not in stopworddic and len(word)>1):
            
                wnl = WordNetLemmatizer()
                word = wnl.lemmatize(word)
                if(word!=''):
                    finallist.append(str(word))
            word = ''
    print(finallist)
    return finallist

def sortCsvByDate(ori, new):
    with open(ori, 'rb') as f:
        reader = csv.reader(f)

        sortedlist = sorted(reader, key=operator.itemgetter(0), reverse=False) # sort
    # print sortedlist
    for each in sortedlist:
        pair = []
        pair.append(each[0])

        final = preprocess(each[1])
        pair.append(final)

        if(is_valid_date(pair[0])==True):
            insert_data(pair, new)

# nltk.download('stopwords')
# nltk.download('wordnet')
stopworddic = set(stopwords.words('english'))
nlist = ['AAPL','VZ', 'AGN', 'PFE', 'CBS', 'PEP', 'UPS', 'JCP', 'MA',
         'HD', 'LMT', 'JNJ', 'TGT', 'S', 'CMG', 'IBM', 'NDAQ',
         'SBUX', 'KR', 'NVDA', 'KSS', 'BMY', 'NKE', 'LUV', 'AMZN',
         'CMCSA', 'GOOG', 'MS', 'WMT', 'INTC', 'GS', 'BLK', 'BAC', 'FB',
         'MSFT', 'NFLX', 'F', 'XOM', 'BA', 'GE', 'DIS', 'M', 'C', 'JPM']
wrongcode = []
for n in nlist:
    oldf = '/Users/xiaoxiao/USAnews_2016(csv)/' + n + '.csv'
    newf = '/Users/xiaoxiao/USAnews_2016(pre)/' + n + '.csv'
    try:
        sortCsvByDate(oldf,newf)
    except:
        wrongcode.append(n)



