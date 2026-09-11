from openai import OpenAI

# pip install openai
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key = "openai_api_key" ,
)

completion = client.chat.completions.create(
    model="gpt-5.6-luna",
    messages=[
        {"role": "system", "content": "You are a Virtual assistant named jarvis skilled in general tasks like ALexa and Google Cloud."},
        {"role": "user", "content": "WHat is coding"},
    ],
)
print(completion.choices[0].message.content)



