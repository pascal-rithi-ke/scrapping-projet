import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DB_NAME")
collection_name = os.getenv("MONGO_COLLECTION_NAME")
collection_name_test = os.getenv("MONGO_COLLECTION_NAME_TEST")
collection_name_train = os.getenv("MONGO_COLLECTION_NAME_TRAIN")

uri = f"mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority"

def get_collection_restaurants(typeCol):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        if typeCol == "raw":
            return db[collection_name]
        elif typeCol == "test":
            return db[collection_name_test]
        elif typeCol == "train":
            return db[collection_name_train]
        else:
            raise ValueError("Type de collection non pris en charge")
    except Exception as e:
        print("Erreur lors de la connexion à MongoDB :", e)

def add_restaurants(restaurant, typeCol):
    try:
        collection = get_collection_restaurants(typeCol)
        collection.insert_many(restaurant)
    except Exception as e:
        print("Erreur lors de l'ajout des restaurants :", e)

def add_restaurant(restaurant):
    try:
        collection = get_collection_restaurants()
        collection.insert_one(restaurant)
    except Exception as e:
        print("Erreur lors de l'ajout du restaurant :", e)

def get_restaurant(restaurant_id):
    try:
        collection = get_collection_restaurants()
        restaurant = collection.find_one({"_id": restaurant_id})
        return restaurant
    except Exception as e:
        print("Erreur lors de la récupération du restaurant :", e)