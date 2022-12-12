import pandas as pd
import re
import string
from collections import Counter

file_name = 'mev1010'
file_name = 'flashbots1010'
df = pd.read_csv('data/%s.csv'%file_name)

stopwords = [line.strip() for line in open('data/english_stop.txt', 'r', encoding='utf-8').readlines()]
def cut_word(s):
    s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str(s))
    s = re.sub("[0-9]", " ", s)
    s = s.replace('#','punc_not_remove')
    s = re.sub("\W", " ", s)
    s = s.replace('punc_not_remove','#')
    sa = s.split(' ')
    outstr = ''

    for word in sa:
        word1 = re.sub("[#a-zA-Z]", "", word)
        if len(word1) == 0 and word.lower() not in stopwords and len(word) > 2:
            outstr += word
            outstr += " "
    return outstr[:-1]
df['div_result'] = df["Tweets"].apply(cut_word) 

result = Counter(" ".join(df['div_result'].values).split(' '))
cipin_sort = sorted(result.items(), key=lambda x: x[1], reverse=True)
df_cipin = pd.DataFrame(cipin_sort, columns=['word','word_freq'])
df_cipin.to_csv('data/%s freq.csv' % file_name, index=None)

key_word = list(df_cipin['word'][:40])
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
df['div_result'].apply(get_num)      

edge = []
for item,value in num.items():
    edge.append([item[0],item[1],value])
dff = pd.DataFrame(edge, columns=['Source','Target','Weight'])
dff.to_csv('data/%s edge.csv' % file_name,index=None)
