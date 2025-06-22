from agent.chat_agent import ask_openai

if __name__ == "__main__":
    user_input = input("Unesi pitanje: ")
    answer = ask_openai(user_input)
    print("\nOdgovor:\n", answer)