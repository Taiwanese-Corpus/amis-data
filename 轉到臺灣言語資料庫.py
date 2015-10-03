from json import load
import re
import yaml


class 轉到臺灣言語資料庫:
    萌典檔名 = 'dict-amis.json'
    目標檔名 = 'dict-amis.yaml'
    解釋格式 = re.compile('￹(.*)￺(.*)￻(.*)')

    def 轉成資料庫yaml(self):
        全部資料 = {
            '來源': {'名': '方敏英',
                   '書名': "Virginia Fey's Amis Dictionary",
                   '音標改寫原民會版': '吳明義老師'},
            '版權': 'Creative Commons 姓名標示-非商業性 3.0 Unported License',
            '著作所在地': '臺灣',
            '著作年': '1980',
            '語言腔口': '阿美語',
            '相關資料組': [],

        }
        相關資料組 = 全部資料['相關資料組']
        for 族語, 華語, 種類 in self.整理族語華語對齊詞條():
            相關資料組.append(
                {
                    '種類': 種類,
                    '外語語言': '華語',
                    '外語資料': 華語,
                    '下層': [{'文本資料': 族語}],
                }
            )
        with open(self.目標檔名, 'w') as 檔案:
            yaml.dump(全部資料, 檔案, default_flow_style=False, allow_unicode=True)

    def 整理族語華語對齊詞條(self):
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
        yield 族語, 華語詞義, '字詞'
        try:
            example = definition.pop('example')
            for 例 in example:
                解析 = self.解釋格式.match(例)
                族語句 = 解析.group(1)
                華語句 = 解析.group(3)
                yield 族語句, 華語句, '語句'
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

for 結果 in 轉到臺灣言語資料庫().整理族語華語對齊詞條():
    print(結果)

轉到臺灣言語資料庫().轉成資料庫yaml()
