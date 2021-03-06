import asyncio
import re

from log import logger

import aiohttp

params = {
    "callback": "jsonp_queryMoreNums",
    "provinceCode": 97,
    "cityCode": 994,
    "monthFeeLimit": 0,
    "groupKey": 4200332935,
    "net": "01",
    "searchCategory": 3,
    "codeTypeCode": "",
    "advancePayLower": 0,
    "searchValue": "",
    "qryType": "02",
    "goodsNet": 4,
    "_": ""
}

card_dict = {
    # 4200332935: "黑龙江39元流量王",
    # 9301858665: "【生日号】黑龙江39元流量王;",
    # 4201858666: "【钻石号】黑龙江39元流量王;",
    # 9901858662: "【爱情号】黑龙江39元流量王;",
    # 49236584: "腾讯王卡-地王卡;阿里小宝卡（新）;",
    # 3901858663: "【发达号】黑龙江39元流量王;",
    # 2702314874: "AAA靓号】5G畅爽冰激凌-199档;",
    # 8401859252: "学霸号】黑龙江39元流量王;",
    # 7401858667: "红色号】黑龙江39元流量王;",
    # 5100255964: "5G畅爽冰激凌-159 AABB ABAB靓号;",
    36243047: "山东济南腾讯地王卡",
    17236695: "山东济南腾讯天王卡",
    3100271134: "山东济南冰激凌"
}

province_code = {
    "广东": 51,
    "黑龙江": 97,
    "山东":17
}

cite_code = {
    "哈尔滨": 971,
    "齐齐哈尔": 973,
    "牡丹江": 988,
    "佳木斯": 976,
    "绥化": 989,
    "大庆": 981,
    "鸡西": 991,
    "黑河": 990,
    "双鸭山": 994,
    "鹤岗": 993,
    "七台河": 992,
    "大兴安岭": 995,
    "济南":170
}

task_code = [
    # "00",
    # "11",
    # "06",
    # "41",
    # "42",
    # "46",
    # "49",
    # "64",
    # "74",
    "53",
    # "55",
    # "58",
    # "68"
]


async def get_liantong(params, province, city):
    async with aiohttp.ClientSession() as session:
        check_list = []
        with open("./result/联通result.txt", 'a+') as file_object:
            for search_value in task_code:
                for groupKey in card_dict.keys():
                    file_object.write('\n\n{}\n\n'.format(card_dict[groupKey]))
                    params['groupKey'] = groupKey
                    params['provinceCode'] = province_code[province]
                    params['cityCode'] = cite_code[city]
                    params['searchValue'] = search_value
                    for i in range(20):
                        async with session.get('http://num.10010.com/NumApp/NumberCenter/qryNum',
                                               params=params) as resp:
                            r = await resp.text()
                            try:
                                r_ = re.findall(r'[(](.*?)[)]', r)
                                r_dict = eval(r_[0])
                                num_list_from = r_dict['numArray']
                                num_list = [i for i in num_list_from if len(str(i)) == 11]
                                if not num_list:
                                    print("no{0}".format(search_value))
                                    break

                                key_list = [str(x) for x in num_list if
                                            x not in check_list and str(x)[-2:] == search_value]
                                if key_list:
                                    str_list = "，\n".join(key_list)
                                    check_list.extend(num_list)
                                    check_list = list(set(check_list))

                                    a_line = "，\n{0}".format(str_list)
                                    file_object.write(a_line)
                                    print("done:{0}".format(search_value))
                            except Exception as e:
                                logger.info(e)
        print("爬取任务已完成")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_liantong(params, "山东", "济南"))
    loop.close()
