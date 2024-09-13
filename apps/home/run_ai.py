from zhipuai import ZhipuAI

if __name__ == '__main__':
    client = ZhipuAI(api_key="ced7ea2da5a4ee898d65ca6d97533bbc.CejWrcYU8x32Ycvv")  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user",
             "content": "我对太阳系的行星非常感兴趣，特别是土星。请提供关于土星的基本信息，包括其大小、组成、环系统和任何独特的天文现象。"},
        ],
        stream=False,
    )
    for chunk in response:
        print(chunk.choices[0].delta)
