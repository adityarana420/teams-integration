from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from bot_core.utils import CRED_OPS, RESPONSE_HANDLER, post_message
from bot_core.mist_api import fetch_marvis_response
import json

credentials = CRED_OPS()
response_handler = RESPONSE_HANDLER()

def _clean_user_input(text):
    text = text.strip()
    cleaned_text = text.replace("<at>Marvis-test</at>", "").strip() if text.find("<at>Marvis-test</at>") >= 0 else text
    return cleaned_text

class BOT_PROCESSOR(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        token = org = ""
        user_msg = _clean_user_input(turn_context.activity.text)
        print("=> User Input:", user_msg)

        # fetch credentials
        token, org = credentials.fetch_credentials(turn_context.activity.channel_id)
        if not (token or org):
            response = await post_message(turn_context, "Some error occurred. Unable to fetch credentials.")
            return response
        
        api_response = fetch_marvis_response(user_msg, token, org)

        # handling error response code
        if api_response.status_code != 200:
            response = await post_message(turn_context, f"Some error Occurred. Status code {api_response.status_code}")
            return response
        
        response_text = json.loads(api_response.text)
        marvis_response = response_text['data']

        formatted_response_lst = response_handler.generate_response_list(marvis_response)
        print(formatted_response_lst)

        for formatted_response in formatted_response_lst:
            response = await post_message(turn_context, formatted_response)
        return response
