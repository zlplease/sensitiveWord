import sys
import os
from dfa import DFA
from pypinyin import lazy_pinyin
from solve import transform

if __name__ == '__main__':

  test = DFA()
  #读入敏感词
  with open(sys.argv[1],'r',encoding='utf-8') as f:
    sensitiveWords = f.readlines()
    for keyword in sensitiveWords:
      finalKey = transform(keyword.strip())
      for i in finalKey:
        test.generate_dict(i)

  #读入待检测文本
  with open(sys.argv[2],'r',encoding='utf-8') as f:
    detectedText = f.readlines()
    for i in range(len(detectedText)):
      print(detectedText[i].strip())

  #将答案写入特定文件
  with open(sys.argv[3],'a',encoding='utf-8') as w:
    w.write('hello world!')