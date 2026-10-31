from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Say hi in 5 words"}],
)
print(completion.choices[0].message.content)