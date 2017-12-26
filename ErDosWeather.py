# coding=utf8
import requests
import docx
from bs4 import BeautifulSoup

# for index, weatherLine in enumerate(weatherLines):
#       print(index, weatherLine)

# for i in range(20):
#       if i < 10:
#             print(weatherLines[1 + i * 8])
#       else:
#             print(weatherLines[2 + i * 8])

d =  docx.Document('weatherTemplate.docx')
for table in d.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)


def weatherraw():
    url = 'http://wisdom.tqonline.top/weiqixiang/tianqi/getforecastbystations?' \
             'stations=[53562,53469,53475,53484,53487,54449,53478,53574,53578,53575]'
    r = requests.get(url)
    weathersoup = BeautifulSoup(r.content, "html.parser")
    return weathersoup.body


def weatherlist():
    weatherrawlines = str(weatherraw()).split("<br/>")
    for index, weatherLine in enumerate(weatherrawlines):
        weatherrawlines[index] = weatherrawlines[index].strip()
    while '' in weatherrawlines:
        weatherrawlines.remove('')
    return weatherrawlines



