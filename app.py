from fastapi import FastAPI
from pydantic import BaseModel

from agents.intent_agent import IntentAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.emotion_agent import EmotionAgent
from agents.ticket_agent import TicketAgent

app = FastAPI()

intent_agent = IntentAgent()
knowledge_agent = KnowledgeAgent()
emotion_agent = EmotionAgent()
ticket_agent = TicketAgent()

class UserMessage(BaseModel):
    user: str
    message: str

@app.post("/chat")
def chat(data: UserMessage):

    text = data.message

    # 1. 意图识别
    intent = intent_agent.analyze_intent(text)

    # 2. 情绪分析
    emotion = emotion_agent.detect_emotion(text)

    # 3. 情绪异常转人工
    if emotion == "negative":
        ticket = ticket_agent.create_ticket(data.user, text)

        return {
            "status": "人工介入",
            "ticket": ticket
        }

    # 4. 知识库检索
    answer = knowledge_agent.search_answer(text)

    return {
        "intent": intent,
        "emotion": emotion,
        "reply": answer
    }
