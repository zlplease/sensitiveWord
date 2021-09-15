from typing import final
import unittest
import solve
from dfa import DFA
from os import path


class Test(unittest.TestCase):
    def test_isChinese(self):
        self.assertEqual(solve.isChinese('和'), True)
        self.assertEqual(solve.isChinese('h'), False)
        self.assertEqual(solve.isChinese('.'), False)

    def test_transform(self):
        global_ans = ['你好', '你hao', '你h', '你女子', 'ni好', 'nihao', 'nih', 'ni女子',
                      'n好', 'nhao', 'nh', 'n女子', '亻尔好', '亻尔hao', '亻尔h', ' 亻尔女子']
        separate_ans = [('你', '好'), ('你', 'hao'), ('你', 'h'), ('你', '女子'), ('ni', '好'),
                        ('ni', 'hao'), ('ni', 'h'), ('ni', '女子'), ('n', '好'), ('n', 'hao'), ('n', 'h'), ('n', '女子'),
                        ('亻尔', '好'), ('亻尔', 'hao'), ('亻尔', 'h'), ('亻尔', '女子')]
        global_test, separate_test = solve.transform('你好')
        self.assertEqual(global_test.sort(), global_ans.sort())
        self.assertEqual(separate_test.sort(), separate_ans.sort())

    def test_DFAfilter(self):
        sensitiveWord = ['哈利波特', '作家']
        texts = ['《哈利·波$!*&特是英国zjJ.K.罗琳（J. K. Rowling）于1997～2007年所著的魔幻文学系列小说，共7部。',
                 '其中前六部以霍哥沃z魔法学校（Hogwarts School of Witchcraft and Wizardry）为主要舞台，描写的是主人公——年轻的巫师学生h利·波特在霍格沃茨前后六年的学习生活和冒险故事',
                 '第七本描写的是hl&*%^·b特在第二次魔法界大战中在外寻找魂器并消灭fd的故事。']
        ans = ['Total: 4', 'line1: <哈利波特> 哈利·波$!*&特', 'line1: <作家> zj', 'line2: <哈利波特> h利·波特',
               'line3: <哈利波特> hl&*%^·b特']
        test = DFA()
        count = 0
        for keyword in sensitiveWord:
            test.initWords(keyword.strip())
            finalKey, pinyinKey = solve.transform(keyword.strip())
            for i in pinyinKey:
                test.generate_dict1(i, count)
            for i in finalKey:
                test.generate_dict(i, count)
            count += 1

        for i in range(len(texts)):
            test.filter(texts[i].strip(), i + 1)

        answer = test.getAnswer()
        self.assertEqual(ans, answer)

    def test_IOError(self):
        try:
            with open(path.join(path.dirname(__file__), 'chai_zi.json'), 'r', encoding='utf-8') as f:
                f.close()
        except IOError:
            print('IOError:未找到文件或读取文件失败')
        else:
            print("文件读取成功")


if __name__ == '__main__':
    unittest.main()
