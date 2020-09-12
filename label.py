import csv
# price-change (6,1) = (5,1)-(5,0),
# pchange (7,1) = (6,1)/(5,0)*100
# https://finance.yahoo.com/quote/CSCO/history?period1=1483113600&period2=1514649600&interval=1d&filter=history&frequency=1d
# url = 'https://finance.yahoo.com/quote/JPM/history?period1=1483113600&period2=1514649600&interval=1d&filter=history&frequency=1d'


nlist = ['AMZN', 'AAPL', 'CMCSA', 'GOOG', 'MS', 'WMT', 'INTC', 'GS',
         'BLK', 'BAC', 'FB', 'MSFT', 'NFLX', 'F', 'XOM', 'BA', 'GE',
         'DIS', 'M', 'C', 'JPM', 'VZ', 'AGN', 'PFE', 'CBS', 'PEP', 'UPS',
         'JCP', 'MA', 'HD', 'LMT', 'JNJ', 'TGT', 'S', 'CMG', 'IBM',
         'NDAQ', 'SBUX', 'KR', 'NVDA', 'KSS', 'BMY', 'NKE', 'LUV']

for n in nlist:
    r = csv.reader(open('/Users/xiaoxiao/dataset/U_Stock/uprice_1617/'+ n +'.csv')) # Here your csv file
    lines = [l for l in r]
    lines = lines[1:]
    # print lines
    i=0
    while(i<len(lines)):

        lines[i][5] = str(round(float(lines[i][4])-float(lines[i-1][4]),6))
        lines[i][6] = str(round(float(lines[i][5])/float(lines[i-1][4])*100,2))
        judge = round(float(lines[i][4]) - float(lines[i - 1][4]), 6)

        if (judge < 0):
            lines[i].append('-1')
        elif (judge == 0):
            lines[i].append('0')
        elif (judge > 0):
            lines[i].append('1')
        i = i + 1
    lines = lines[1:]
    print(lines)
    f = open('/Users/xiaoxiao/dataset/U_Stock/uprice_1617(label)/'+ n +'.csv','w')
    writer = csv.writer(f)
    # for line in lines:
    writer.writerows(lines)

