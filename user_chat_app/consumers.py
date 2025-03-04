import json

import requests
from channels.generic.websocket import AsyncWebsocketConsumer

GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class UserChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        """Authenticate user using Google OAuth token"""

        # Extract token from query string (ws://localhost:8000/ws/chat/?token=ACCESS_TOKEN)
        query_string = self.scope["query_string"].decode()
        token = query_string.split("token=")[-1] if "token=" in query_string else None

        if not token:
            await self.close()
            return

        # Validate Google OAuth token
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)

        if response.status_code != 200:
            await self.close()
            return

        user_info = response.json()
        self.user_email = user_info.get("email")

        # Only allow users who authenticated via Google
        if self.user_email:
            self.room_group_name = "chat_room"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code) -> None:  # type: ignore
        """Remove user from chat group"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  # type: ignore

    async def receive(self, text_data) -> None:  # type: ignore
        """Handle incoming messages"""
        message_data = json.loads(text_data)
        message = message_data.get("message")

        if self.user_email and message:
            await self.channel_layer.group_send(  # type: ignore
                self.room_group_name,
                {"type": "chat_message", "message": f"{self.user_email}: {message}"},
            )

    async def chat_message(self, event) -> None:
        """Send messages to users"""
        await self.send(text_data=json.dumps({"message": event["message"]}))
