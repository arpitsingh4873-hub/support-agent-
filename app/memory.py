from langchain_core.messages import HumanMessage, AIMessage
conversation_store = {}
def get_history(session_id: str):
    if session_id not in conversation_store:
        conversation_store[session_id] = []
    return conversation_store[session_id]

def add_to_history(session_id:str, question:str, answer: str):
    history = get_history(session_id)
    history.append(HumanMessage(content = question))
    history.append(AIMessage(content = answer))

def format_history(session_id:str):
    history = get_history(session_id)
    formatted = ""
    for msg in history:
        if isinstance(msg, HumanMessage):
            formatted += f"User: {msg.content}\n"
        else:
            formatted += f"Agent: {msg.content}\n"
    return formatted