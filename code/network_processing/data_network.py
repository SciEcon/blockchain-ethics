import pandas as pd
import re
import string
from collections import Counter

file_name = 'mev1010'
file_name = 'flashbots1010'
df = pd.read_csv('data/%s.csv'%file_name)

stopwords = [line.strip() for line in open('data/英文stop.txt', 'r', encoding='utf-8').readlines()]
def cut_word(s):
    """
    分词
    :return:
    """
    # 删除网址
    s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str(s))
    # 去除数字
    s = re.sub("[0-9]", " ", s)
    s = s.replace('#','不删的标点')
    # 去除标点
    s = re.sub("\W", " ", s)
    
    s = s.replace('不删的标点','#')
    # 分词
    sa = s.split(' ')
    
    outstr = ''
    # 去停用词
    for word in sa:
        word1 = re.sub("[#a-zA-Z]", "", word)
        if len(word1) == 0 and word.lower() not in stopwords and len(word) > 2:
            outstr += word
            outstr += " "
    return outstr[:-1]
df['分词结果'] = df["Tweets"].apply(cut_word) 


# 计算词频
result = Counter(" ".join(df['分词结果'].values).split(' '))
# 排序
cipin_sort = sorted(result.items(), key=lambda x: x[1], reverse=True)
df_cipin = pd.DataFrame(cipin_sort, columns=['词','词频'])
df_cipin.to_csv('data/%s 词频.csv' % file_name, index=None, encoding='ANSI')

"""
共现次数
"""
# 词
key_word = list(df_cipin['词'][:40])
num = dict()
def get_num(s):
    s = s.split(' ')
    for i in range(len(key_word)):
        for j in range(i+1, len(key_word)):
            if key_word[i] in s and key_word[j] in s:
                if (key_word[i], key_word[j]) in num:
                    num[(key_word[i], key_word[j])] = num[(key_word[i], key_word[j])] + 1
                else:
                    num[(key_word[i], key_word[j])] = 1
df['分词结果'].apply(get_num)      

edge = []
for item,value in num.items():
    edge.append([item[0],item[1],value])
dff = pd.DataFrame(edge, columns=['Source','Target','Weight'])
dff.to_csv('data/%s edge.csv' % file_name,index=None)
