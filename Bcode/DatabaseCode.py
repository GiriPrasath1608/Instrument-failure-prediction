from pymongo import MongoClient
from urllib.parse import quote_plus
import pandas as pd

def mongodb_client():
    user_name = "giriprasathm1608"
    user_password = "Girim1608@"

    user_name_escaped = quote_plus(user_name)
    user_password_escaped = quote_plus(user_password)

    URI = f'mongodb+srv://{user_name_escaped}:{user_password_escaped}@fp-ml-data.ehr5y.mongodb.net/?retryWrites=true&w=majority&appName=FP-ML-DATA'
    client = MongoClient(URI)
    db = client['log']
    return db

def DataPush_mongoDB(instrument_readings):
    try:
        db = mongodb_client()
        collection = db['exp']
        return_from_db = collection.insert_one(instrument_readings)
        if return_from_db.acknowledged:
            return {'return_data' : 'Data is Stored in DataBase','acknowledge':True}  
    except Exception as e:
        print(f'An error occured {e}')
        return {'return_data' : 'Data is not Stored in DataBase','acknowledge':False}
    
def to_dataframe(instrument_readings):
    df = pd.DataFrame(instrument_readings.values(),index = instrument_readings.keys())
    return df