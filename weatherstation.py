#!python3
# coding=utf8
from city import City

if __name__ == '__main__':
    def __main():
        cities = {
            '53553': '准格尔旗',
            '53562': '清水河县',
            '53484': '丰镇',
            '53487': '大同',
            '54449': '秦皇岛',
            '53469': '和林格尔县',
            '53475': '凉城',
            '53478': '右玉',
            '53574': '平鲁',
            '53578': '朔州',
            '53575': '神池',
        }
        cities_order = \
            [
                '53553', '53562', '53469', '53475', '53484', '53487', '54449',
                '53469', '53475', '53478', '53574', '53578', '53575',
            ]

        City.predocx()
        print('今日数据模板准备完毕')
        for i, code in enumerate(cities_order):
            city = City(cities.get(code), code)
            weather = City.weekly_weather(city.content_from_page())
            if len(weather) > 0:
                City.save_doc(doc_name=City.doc_names[0], weekly_weather=weather[0], start_row=i)
                print(cities.get(code), '8点版本写入完成')
                if len(weather) > 1:
                    City.save_doc(doc_name=City.doc_names[1], weekly_weather=weather[1], start_row=i)
                    print(cities.get(code), '20点版本写入完成')
    __main()
