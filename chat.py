from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from dotenv import load_dotenv

load_dotenv()
bot_name = "Pi"

session_messages = []
session_messages.append(SystemMessage(content="You are a helpful assistant."))


def get_response(msg):
    
    llm = ChatOpenAI(
        temperature=0, 
        model='gpt-3.5-turbo'
    )
    session_messages.append(HumanMessage(content=msg))
    answer = llm(session_messages)
    session_messages.append(AIMessage(content=answer.content))
    return answer.content


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")

    # testing chat box in chat
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(bot_name+": " + resp)

