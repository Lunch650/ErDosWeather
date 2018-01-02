#! python3
# coding=utf8
import requests
from bs4 import BeautifulSoup
from docx import Document
from datetime import datetime, timedelta

def predocx():
    # 由模板生成两个word文件，分别对应8点钟版本及16点版本，并修改模板中的时间
    dt = datetime.now()
    d = Document('weatherTemplate.docx')
    d.paragraphs[1].text = '(' + dt.strftime('%Y') + '年第' + dt.strftime('%W') + '期）'
    d.paragraphs[3].text = dt.strftime('%Y') + '年' + dt.strftime('%m') + '月' + dt.strftime('%d') + '日'
    t = d.tables[0]
    for column in range(1, 8):
        dttemp = dt + timedelta(days=column)
        t.cell(0, column + 2).text = (dttemp.strftime('%m') + '月' + dttemp.strftime('%d') + '日')
    d.save(dt.strftime('%Y%m%d') + '08.docx')
    d.save(dt.strftime('%Y%m%d') + '16.docx')

class City(object):
    def __init__(self, city_name, city_code):
        self.__name = city_name
        self.__code = city_code
        self.__param = {'stations': '['+city_code+']'}
        self.__url = 'http://wisdom.tqonline.top/weiqixiang/tianqi/getforecastbystations'
        self.page_content = ''

    def print_city_info(self):
        print('城市名称为:' + self.__name + ';城市代码为:' + self.__code)

    def content_from_page(self):
        request = None
        while request is None:
            try:
                request = requests.get(self.__url, params=self.__param, timeout=10)
            except requests.Timeout:
                print(self.__name + 'mission:页面加载连接超时，加载任务重新启动中')
        self.page_content = BeautifulSoup(request.content, 'html.parser').body
        return self.page_content

    def weather_week(self, mess_str):
        if mess_str is not '':
            temp_split = str(mess_str).split("<br/>")
            temp_list = [n.strip() for n in temp_split if (n.strip() != '') and (n.find('<') < 0)]
            weather_week = self.separate_list(temp_list)
            return weather_week
        else:
            print('错误')
            return None

    @staticmethod
    def separate_list(prelist):
        if prelist is []:
            print('找不到需要处理的列表')
            return None
        if prelist.count('报歉，暂无预报数据。') == 2:
            print('报歉，' + str(prelist[0])[:-1] + '页面还未发布数据。')
            week = []
        elif prelist.count('报歉，暂无预报数据。') == 1:
            week = \
                [
                    [
                        d[d.index('：') + 1:] for d in prelist[1:prelist[1:].index(prelist[0]) + 1]
                    ],
                ]
        else:
            week = \
                [
                    [
                        d[d.index('：') + 1:] for d in prelist[1:prelist[1:].index(prelist[0]) + 1]
                    ],
                    [
                        s[s.index('：') + 1:] for s in prelist[prelist[1:].index(prelist[0]) + 2:]
                    ],
                ]
        return week

    def save_doc(self, path, doc_name, weekly_weather, start_row):
        doc = Document(path + doc_name)
        t = doc.tables[0]
        for column, daily_weather in enumerate(weekly_weather):
            daily_weather = self.format_daily(daily_weather)
            for row, daily_element in enumerate(daily_weather):
                t.cell((start_row * 3) + row + 1, column + 3).text = daily_element
        doc.save(path + doc_name)

    @staticmethod
    def format_daily(daily_weather):
        templist = daily_weather.split('，')
        temperature = templist[2][4:-1] + '~' + templist[3][4:-2]
        return [templist[0], temperature, templist[1]]


a = City('aaa', '53478')
print(a.weather_week(a.content_from_page()))