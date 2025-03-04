import openai
import toml


def load_config(config_file="config.toml"):
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
    client = openai.OpenAI(api_key=config["api_key"], base_url=config["api_base"])
    model = config["model_name"]
    temperature = config["temperature"]
    stream = config["stream"]

    messages = []

    while True:
        user_input = input("你: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            if stream:
                response_stream = client.chat.completions.create(
                    model=model, messages=messages, temperature=temperature, stream=True
                )
                print("助手: ", end="", flush=True)
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
                    stream=False,
                )
                assistant_message = response.choices[0].message.content
                print("助手:", assistant_message)
                messages.append({"role": "assistant", "content": assistant_message})
        except openai.OpenAIError as e:
            print(f"OpenAI API 错误: {e}")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break


if __name__ == "__main__":
    config = load_config()
    chat(config)
