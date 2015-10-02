from json import load
import re


class 轉到臺灣言語資料庫:
    萌典檔名 = 'dict-amis.json'
    目標檔名 = 'dict-amis.yaml'
    解釋格式 = re.compile('￹(.*)￺(.*)￻(.*)')

    def 轉(self):
        '''
            "def":
        "definitions":
            "example":
    "heteronyms":
            "synonyms":
    "title":
'''
        with open(self.萌典檔名) as 檔案:
            for 一筆族語 in load(檔案):
                族語 = 一筆族語['title']
                for heteronym in 一筆族語['heteronyms']:
                    for definition in heteronym['definitions']:
                        for 結果 in self._definitions(族語, definition):
                            yield 結果

    def _definitions(self, 族語, definition):
        華語詞義 = self.解釋格式.match(definition['def']).group(3)
        yield 族語, 華語詞義
        try:
            example=definition.pop('example')
            for 例 in example:
                解析 = self.解釋格式.match(例)
                族語句 = 解析.group(1)
                華語句 = 解析.group(3)
                yield 族語句, 華語句
        except KeyError:
            pass
        try:
            synonyms = definition.pop('synonyms')
        except KeyError:
            pass
        else:
            for synonym in synonyms:
                for 結果 in self._definitions(synonym, definition):
                    yield 結果

for 結果 in 轉到臺灣言語資料庫().轉():
    print(結果)
