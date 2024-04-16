import os
import sparkAPI
import _config


configInfo = _config.ConfigInfo()


def gen_spark_params(model):
    """
    构造星火模型请求参数
    """

    spark_url_tpl = "wss://spark-api.xf-yun.com/{}/chat"

    model_params_dict = {
        "v1.5": {
            "domain": "general",
            "spark_url": spark_url_tpl.format("v1.1")
        },

        "v2.0": {
            "domain": "generalv2",
            "spark_url": spark_url_tpl.format("v2.1")
        },

        "v3.0": {
            "domain": "generalv3",
            "spark_url": spark_url_tpl.format("v3.1")
        },

        "v3.5": {
            "domain": "generalv3.5",
            "spark_url": spark_url_tpl.format("v3.5")
        }
    }

    return model_params_dict[model]


def get_completion(prompt, model="v3.5", temperature=0.1):
    """
    获取星火模型调用结果

    请求参数：
        prompt: 对应的提示词
        model: 调用的模型，默认为 v3.5，也可以按需选择 v3.0 等其他模型
        temperature: 模型输出的温度系数，控制输出的随机程度，取值范围是 0~1.0，且不能设置为 0。温度系数越低，输出内容越一致。
    """

    response = sparkAPI.main(
        appid=configInfo.appid,
        api_secret=configInfo.api_secret,
        api_key=configInfo.api_key,
        gpt_url=gen_spark_params(model)["spark_url"],
        domain=gen_spark_params(model)["domain"],
        query=prompt
    )

    return response
