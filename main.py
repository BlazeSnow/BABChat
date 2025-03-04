import os
import requests


def main():
    # 配置API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("请输入你的OpenAI API密钥: ")

    # API配置
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # 初始化对话历史
    messages = []

    print("\n欢迎使用聊天助手！输入'exit'退出程序\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("你：")

            if user_input.lower() in ["exit", "quit"]:
                print("再见！")
                break

            # 添加用户消息到历史
            messages.append({"role": "user", "content": user_input})

            # 构造请求数据
            data = {"model": "gpt-3.5-turbo", "messages": messages, "temperature": 0.7}

            # 发送请求
            response = requests.post(url, json=data, headers=headers)

            # 处理响应
            if response.status_code == 200:
                response_data = response.json()
                assistant_reply = response_data["choices"][0]["message"]["content"]

                # 添加助手回复到历史
                messages.append({"role": "assistant", "content": assistant_reply})

                print(f"\n助手：{assistant_reply}\n")
            else:
                print(f"请求失败，状态码：{response.status_code}")
                print(f"错误信息：{response.text}")

        except requests.exceptions.RequestException as e:
            print(f"网络请求错误：{str(e)}")
        except KeyboardInterrupt:
            print("\n用户中断操作，退出程序")
            break
        except Exception as e:
            print(f"发生未知错误：{str(e)}")


if __name__ == "__main__":
    main()
