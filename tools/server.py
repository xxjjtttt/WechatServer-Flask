import re
from hashlib import sha1
from time import time

import xmltodict
from flask import Request



class Server:
    token = "testing"

    @staticmethod
    def get_token():
        return Server.token

    @staticmethod
    def get_request_list(request: Request):
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        return [signature, timestamp, nonce, echostr]

    @staticmethod
    def get_signature(request_list: list):
        string = "".join(sorted(request_list))
        return sha1(string.encode()).hexdigest()

    @staticmethod
    def check_signature(request: Request):
        request_list = Server.get_request_list(request)
        if not all(request_list):
            return False
        else:
            plaintext = [Server.get_token(), request_list[1], request_list[2]]
            ciphertext = Server.get_signature(plaintext)
            if ciphertext != request_list[0]:
                return False
            else:
                return True

    @staticmethod
    def bind_server(request: Request):
        if Server.check_signature(request):
            print("成功链接微信服务器与本地服务器")
            return request.args.get("echostr")
        else:
            print("收到请求,拒绝链接")
            return "false"

    @staticmethod
    def get_xml_list(request: Request):
        if request.data:
            xml_dict = xmltodict.parse(request.data).get("xml", {})
            to_user_name = xml_dict.get("ToUserName")
            from_user_name = xml_dict.get("FromUserName")
            msg_type = xml_dict.get("MsgType")
            content = xml_dict.get("Content")
            return [to_user_name, from_user_name, msg_type, content]

    @staticmethod
    def create_message(xml_list: list, content: str):
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
    def get_content(func, *args):
        return func(*args)

    @staticmethod
    def send_message(request: Request):
        msg_list = Server.get_xml_list(request)
        content = Server.commander(msg_list[3])
        return Server.create_message(msg_list, content)

    # 用来控制使用哪个content maker
    @staticmethod
    def commander(content):
        # 这里编写content策略
        match = re.match(pattern, content)
        if re.search(r"华为", content):
            return "华为，遥遥领先"
        elif re.search(r"原神", content):
            return "原神~启动！"
        else:
            return "你发的是什么归"
