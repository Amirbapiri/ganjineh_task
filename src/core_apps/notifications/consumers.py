from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from core_apps.notifications.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = f"notifications_{self.user.id}"
        print("HEREHERHERHEHREHRR", self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

    async def send_notification(self, event):
        notification = event["notification"]

        await self.send(text_data=json.dumps(notification))

    @database_sync_to_async
    def get_unread_notification(self):
        return list(self.user.notifications.filter(read=False).values())
