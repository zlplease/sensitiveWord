import sys
from dfa import DFA
from solve import transform
from wordCloud import wordCloud

if __name__ == '__main__':

    test = DFA()
    #  读入敏感词
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        sensitiveWords = f.readlines()
        count = 0
        for keyword in sensitiveWords:
            test.initWords(keyword.strip())
            finalKey, pinyinKey = transform(keyword.strip())
            for i in pinyinKey:
                test.generate_dict1(i, count)
            for i in finalKey:
                test.generate_dict(i, count)
            # for i in pinyinKey:
            #   test.generate_dict1(i,count)
            count += 1
        # test.print_dic()

    # 读入待检测文本
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        detectedText = f.readlines()
        for i in range(len(detectedText)):
            test.filter(detectedText[i].strip(), i + 1)

    # 将答案写入特定文件
    with open(sys.argv[3], 'a', encoding='utf-8') as w:
        ans = test.getAnswer()
        for item in ans:
            w.write(item + '\n')

    # 渲染词云图
    # wordCloud(test.sensitiveWords,test.counts)
