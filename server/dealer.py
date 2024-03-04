import re
from time import time

import xmltodict
from flask import Request

from component.message import Message


def function_chooser(func, args):
    return func(args)


class Dealer:
    @staticmethod
    def get_xml_list(request: Request):
        # 必须重载
        pass

    @staticmethod
    def create_message_text(xml_list: list, content: str):
        # 创建一个消息字符串并将其参数格式化
        xml_dict = {
            "xml": {
                "ToUserName": xml_list[1],
                "FromUserName": xml_list[0],
                "CreateTime": int(time()),
                "MsgType": "text",
                "Content": content
            }
        }
        return xmltodict.unparse(xml_dict)
    
    @staticmethod
    def create_message_text(xml_list: list, content: str):
        # 创建一个消息字符串并将其参数格式化
        xml_dict = {
            "xml": {
                "ToUserName": xml_list[1],
                "FromUserName": xml_list[0],
                "CreateTime": int(time()),
                "MsgType": "text",
                "Content": content
            }
        }
        return xmltodict.unparse(xml_dict)

    @staticmethod
    def deal(request: Request):
        # 务必重载
        if request.data:
            type_list = ["text", "event"]
            function_list = [MessageDealer.deal, EventDealer.deal]
            xml = xmltodict.parse(request.data).get("xml", {})
            msg_type = xml.get("MsgType", "error")
            if xml == "error":
                return "msg_type error"
            for current_type, func in zip(type_list, function_list):
                if current_type == msg_type:
                    return function_chooser(func, xml)
        else:
            return "data is none"


class MessageDealer(Dealer):
    @staticmethod
    def get_xml_list(xml_dict: dict):
        to_user_name = xml_dict.get("ToUserName", False)
        from_user_name = xml_dict.get("FromUserName", False)
        content = xml_dict.get("Content", False)
        xml_list = [to_user_name, from_user_name, content]
        if all(xml_list):
            return xml_list
        else:
            return False

    @staticmethod
    def keywords_matcher(content):
        keys = ["华为", "原神", "熊金涛"]
        for key in keys:
            if re.search(key, content):
                return Message.get_keyword(key)
        return Message.get_keyword("nothing")

    @staticmethod
    def rules_matcher(content):
        if content == "帮助":
            return Message.get_help()
        rules = [r"^([\u4e00-\u9fa5]{2,10}) ([\u4e00-\u9fa5]{2,10}) 天气$", r"(.*) ([\u4e00-\u9fa5]) 查词"]
        # functions = [Message.get_weather, Message.translation]
        # for rule,func in zip(rules, functions):
        #     match = re.match(rule, content)
        #     if match:
        #         function_chooser(func, )
        match = re.match(rules[0], content)
        if match:
            province = match.group(1)
            city = match.group(2)
            return Message.get_weather(province, city)
        match = re.match(rules[1], content)
        if match:
            word = match.group(1)
            le = match.group(2)
            return Message.translation(word, le)

        else:
            return False

    @staticmethod
    def deal(xml_dict: dict):
        xml_list = MessageDealer.get_xml_list(xml_dict)
        print(xml_list)
        if xml_list:
            content = xml_list[2]
            message = MessageDealer.rules_matcher(content)
            if message:
                return MessageDealer.create_message_text(xml_list, message)
            else:
                message = MessageDealer.keywords_matcher(content)
                return MessageDealer.create_message_text(xml_list, message)
        else:
            return ""


class EventDealer(Dealer):
    @staticmethod
    def get_xml_list(xml_dict: dict):
        to_user_name = xml_dict.get("ToUserName", False)
        from_user_name = xml_dict.get("FromUserName", False)
        event = xml_dict.get("Event", False)
        xml_list = [to_user_name, from_user_name, event]
        if all(xml_list):
            return xml_list
        else:
            return False

    @staticmethod
    def deal(xml_dict: dict):
        xml_list = EventDealer.get_xml_list(xml_dict)
        if xml_list:
            event = xml_list[2]
            if event == "subscribe":
                message = Message.get_help()
                return EventDealer.create_message_text(xml_list, message)
        else:
            return ""
