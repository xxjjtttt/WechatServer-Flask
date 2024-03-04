import re
from random import randint

from flask import json

from component.spider import Proxy


class Message:
    @staticmethod
    def get_keyword(key):
        if key == "nothing":
            messages = ["你发的诗歌集吧 看球不懂🤣👉", "你发的我真的看不懂啦 😋"]
        else:
            keyword_dict = {
                "华为": ["遥遥领先", "遥遥领先于同行", "不用华为就是不爱国"],
                "原神": ["我们就是玩玩游戏，怎么你了", "原神启动", "我就是米哈游的Gog /手动狗头"],
                "熊金涛": ["涛哥的吊炸了", "That thing from Brother Tao is really quite big"],
                "蔡徐坤": ["鸡🐔你太美，贝贝"]
            }
            messages = keyword_dict.get(key, ["你发的诗歌集吧 看球不懂🤣👉", "你发的我真的看不懂啦 😋"])
        message = messages[randint(0, 100) % (len(messages))]
        return message

    @staticmethod
    def get_weather(province, city):
        province_dict = {
            "北京市": "BJ", "上海市": "SH", "天津市": "TJ", "重庆市": "CQ", "河北省": "HE", "山西省": "SX",
            "内蒙古自治区": "NM", "辽宁省": "LN", "吉林省": "JL", "黑龙江省": "HL", "江苏省": "JS", "浙江省": "ZJ",
            "安徽省": "AH", "福建省": "FJ", "江西省": "JX", "山东省": "SD", "河南省": "HA", "湖北省": "HB",
            "湖南省": "HN",
            "广东省": "GD", "广西壮族自治区": "GX", "海南省": "HI", "四川省": "SC", "贵州省": "GZ", "云南省": "YN",
            "西藏自治区": "XZ", "陕西省": "SN", "甘肃省": "GS", "青海省": "QH", "宁夏回族自治区": "NX",
            "新疆维吾尔族自治区": "XJ", "台湾省": "TW", "香港特别行政区": "HK", "澳门特别行政区": "MO"
        }

        p = ""
        for key, value in province_dict.items():
            if re.search(province, key):
                p = value
                break

        statonid_url = f"http://www.nmc.cn/rest/province/A{p}"
        print(statonid_url)

        city_list = list(json.loads(Proxy.get_response(statonid_url, False).text))

        stationid = "error"
        for item in city_list:
            c = item["city"]
            if re.search(city, c):
                stationid = item["code"]

        weather_url = f"http://www.nmc.cn/rest/weather?stationid={stationid}"
        print(weather_url)
        weather = json.loads(Proxy.get_response(weather_url, False).text)

        # air_current = weather["data"]["air"]["text"]
        # wind_current = [weather["data"]["real"]["wind"]["direct"],weather["data"]["real"]["wind"]["power"]]
        # warn_current = weather["data"]["real"]["warn"]["issuecontent"]
        temperature_current = weather["data"]["real"]["weather"]["temperature"]
        feel_temperature_current = weather["data"]["real"]["weather"]["feelst"]
        weather_current = weather["data"]["real"]["weather"]["info"]

        temperature_predict: list = weather["data"]["tempchart"]
        predict = []

        for temperature in temperature_predict:
            if temperature["day_img"] != "9999":
                time = temperature["time"]
                max_temp = temperature["max_temp"]
                min_temp = temperature["min_temp"]
                day_text = temperature["day_text"]
                night_text = temperature["night_text"]
                if night_text == day_text:
                    weather_text = night_text
                else:
                    weather_text = f"{day_text}转{night_text}"
                predict.append([time, max_temp, min_temp, weather_text])

        message = (f"{province}{city}:\n"
                   f"实时天气{weather_current}\n"
                   f"室外温度{temperature_current}℃ ")

        if feel_temperature_current != 9999.0:
            print(feel_temperature_current)
            message += f" 体感温度{feel_temperature_current}℃"

        message += f"\n天气预报:\n"

        for data in predict:
            message += (f"{data[0]}:\n"
                        f"天气{data[3]} "
                        f"温度{data[1]}-{data[2]}℃\n")
        return message

    @staticmethod
    def translation(word,language="英",num=5):
        if word:
            language_dict = {
                "英": "en", "法": "fr", "日": "ja", "韩": "ko"
            }
            le = language_dict.get(language, "en")
            print(word, num, language)
            url = f"https://dict.youdao.com/suggest?&num={num}&doctype=json&le={le}&q={word}"
            try:
                explain_json = json.loads(Proxy.get_response(url, False).text)["data"]["entries"]
            except:
                return "这好像不是一个词 换个词试试吧"
            message = f"{word}:\n"
            for index, entry in enumerate(explain_json):
                message += f"{index + 1}:{entry['entry']}\nexplain:{entry['explain']}\n"
            return message
        else:
            return "你想查啥词啊 我都找求不到"

    @staticmethod
    def get_help():
        message = ("欢迎，下面是使用方法：\n"
                   "1.执行任务\n"
                   "a.天气查询任务：\n"
                   "输入“{省份} {城市} 天气”\n"
                   "b.查词任务\n"
                   "输入{单词} {语言} 查词\n"
                   "语言支持：英、法、日、韩\n"
                   "\n2.一些无聊的关键词，自个来探索\n"
                   "tips:输入{帮助} 重新获取本消息\n"
                   "还有更多项目正在开发中🤔")
        return message