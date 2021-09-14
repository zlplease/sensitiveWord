from pypinyin import lazy_pinyin
from solve import isMatch,  isChinese
class DFA:
  
  def __init__(self):
    self.keyword_chains = {}
    self.delimit = 'is_end'
    self.answer = []
    self.sensitiveDic = {}
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
      


  def print_dic(self):
    print(self.sensitiveWords)

  def sensitiveEqual(self,finalKey):
    for i in range(len(finalKey)):
      key = finalKey[0]
      value = finalKey[i]
      self.sensitiveDic.setdefault(key,[]).append(value)

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
          #匹配
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
                  print('line' + str(line) + ':' + ' <' + self.sensitiveWords[x] + '> ' + ans)
                  flag = 0
                  ret = []
                  self.total += 1
                  break
          elif not isMatch(char) and flag == 1:
            step_ins += 1
          else:
            flag = 0
            break
      start += 1

