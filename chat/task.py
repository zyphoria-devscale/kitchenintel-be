import asyncio

from chat.models import Conversation
from core.ai.agent import chats
from core.methods import send_chat_message
from huey.contrib.djhuey import task


@task()
def process_chat(message: str, session_id: str):
    Conversation.objects.create(message=message, role="user", session_id=session_id)

    chats_history = Conversation.objects.filter(session_id=session_id)
    messages = []
    for chat in chats_history:
        messages.append({"role": chat.role, "content": chat.message})

    res = asyncio.run(chats(messages))
    send_chat_message(res)
    Conversation.objects.create(message=res, role="assistant", session_id=session_id)

@task()
def send_history_chat(session_id: str):
    chats_history = Conversation.objects.filter(session_id=session_id)
    messages = []
    for chat in chats_history:
        messages.append({"role": chat.role, "content": chat.message})

    send_chat_message(messages)
