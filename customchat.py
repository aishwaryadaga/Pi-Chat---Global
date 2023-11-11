import dotenv
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.chains import RetrievalQA, ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import openai

load_dotenv()
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

session_messages = []
responses = ['How can I assist you?']
requests = []
buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""You a helpful assistant. Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know' politely. """)


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

llm = ChatOpenAI(
        temperature=0, 
        model='gpt-3.5-turbo'
    )

conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function = len)
embedding_function = OpenAIEmbeddings()

def load_docs(filename):
    # static\files\note.txt --> double backslash to make it a string
    dest = "static\\files\\" + filename
    if(filename.split('.')[1] == 'pdf'):
        loader = PyPDFLoader(dest)
    elif(filename.split('.')[1] == 'csv'):
        loader = CSVLoader(dest)
    elif(filename.split('.')[1] == 'txt'):
        loader = TextLoader(dest)
    documents = loader.load()
    docs = text_splitter.split_documents(documents)
    directory = "./static/files/" + filename.split('.')[0]
    db = Chroma.from_documents(docs, embedding_function, persist_directory=directory)
    db.persist()
    
def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(responses)-1):
        conversation_string += "Human: "+requests[i] + "\n"
        conversation_string += "Bot: "+ responses[i+1] + "\n"
    return conversation_string


def get_custom_response(msg, filename):
    conversation_string = get_conversation_string()
    refined_query = query_refiner(conversation_string, msg)
    requests.append(msg)
    directory = "./static/files/" + filename.split('.')[0]
    db_connection = Chroma(persist_directory=directory,embedding_function=embedding_function)
    retriever = db_connection.as_retriever()
    # search_kwargs = {"score_threshold":0.8,"k":2}
    # context = retriever.get_relevant_documents(refined_query, search_kwargs={"score_threshold":0.8,"k":2})
    context = retriever.get_relevant_documents(refined_query)
    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{msg}")
    responses.append(response)

    return response


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")

    # testing chat box in chat
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_custom_response(sentence, "note")
        print("Bot"+": " + resp)