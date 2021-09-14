from pypinyin import lazy_pinyin

class DFA:
  
  def __init__(self):
    self.keyword_chains = {}
    self.delimit = 'is_end'

 #构建嵌套字典
  def generate_dict(self, word):
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
        last_level[last_keyword] = {self.delimit: True}
        break
    if i == len(keyword) -1:
      level[self.delimit] = True

  # def print_dic(self):
  #   print(self.keyword_chains)

