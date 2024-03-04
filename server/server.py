from hashlib import sha1

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
       