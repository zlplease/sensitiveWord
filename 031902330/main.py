import sys
import os

if __name__ == '__main__':
  #读入敏感词
  with open(sys.argv[1],encoding='utf-8') as f:
    sensitiveWords = f.readlines()

  #读入待检测文本
  with open(sys.argv[2],encoding='utf-8') as f:
    detectedText = f.readlines()

  #将答案写入特定文件
  with open(sys.argv[3],'a',encoding='utf-8') as w:
    w.write('hello world!')

  print(detectedText)