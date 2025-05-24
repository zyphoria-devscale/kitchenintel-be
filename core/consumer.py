import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.task import process_chat, send_history_chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.group_name = f"chat_{self.session_id}"

        await self.accept()
        await self.channel_layer.group_add("chat", self.channel_name)
        send_history_chat(session_id=self.session_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        process_chat(message=message, session_id=self.session_id)

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
