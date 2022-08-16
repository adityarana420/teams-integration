from config import DBConfigs
import pymongo
from cachetools import TTLCache

MONGODB_URL = "mongodb+srv://rana699:{}@cluster0.oujmu.mongodb.net/?retryWrites=true&w=majority".format(DBConfigs.MONGODB_PW)

class MongoDB:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.mongo_client = pymongo.MongoClient(MONGODB_URL)
        self.cred_collection = self.mongo_client["TeamsBotDB"]["credentials"]
    
    def insert_entry(self):
        data = {
            "user_id": "",
            "token": "",
            "org_id": ""
        }
        self.cred_collection.insert_one(data)
    
    def fetch_credentials_for_user(self):
        key = {'user_id': self.user_id}
        user_creds = self.cred_collection.find_one(key)

        token = user_creds.get("token", "")
        org_id = user_creds.get("org_id", "")

        return token, org_id
    
    def set_credentials(self, key, value):
        find_key = {
            'user_id': self.user_id
        }
        data = {
            '$set': {
                key: value
            }
        }
        try:
            self.cred_collection.update_one(find_key, data, upsert=True)
        except Exception as e:
            print(f"Unable to insert. Exception {e} occurred...")

        return True


    
    