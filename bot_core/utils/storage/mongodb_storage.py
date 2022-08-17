from config import MongoConfigs
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=200, ttl=14*24*3600)

class MongoDB:
    def __init__(self):
        pass
    
    @staticmethod
    @cached(cache)
    def fetch_credentials_for_user(user_id):
        key = {'user_id': user_id}
        user_creds = MongoConfigs.COLLECTION.find_one(key)

        token = user_creds.get("token", "")
        org_id = user_creds.get("org_id", "")

        return token, org_id
    
    @staticmethod
    def set_credentials(user_id, key, value):
        find_key = {
            'user_id': user_id
        }
        data = {
            '$set': {
                key: value
            }
        }
        try:
            MongoConfigs.COLLECTION.update_one(find_key, data, upsert=True)
        except Exception as e:
            print(f"Unable to insert. Exception {e} occurred...")

        return True


    
    