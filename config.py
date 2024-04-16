class ConfigInfo:
    def __init__(self):
        # 认证信息
        self.appid = ""
        self.api_secret = ""
        self.api_key = ""

        # api 调用接口
        self.gpt_url = "wss://spark-api.xf-yun.com/v3.5/chat"     # v3.5环境的地址
        # self.gpt_url="ws://spark-api.xf-yun.com/v3.1/chat",     # v3.0环境的地址
        # self.gpt_url="ws://spark-api.xf-yun.com/v2.1/chat",     # v2.0环境的地址
        # self.gpt_url="ws://spark-api.xf-yun.com/v1.1/chat",     # v1.5环境的地址

        # 选择对应的版本
        self.domain = "generalv3.5"     # v3.5版本
        # self.domain="generalv3",      # v3.0版本
        # self.domain="generalv2"       # v2.0版本
        # self.domain="general"         # v2.0版本
