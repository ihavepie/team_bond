import openai

openai.api_key = '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'

prompt = "Hello, how are you today?"
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=50
)
message = response.choices[0].text
print(message)
