import requests
import json

def _get_payload_header(query_msg, mist_token, metadata):
    auth_key = "Token {}".format(mist_token)
    payload = json.dumps({
      "type": "phrase",
      "phrase": query_msg,
      "attempt": "first",
      "user_metadata": metadata
    })

    header = {
      'Content-Type': 'application/json',
      'Authorization': auth_key,
      'Access-Control-Allow-Origin': '*'
    }
    return payload, header


def fetch_marvis_response(query_msg, mist_token, org_id, metadata):
    url = "https://api.mistsys.com/api/v1/labs/orgs/" + org_id + "/chatbot_converse"
   
    payload, headers = _get_payload_header(query_msg, mist_token, metadata)
    try:
      response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
      print("Exception occurred: {}".format(e))
      response = requests.Response()
      response.status_code = 504
      return response
    except Exception as e:
      response = requests.Response()
      response.status_code = 500
      return response
    return response
