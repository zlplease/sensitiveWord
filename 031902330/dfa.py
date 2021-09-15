from pypinyin import lazy_pinyin
from solve import isMatch


class DFA:

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = 'is_end'
        self.answer = []
        self.sensitiveWords = []
        self.counts = []
        self.total = 0

    def initWords(self, word):
        self.sensitiveWords.append(word)
        self.counts.append(0)

    # 构建嵌套字典
    # def generate_dict(self, word,count):
    #   #统一英文为小写
    #   word = word.lower()
    #   #去除行首行尾空格和换行
    #   keyword = word.strip()
    #   #剔除为空的情况
    #   if not keyword:
    #     return
    #   level = self.keyword_chains
    #   for i in range(len(keyword)):
    #     if keyword[i] in level:
    #       level = level[keyword[i]]
    #     else:
    #       if not isinstance(level, dict):
    #         break
    #       for j in range(i,len(keyword)):
    #         level[keyword[j]] = {}
    #         last_level, last_keyword = level, keyword[j]
    #         level = level[keyword[j]]
    #       last_level[last_keyword] = {self.delimit: count}
    #       break
    #   if i == len(keyword) -1:
    #     level[self.delimit] = count

    # 转换为拼音建树,但要考虑时间成本
    def generate_dict(self, word, count):
        # 统一英文为小写
        word = word.lower()
        # 去除行首行尾空格和换行
        keyword = word.strip()
        # 剔除为空的情况
        if not keyword:
            return
        level = self.keyword_chains
        for i in range(len(keyword)):
            x = lazy_pinyin(keyword[i])[0]
            if x in level:
                level = level[x]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(keyword)):
                    y = lazy_pinyin(keyword[j])[0]
                    level[y] = {}
                    last_level, last_keyword = level, y
                    level = level[y]
                last_level[last_keyword] = {self.delimit: count}
                break
        if i == len(keyword) - 1:
            level[self.delimit] = count

    # 将偏旁部首拆分并加入字典
    # def generate_dict1(self, word, count):
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
    #       last_level[last_keyword] = {self.delimit: count}
    #       break
    #   if i == len(word) -1:
    #     level[self.delimit] = count

    # 转换为拼音建树,但要考虑时间成本
    def generate_dict1(self, word, count):
        word = list(word)
        if not word:
            return
        level = self.keyword_chains
        for i in range(len(word)):
            x = lazy_pinyin(word[i])[0]
            if x in level:
                level = level[x]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(word)):
                    y = lazy_pinyin(word[j])[0]
                    level[y] = {}
                    last_level, last_keyword = level, y
                    level = level[y]
                last_level[last_keyword] = {self.delimit: count}
                break
        if i == len(word) - 1:
            level[self.delimit] = count

    def getAnswer(self):
        self.answer.insert(0, 'Total: ' + str(self.total))
        return self.answer

    def print_dic(self):
        print(self.counts)

    # To Do 同音字和繁体拼音匹配
    def filter(self, texts, line):
        text = texts.lower()
        ret = []
        start = 0
        while start < len(text):
            level = self.keyword_chains
            step_ins = 0
            flag = 0
            for char in text[start:]:
                # 匹配字典树
                if char in level:
                    step_ins += 1
                    flag = 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(texts[start:start + step_ins])
                        start += step_ins - 1
                        ans = ''.join(ret)
                        x = level[char]['is_end']
                        self.counts[x] += 1
                        self.answer.append('line' + str(line) + ':' + ' <' + self.sensitiveWords[x] + '> ' + ans)
                        # 记录恢复
                        flag = 0
                        ret = []
                        self.total += 1
                        break
                elif char not in level and lazy_pinyin(char)[0] in level:
                    pinyin = lazy_pinyin(char)[0]
                    step_ins += 1
                    flag = 1
                    if self.delimit not in level[pinyin]:
                        level = level[pinyin]
                    else:
                        ret.append(texts[start:start + step_ins])
                        start += step_ins - 1
                        ans = ''.join(ret)
                        x = level[pinyin]['is_end']
                        self.counts[x] += 1
                        self.answer.append('line' + str(line) + ':' + ' <' + self.sensitiveWords[x] + '> ' + ans)
                        # 记录恢复
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
