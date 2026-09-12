import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

print(response["message"]["content"])