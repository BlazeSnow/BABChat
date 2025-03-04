import openai
import toml


def load_config(config_file="config.toml"):
    """从 TOML 文件加载配置"""
    try:
        config = toml.load(config_file)
        # 检查关键配置是否存在
        if not config["openai"]["api_key"]:
            raise ValueError("config.toml 文件中缺少 'openai.api_key' 配置。")
        return config["openai"]
    except FileNotFoundError:
        raise FileNotFoundError("未找到 config.toml 文件。请确保它存在于当前目录。")
    except (toml.TomlDecodeError, KeyError) as e:
        raise ValueError(f"config.toml 文件解析错误或缺少必要的配置: {e}")


def chat(config):
    """与 OpenAI API 进行聊天"""

    openai.api_key = config["api_key"]
    openai.api_base = config["api_base"]
    model = config["model_name"]
    temperature = config["temperature"]
    stream = config["stream"]

    messages = []  # 用于存储对话历史

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":  # 退出机制
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model=model, messages=messages, temperature=temperature, stream=stream
            )

            if stream:
                print("Assistant: ", end="", flush=True)  # flush=True 很重要
                collected_chunks = []
                collected_messages = []
                for chunk in response:
                    collected_chunks.append(chunk)
                    chunk_message = chunk["choices"][0]["delta"]
                    collected_messages.append(chunk_message)
                    if "content" in chunk_message:
                        print(chunk_message["content"], end="", flush=True)
                print()
                full_reply_content = "".join(
                    [m.get("content", "") for m in collected_messages]
                )
                messages.append({"role": "assistant", "content": full_reply_content})

            else:
                assistant_message = response.choices[0].message["content"]
                print("Assistant:", assistant_message)
                messages.append({"role": "assistant", "content": assistant_message})

        except openai.error.OpenAIError as e:
            print(f"An OpenAI API error occurred: {e}")
            break  # 或者处理错误并继续
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # 或根据需要处理


if __name__ == "__main__":
    config = load_config()
    chat(config)
