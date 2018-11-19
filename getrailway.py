# -*- coding: utf-8 -*-
'''
获取12306城市名和城市代码的数据
文件名： parse_station.py
'''
import requests
import re
import json
import urllib


# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()


def getStation():
    # 12306的城市名和城市代码js文件url
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
    r = requests.get(url, verify=False)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = re.findall(pattern, r.text)
    station = dict(result)  # {'北京北': 'VAP', '北京东': 'BOP', '北京': 'BJP',
    # print(station)
    return station


'''
查询两站之间的火车票信息
输入参数： <date> <from> <to>
12306 api:
'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SZH&purpose_codes=ADULT'
'''

all_data =  '2018-11-20'

# 生成查询的url
def get_query_url(text):
    # 城市名代码查询字典
    # key：城市名 value：城市代码

    try:
        date = all_data
        from_station_name = '南宁'
        to_station_name = '北海'
        from_station = text[from_station_name]
        to_station = text[to_station_name]
    except:
        date, from_station, to_station = '--', '--', '--'
        # 将城市名转换为城市代码

    # api url 构造
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
    # print(url)

    return url


# 获取信息
def query_train_info(url, text):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''
    print(url)

    info_list = []
    price_list = []
    try:
        r = requests.get(url, verify=False)

        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']

        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_number = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = text['南宁']
            # 终点站
            to_station_code = data_list[7]
            to_station_name = text['北海']
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'

            # 列车序列号
            train_no = data_list[2]
            # 出发站序列号
            from_station_no = data_list[16]
            # 终点站序列号
            to_station_no = data_list[17]
            # 类型
            seat_types = data_list[35] or 'OMO'
            # 列车日期
            train_date = all_data

            # https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=77000D179310&from_station_no=11&to_station_no=14&seat_types=OMO&train_date=2018-11-20
            # api url 构造
            price_url = (
                'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
                'train_no={}&'
                'from_station_no={}&'
                'to_station_no={}&'
                'seat_types={}&'
                'train_date={}'
            ).format(train_no, from_station_no, to_station_no, seat_types, train_date)

            print(price_url)

            re = requests.get(price_url, verify=False)
            ticket_price = re.json()['data']
            print(ticket_price)
            # first_class_seat_price = ticket_price['M']
            # second_class_seat_price = ticket_price['O']
            # no_seat_price = ticket_price['WZ']


            # 打印查询结果
            info = (
            '车次:{}\n出发站:{}\n目的地:{}'
            '\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n'
            '座位情况：\n 一等座：「{}」 \n二等座：「{}」\n软卧：「{}」'
            '\n硬卧：「{}」\n硬座：「{}」\n无座：「{}」\n\n'.format(
                train_number, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
                second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))

            # print(info)
            # info_list.append(info)

        return info_list
    except:
        return ' 输出信息有误，请重新输入'


text = getStation();
url = get_query_url(text)

query_train_info(url, text)