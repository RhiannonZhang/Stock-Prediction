import sys, datetime, os, csv, time
import gensim
import sklearn
import numpy as np
from gensim.models.doc2vec import Doc2Vec, LabeledSentence


TaggededDocument = gensim.models.doc2vec.TaggedDocument

def get_dataset(dir, filename):
    with open(dir + filename, 'r') as cf:
        docs = cf.read()
        # print ('行数：',len(docs))
    x_train = []
    # y = np.concatenate(np.ones(len(docs)))
    word_list = docs.split(',')
    l = len(word_list)
    word_list[l - 1] = word_list[l - 1].strip()
    document = TaggededDocument(word_list, tags=[i])
    x_train.append(document)
    return x_train


def getVecs(model, corpus, size):
    vecs = [np.array(model.docvecs[z.tags[0]].reshape(1, size)) for z in corpus]
    return np.concatenate(vecs)



def train(x_train, dir, modelname, size=100):  # 100dim
    if not os.path.exists(dir + modelname + 'model100'):
        model_dm = Doc2Vec(x_train, min_count=10, window=3, vector_size=size, sample=1e-3, negative=5, workers=4)
    else:
        model_dm = Doc2Vec.load(dir + modelname + 'model100')
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=15)
    model_dm.save(dir + modelname + 'model100')
    return model_dm



def test(dir, modelname, test_text):
    model_dm = Doc2Vec.load(dir + modelname + 'model100')
    inferred_vector_dm = model_dm.infer_vector(test_text)
    # print (inferred_vector_dm)
    return inferred_vector_dm




if __name__ == '__main__':
    start = datetime.datetime.now()
    filedirs = ["/Users/xiaoxiao/dataset/U_Stock/USAnews_1617(pre)/"]
    # "/Users/xiaoxiao/dataset/U_Stock/USAnews_1617(pre)/",
    for filedir in filedirs:
        # print('正在读取文件……')
        fnames = os.listdir(filedir)
        alltxtnames = []
        modelnames = []
        foldernames = []
        timenames = []
        for i in fnames:
            if 'all.txt' in i:
                alltxtnames.append(i)
            elif 'model100' in i:
                modelnames.append(i)
            elif 'time' in i:
                timenames.append(i)
            elif 'csv' in i:
                pass
            elif 'DS_S' in i:
                pass
            else:
                foldernames.append(i)

        # print('开始建模……')
        # get model

        for filename in alltxtnames:
            x_train = get_dataset(filedir, filename)
                # if not os.path.exists(filedir + filename[:-4] + 'model100'):
            end = datetime.datetime.now()
            print('%s\t\t正在生成模型……\t%s' % (filename[:-7], str(end - start)))
            model_dm = train(x_train, filedir, 'USnews')


        for filename in foldernames:
            # open XXresult.csv and write in
            fnames = os.listdir(filedir + filename)
            for i in fnames:
                if 'DS_Store' in i:
                    fnames.remove(i)
            with open(filedir + filename + 'pvec100.csv', 'w', newline='')as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['time'])
                modelname = 'USnews'
                for txtname in fnames:
                    with open(filedir + filename + '/' + txtname, 'r') as cf:
                        docs = cf.read()
                    word_list = docs.split(' ')

                    result = list(test(filedir, modelname, word_list))
                    line = [txtname[:-4]]
                    # print(line)
                    writer.writerow(line + result)
            print('已将结果写入' + filedir + filename + 'pvec100.csv')