import json
from random import random

import requests


class Proxy:

    @staticmethod
    def get_user_agent_local():
        user_agnet_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2736.97 Safari/537.36 Edge/18.18362",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.1933.16 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.0.10191 SLBChan/102",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:84.0) Gecko/20100101 Firefox/84.0"
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) QQBrowser/6.9.1 Safari/537.22",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; CIBA; 360SE)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/44.0.2403.130 Safari/537.36 QIHU 360SE",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; 126BROWSER; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",
            "360SE	Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        ]
        return user_agnet_list[int(random() * 100) % len(user_agnet_list)]


    @staticmethod
    def get_user_agent():
        # 巨量api 每日领取1k代理使用量
        api_url = "http://v2.api.juliangip.com/users/getUserAgent" \
                  + "?num=1&platform=win&user_id=1026166&sign=91e56c42d8c5419eb5d27ee40c3115a0"
        return json.loads(requests.get(api_url).text)["data"]["user_agent_list"][0]

    @staticmethod
    def get_headers():
        return {"User-Agent": Proxy.get_user_agent()}

    @staticmethod
    def get_proxy_ip():
        api_url = "http://v2.api.juliangip.com/dynamic/getips" \
                  + "?auto_white=1&num=1&pt=1&result_type=json" \
                  + "&trade_no=1134776592803734&sign=d10d803b46c50847381e0d39c264073a"
        json_proxy = json.loads(requests.get(api_url).text)
        return json_proxy["data"]["proxy_list"][0]

    @staticmethod
    def get_proxies():
        # 这里使用自己的账号密码
        username = "username"
        password = "passward"
        proxy_ip = Proxy.get_proxy_ip()
        return {"http": f"http://{username}:{password}@{proxy_ip}/",
                "https": f"http://{username}:{password}@{proxy_ip}/"}

    @staticmethod
    def get_response(target_url, use_proxy: bool):
        """
        如果不想使用代理请在第二个参数填写 Flase
        """
        if use_proxy:
            return requests.get(target_url, headers=Proxy.get_headers(), proxies=Proxy.get_proxies())
        else:
            return requests.get(target_url, headers={"User-Agent": Proxy.get_user_agent_local()})


class Downloader:

    @staticmethod
    def download(target_url, use_proxy: bool):
        if use_proxy:
            result = Proxy.get_response(target_url, False)
        else:
            result = requests.get(target_url, headers=Proxy.get_headers())
        with open("new.html", "w", encoding="utf-8") as f:
            f.write(result.text)


if __name__ == '__main__':
    url = "https://myip.ipip.net"

    response = Proxy.get_response(url, True)
    print(response.text)
