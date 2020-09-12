from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import csv, time, os, re, datetime

analyser = SentimentIntensityAnalyzer()
start = datetime.datetime.now()

# vaderSentiment
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    # print("{:-<40} {}".format(sentence, str(score)))
    return (score['compound'])

result = 'pvec100'
sentiment = 'sentiment(100)'

filedir = "/Users/xiaoxiao/dataset/U_Stock/"
sentimentfolderdir = filedir + "USAnews_1617/"
csvfolderdir = filedir + "USAnews_1617(pre)/"

# read files
fnames = os.listdir(sentimentfolderdir)
for newsfile in fnames:
    if 'DS_S' in newsfile:
        fnames.remove(newsfile)


for newsfile in fnames:
    compid = newsfile[:-4]
    filename = sentimentfolderdir + compid + '.csv'
    end = datetime.datetime.now()
    print('正在分析', compid, "用时：" + str(end - start))


    data = pd.read_csv(filename, engine='python', header=None)
    sentimentdict = {}

    # 计算分数
    for i in range(len(data[0])):
        if data[0][i] in sentimentdict.keys():
            try:
                sentimentdict[data[0][i]] += sentiment_analyzer_scores(data[1][i])
            except:
                print('something wront with', compid)
        else:
            sentimentdict[data[0][i]] = 0.0

    with open(csvfolderdir + compid + result + '.csv', 'r') as csvinput:
        with open(filedir + '/' + sentiment + '/' + compid + '.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            # print(reader)
            all = []
            row = next(reader)
            for i in range(1,101):
                row.append(i)
            row.append('SentimentScore')
            all.append(row)
            for row in reader:
                try:
                    if(sentimentdict[row[0]]!='time'):
                        row.append(sentimentdict[row[0]])
                except:
                    row.append(0.0)
                all.append(row)
            writer.writerows(all)
