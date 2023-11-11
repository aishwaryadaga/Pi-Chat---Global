from langflow import load_flow_from_json
import os

# os.environ['OPENAI_API_KEY'] = 'sk-'

from dotenv import load_dotenv

load_dotenv()

# flow = load_flow_from_json("Conversation Chain.json")
# Now you can use it like any chain

def get_flow_response(msg):
    flow = load_flow_from_json("Time Travel Guide.json")
    return ((flow(msg))['response'])


# to test on terminal -->
if __name__ == "__main__":
    while True:
        inp = input()
        print("Human: " + inp)
        resp = get_flow_response(inp)
        print("AI: " + resp)