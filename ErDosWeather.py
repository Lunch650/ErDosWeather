# coding=utf8
import requests
from docx import Document
from bs4 import BeautifulSoup


def pagecontent():
    # TODO 需要catch
    url = 'http://wisdom.tqonline.top/weiqixiang/tianqi/getforecastbystations?' \
             'stations=[53553,53562,53469,53475,53484,53487,54449,53478,53574,53578,53575]'
    r = requests.get(url)
    weathersoup = BeautifulSoup(r.content, "html.parser")
    return weathersoup.body


def weatherlines():
    pagelines = str(pagecontent()).split("<br/>")
    weatherrawlines = [n.strip() for n in pagelines if (n.strip() != '') and (n.find('<') < 0) ]
    return weatherrawlines


def weatherdocx():
    d = Document('weatherTemplate.docx')
    t = d.tables[0]
    for column in range(len(t.columns)):
        for row in range(len(t.rows)):
            print('(' + str(row) + ',' + str(column) + ')' + t.cell(row, column).text)


if __name__ == '__main__':
    weatherlines = weatherlines()
    # TODO:需要对行数进行判断是否有内容或内容页数
    for index, weatherline in enumerate(weatherlines):
        print(index, ':', weatherline)
    # weatherlineone = weatherlines[:int(len(weatherlines)/2)]
    # for index, w in enumerate(weatherlineone):
    #     print(index,':', w)
    # weatherlinetwo = weatherlines[int(len(weatherlines)/2):]
    # for index, w in enumerate(weatherlinetwo):
    #     print(index, ':', w)
    #
    # 录入行数分别是1-7，9-15等下标
    # for j in range(int(len(weatherlines) / 8)):
    #     for i in range(1, 8):
    #         print(weatherlines[i + j * 8])
    #     print('-----------------------')
