import openai
import toml


def load_config(config_file="config.toml"):
    """从 TOML 文件加载配置"""
    try:
        config = toml.load(config_file)
        if not config["openai"]["api_key"]:
            raise ValueError("config.toml 文件中缺少 'openai.api_key' 配置。")
        return config["openai"]
    except FileNotFoundError:
        raise FileNotFoundError("未找到 config.toml 文件。请确保它存在于当前目录。")
    except (toml.TomlDecodeError, KeyError) as e:
        raise ValueError(f"config.toml 文件解析错误或缺少必要的配置: {e}")


def chat(config):
    """与 OpenAI API 进行聊天"""

    client = openai.OpenAI(
        api_key=config["api_key"],
        base_url=config["api_base"],  # 注意这里是 base_url, 不是 api_base
    )
    model = config["model_name"]
    temperature = config["temperature"]
    stream = config["stream"]

    messages = []  # 用于存储对话历史

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            if stream:
                response_stream = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    stream=True,  # 明确指定 stream=True
                )
                print("Assistant: ", end="", flush=True)
                collected_messages = []
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        print(chunk.choices[0].delta.content, end="", flush=True)
                        collected_messages.append(chunk.choices[0].delta.content)
                print()
                full_reply_content = "".join(collected_messages)
                messages.append({"role": "assistant", "content": full_reply_content})

            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    stream=False,  # 明确指定 stream=False
                )
                assistant_message = response.choices[0].message.content
                print("Assistant:", assistant_message)
                messages.append({"role": "assistant", "content": assistant_message})

        except openai.OpenAIError as e:  # 使用 openai.OpenAIError
            print(f"An OpenAI API error occurred: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    config = load_config()
    chat(config)
