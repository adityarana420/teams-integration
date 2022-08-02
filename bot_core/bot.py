from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
import time
import asyncio
class EchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        response =  await turn_context.send_activity(
            MessageFactory.text(f"Echo: {turn_context.activity.text}")
        )
        return response
