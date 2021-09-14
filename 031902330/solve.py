from pypinyin import lazy_pinyin
from itertools import product
from os import path
import json


#根据unicode判断是否为汉字
def isChinese(word):
  return '\u4e00' <= word <= '\u9fff'

#检测匹配项
def isMatch(word):
  if isChinese(word):
    return True
  if word.isalpha():
    return True
  if word == '/n':
    return True

#初始化文本
def initText(text):

  for index, item in enumerate(text):
    if not isMatch(item):
      text = text.replace(item, '')
  return text

#针对统一敏感词不同情况扩充树
def forest(sameDic):
  forest = []
  loop_val = []
  finalDic = []
  for key in sameDic:
    loop_val.append(sameDic[key])
  for i in product(*loop_val):
    forest.append(i)
  for i in range(len(forest)):
    newWord = ''
    for item in forest[i]:
      newWord += item
    finalDic.append(newWord)
  # return forest
  return finalDic

def transform(words):
  sameDic = {}
  for word in words:
    if isChinese(word):
      #汉字中拼音，偏旁拆分，首字母为同类
      key = word
      value = word
      sameDic.setdefault(key,[]).append(value)
      letter = lazy_pinyin(word)
      value = letter[0]
      sameDic.setdefault(key,[]).append(value)
      value = letter[0][0]
      sameDic.setdefault(key,[]).append(value)
      with open(path.join(path.dirname(__file__), 'chai_zi.json'), 'r', encoding='utf-8') as f:
        #读入json，将字符串转换为字典
        sideDic = json.load(f)
      if sideDic[word]:
        value = sideDic[word]
      sameDic.setdefault(key,[]).append(value)
    else:
      #字母大小写同类
      key = word.lower()
      value = key
      sameDic.setdefault(key,[]).append(value)
      value = key.upper()
      sameDic.setdefault(key,[]).append(value)
      
  return forest(sameDic)