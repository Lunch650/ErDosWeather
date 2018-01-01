#! python3
# coding=utf8
import requests
from bs4 import BeautifulSoup


class City():
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
                self.page_content = BeautifulSoup(request.content, 'html.parser').body
                return self.page_content
            except requests.Timeout:
                print(self.__name + 'mission:页面加载连接超时，加载任务重新启动中')

    @staticmethod
    def content_list(mess_str):
        # 去除页面中不相干行数，返回干净的List数据
        if mess_str is not '':
            templines = str(mess_str).split("<br/>")
            return [n.strip() for n in templines if (n.strip() != '') and (n.find('<') < 0)]
        else:
            print('错误')
            return None


a = City('薛家湾', '53553')
a.content_from_page()
print('--------------------')
print(a.content_list(a.page_content))

