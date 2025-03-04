import openai
import readline  # 用于实现输入历史记录


def main():
    # 配置API密钥
    api_key = input("请输入您的OpenAI API密钥: ").strip()
    openai.api_key = api_key

    # 初始化对话历史
    messages = [{"role": "system", "content": "你是一个有用的助手。"}]

    print("\n欢迎使用聊天助手！输入内容开始对话，输入 'exit' 退出程序。\n")

    try:
        while True:
            try:
                # 获取用户输入
                user_input = input("用户: ").strip()

                if user_input.lower() in ("exit", "quit"):
                    print("再见！")
                    break

                if not user_input:
                    print("输入不能为空，请重新输入。")
                    continue

                # 添加用户消息到历史
                messages.append({"role": "user", "content": user_input})

                # 调用API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500,
                )

                # 获取助手回复
                assistant_reply = response.choices[0].message["content"]

                # 添加并显示助手回复
                messages.append({"role": "assistant", "content": assistant_reply})
                print(f"\n助手: {assistant_reply}\n")

            except openai.error.AuthenticationError:
                print("\n认证失败，请检查API密钥是否正确。")
                break
            except openai.error.RateLimitError:
                print("\n请求被限制，请稍后再试。")
                break
            except openai.error.APIConnectionError:
                print("\n网络连接失败，请检查网络设置。")
                break
            except KeyboardInterrupt:
                print("\n用户中断操作，退出程序。")
                break
            except Exception as e:
                print(f"\n发生未知错误: {str(e)}")
                break

    finally:
        print("\n对话历史已保存，程序结束。")


if __name__ == "__main__":
    main()
