import openai
import toml
import os


def load_config(config_path="config.toml"):
    """
    加载配置文件
    """
    if not os.path.exists(config_path):
        print(f"配置文件 {config_path} 不存在！")
        exit(1)

    try:
        config = toml.load(config_path)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        exit(1)


def chat_with_openai(api_key, api_base, model, temperature, stream):
    """
    和 OpenAI 模型进行聊天
    """
    openai.api_key = api_key
    openai.api_base = api_base

    print("🤖 欢迎使用 OpenAI 聊天程序！输入 'exit' 退出。")

    while True:
        user_input = input("\n你: ")
        if user_input.lower() == "exit":
            print("👋 再见！")
            break

        try:
            if stream:
                # 流式输出
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": user_input}],
                    temperature=temperature,
                    stream=True,
                )
                print("AI: ", end="", flush=True)
                for chunk in response:
                    content = (
                        chunk.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content", "")
                    )
                    print(content, end="", flush=True)
                print()  # 换行
            else:
                # 非流式输出
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": user_input}],
                    temperature=temperature,
                )
                ai_response = response["choices"][0]["message"]["content"]
                print(f"AI: {ai_response}")
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    # 加载配置
    config = load_config()
    openai_config = config.get("openai", {})

    # 获取配置参数
    api_key = openai_config.get("api_key")
    api_base = openai_config.get("api_base", "https://api.openai.com/v1")
    model = openai_config.get("model", "gpt-3.5-turbo")
    temperature = openai_config.get("temperature", 0.7)
    stream = openai_config.get("stream", True)

    # 检查 API 密钥是否存在
    if not api_key:
        print("❌ API 密钥未设置，请在 config.toml 文件中填写你的 OpenAI API 密钥！")
        exit(1)

    # 启动聊天程序
    chat_with_openai(api_key, api_base, model, temperature, stream)
