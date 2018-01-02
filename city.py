#! python3
# coding=utf8
import requests
from bs4 import BeautifulSoup


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

    def save_doc(self, path, doc_name, content):

    def pre_doc_content(self, pre_content):


a = City('aaa', '53478')
print(a.weather_week(a.content_from_page()))