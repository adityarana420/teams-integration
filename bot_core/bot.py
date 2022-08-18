from botbuilder.core import ActivityHandler, TurnContext
from bot_core.utils import (
    Error_Handler,
    Response_Handler,
    Cred_Ops,
    post_message,
    fetch_marvis_response
)
import json

class BOT_PROCESSOR(ActivityHandler):
    def __init__(self):
        super().__init__()
        self.response_handler = Response_Handler()

    def _clean_user_input(self, text):
        text = text.strip()
        cleaned_text = text.replace("<at>Marvis-test</at>", "").strip() if text.find("<at>Marvis-test</at>") >= 0 else text
        return cleaned_text

    def _get_request_metadata(self, turn_context: TurnContext, org_id):
        metadata = {
            "time_zone": turn_context.activity.local_timezone,
            "utc_timestamp": str(turn_context.activity.timestamp),
            "local_timestamp": str(turn_context.activity.local_timestamp),
            "first_name": turn_context.activity.from_property.name.split()[0],
            "user_id": turn_context.activity.from_property.id,
            "conversation_type": turn_context.activity.conversation.conversation_type,
            "conversation_id": turn_context.activity.conversation.id,
            "org_id": org_id,
            "org_user": "True"
        }
        return metadata

    async def on_message_activity(self, turn_context: TurnContext):
        credentials = Cred_Ops(turn_context)

        # clean input message
        user_msg = self._clean_user_input(turn_context.activity.text)

        channel_type = turn_context.activity.conversation.conversation_type

        # if user is setting credentials
        if channel_type == "personal":
            if await credentials.is_setting_credentials(user_msg): return

        # fetch credentials
        token, org = credentials.fetch_credentials(channel_type)

        # verify credentials
        if not await credentials.verify_credentials(token, org): return

        request_metadata = self._get_request_metadata(turn_context, org)
        api_response = fetch_marvis_response(user_msg, token, org, request_metadata)

        # handling error response code
        if api_response.status_code != 200:
            await Error_Handler.credential_error(turn_context, api_response.status_code)
            return

        response_text = json.loads(api_response.text)
        marvis_response = response_text['data']

        # creating simple text response for user
        formatted_response_lst = self.response_handler.generate_response_list(marvis_response)

        for formatted_response in formatted_response_lst:
            response = await post_message(turn_context, formatted_response)
        return response
