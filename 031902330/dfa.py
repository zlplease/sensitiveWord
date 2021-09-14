from pypinyin import lazy_pinyin
import pypinyin
from solve import isMatch
class DFA:
  
  def __init__(self):
    self.keyword_chains = {}
    self.delimit = 'is_end'
    self.answer = []
    self.sensitiveWords = []
    self.total = 0

  def initWords(self,word):
    self.sensitiveWords.append(word)

 #构建嵌套字典
  def generate_dict(self, word,count):
    #统一英文为小写
    word = word.lower()
    #去除行首行尾空格和换行
    keyword = word.strip()
    #剔除为空的情况
    if not keyword:
      return
    level = self.keyword_chains
    for i in range(len(keyword)):
      if keyword[i] in level:
        level = level[keyword[i]]
      else:
        if not isinstance(level, dict):
          break
        for j in range(i,len(keyword)):
          level[keyword[j]] = {}
          last_level, last_keyword = level, keyword[j]
          level = level[keyword[j]]
        last_level[last_keyword] = {self.delimit: count}
        break
    if i == len(keyword) -1:
      level[self.delimit] = count


  #将拼音看作整体建立表格
  # def generate_dict1(self, word):
  #   word = list(word)
  #   if not word:
  #     return
  #   level = self.keyword_chains
  #   for i in range(len(word)):
  #     if word[i] in level:
  #       level = level[word[i]]
  #     else:
  #       if not isinstance(level, dict):
  #         break
  #       for j in range(i,len(word)):
  #         level[word[j]] = {}
  #         last_level, last_keyword = level, word[j]
  #         level = level[word[j]]
  #       last_level[last_keyword] = {self.delimit: True}
  #       break
  #   if i == len(word) -1:
  #     level[self.delimit] = True

  def getAnswer(self):
    self.answer.insert(0, 'Total: ' + str(self.total))
    return self.answer

  def print_dic(self):
    print(self.keyword_chains)

  # To Do 同音字和繁体拼音匹配
  def filter(self,text,line):
    text = text.lower()
    ret = []
    start = 0
    while start < len(text):
      level = self.keyword_chains
      step_ins = 0
      flag = 0
      for char in text[start:]:
          #匹配字典树
          if char in level:
              step_ins += 1
              flag = 1
              if self.delimit not in level[char]:
                  level = level[char]
              else:
                  ret.append(text[start:start+step_ins])
                  start += step_ins - 1
                  ans = ''.join(ret)
                  x = level[char]['is_end']
                  self.answer.append('line' + str(line) + ':' + ' <' + self.sensitiveWords[x] + '> ' + ans)
                  #记录恢复
                  flag = 0
                  ret = []
                  self.total += 1
                  break
          elif not isMatch(char) and flag == 1:
            step_ins += 1
          #To Do处理同音字以及繁体字
          elif lazy_pinyin(char)[0][0] in level:
            pinyin = lazy_pinyin(char)[0]
            for i in range(len(pinyin)):
              if pinyin[i] in level:
                if self.delimit not in level[pinyin[i]]:
                  level = level[pinyin[i]]
                elif ((self.delimit in level[pinyin[i]]) and (i == len(pinyin) -1)):
                # else:
                  # print((self.delimit in level[pinyin[i]]) and i == len(pinyin) -1)
                  # print(pinyin[i])
                  # print(pinyin[i] in level)
                  # print(i)
                  step_ins += 1
                  ret.append(text[start:start+step_ins])
                  start += step_ins - 1
                  ans = ''.join(ret)
                  x = level[pinyin[i]]['is_end']
                  print('line' + str(line) + ':' + ' <' + self.sensitiveWords[x] + '> ' + ans)
                  ret = []
                  flag = 0
                  self.total += 1
                  break
              else:
                break
               
          else:
            flag = 0
            break
      start += 1

