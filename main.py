from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="placeholder")

stream = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Explain the origins of the universe."}],
    stream=True,
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
