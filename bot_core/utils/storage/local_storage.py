import os
import json

class LocalStorage:
    CREDS_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials/user_creds.json")
    
    def __init__(self):
        pass
    
    @staticmethod
    def _read_creds_from_file():
        try:
            all_users_creds = json.load(open(LocalStorage.CREDS_FILE_PATH))
        except Exception as e:
            print(f"Unable to read credentials file due to Exception {e}")
            all_users_creds = {}
        return all_users_creds
    
    @staticmethod
    def fetch_credentials_for_user(user_id):
        all_users_creds = LocalStorage._read_creds_from_file()

        token = all_users_creds.get(user_id, {}).get("token", "")
        org_id = all_users_creds.get(user_id, {}).get("org_id", "")

        return token, org_id
    
    @staticmethod
    def set_credentials(user_id, key, value):
        all_users_creds = LocalStorage._read_creds_from_file()

        if user_id in all_users_creds.keys():
            try:
                all_users_creds.get(user_id)[key] = value
                json.dump(all_users_creds, open(LocalStorage.CREDS_FILE_PATH, "w"))

            except Exception as e:
                print(f"Unable to write credentials due to exception {e}")
                return False
        
        else:
            try:
                all_users_creds[user_id] = {key: value}
                json.dump(all_users_creds, open(LocalStorage.CREDS_FILE_PATH, "w"))

            except Exception as e:
                print(f"Unable to write credentials due to exception {e}")
                return False

        return True
