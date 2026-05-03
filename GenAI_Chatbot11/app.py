from transformers import pipeline

# Load AI model (GPT-2)
chatbot = pipeline("text-generation", model="gpt2")

print("🤖 AI Chatbot Ready! (type 'exit' to stop)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    response = chatbot(user_input, max_length=60, num_return_sequences=1)

    print("Bot:", response[0]["generated_text"])