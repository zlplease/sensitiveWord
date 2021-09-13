#from pypinyin import lazy_pinyin

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

def solveOringin(text):
  pass