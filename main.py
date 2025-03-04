import os
import requests
import json
import time


def stream_chat_response(api_key, messages, model="deepseek-reasoner"):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "stream": True,  # 启用流式传输
    }

    full_response = []
    try:
        with requests.post(url, json=data, headers=headers, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")

                    # 处理流式响应格式
                    if decoded_line.startswith("data: "):
                        chunk = decoded_line[6:]  # 去掉"data: "前缀
                        try:
                            chunk_json = json.loads(chunk)
                            content = chunk_json["choices"][0]["delta"].get(
                                "content", ""
                            )
                            full_response.append(content)
                            yield content
                        except json.JSONDecodeError:
                            pass

    except Exception as e:
        yield f"\n[发生错误：{str(e)}]"

    return "".join(full_response)


def main():
    # 配置API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        api_key = input("请输入你的DeepSeek API密钥: ")

    # 初始化对话历史
    messages = []

    print("\n欢迎使用DeepSeek聊天助手！输入'exit'退出程序\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("你：")

            if user_input.lower() in ["exit", "quit"]:
                print("再见！")
                break

            # 添加用户消息到历史
            messages.append({"role": "user", "content": user_input})

            print("\n助手：", end="", flush=True)

            # 流式输出处理
            full_reply = []
            for chunk in stream_chat_response(api_key, messages):
                # 逐个字符打印实现打字机效果
                for char in chunk:
                    print(char, end="", flush=True)
                    time.sleep(0.02)  # 控制输出速度
                full_reply.append(chunk)

            # 添加完整回复到对话历史
            messages.append({"role": "assistant", "content": "".join(full_reply)})

            print("\n")

        except KeyboardInterrupt:
            print("\n用户中断操作，退出程序")
            break
        except Exception as e:
            print(f"\n发生错误：{str(e)}")


if __name__ == "__main__":
    main()
