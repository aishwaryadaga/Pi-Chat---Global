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
def create_prompt(data):
    ch = data
    session_messages.append(SystemMessage(content=f"""You are an interviewer for a technical company. 
    The interview has a total of 5 questions. The topic of the interview is {ch}. When user says "Start", based on 
    the topic, give 4 or 5 options as user's area of interest. User will reply and ask questions based on user's 
    reply. Interview starts here. After user answers the question, ask the next one directly. If user says "I'm not 
    sure" or "I don't know" or any such variation, move on to next question. If answer is correct,
    increase the difficulty of the next question. If answer is wrong, next question should be easier. Do not 
    repeat questions. Do NOT give answers for any question you ask. Do NOT give any explanation after user answers.
    For each correct answer, award 5 points. For partially correct answer, award 2.5 points. For wrong answers, 
    award 0 points. Do not mention if answer is correct or not. After the last question is answered, display the 
    final points without user prompting. Display question-wise marks as well."""))
    


def get_interview_question(msg):
    
    llm = ChatOpenAI(
        temperature=0, 
        model='gpt-3.5-turbo'
    )
    session_messages.append(HumanMessage(content=msg))
    answer = llm(session_messages)
    session_messages.append(AIMessage(content=answer.content))
    return answer.content





        