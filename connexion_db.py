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
        result = collection.insert_many(restaurant)
        return result.inserted_ids
    except Exception as e:
        print("Erreur lors de l'ajout des restaurants :", e)

def add_restaurant(restaurant):
    try:
        collection = get_collection_restaurants()
        result = collection.insert_one(restaurant)

        return result.inserted_id
    except Exception as e:
        print("Erreur lors de l'ajout du restaurant :", e)

def add_reviews_to_restaurant(restaurant_id, reviews):
    # insert the array called 'avis' in one restaurant
    try:
        collection = get_collection_restaurants()
        result = collection.update_one({"_id": restaurant_id}, {"$push": {"avis": {"$each": reviews}}})

        return result
    except Exception as e:
        print("Erreur lors de l'ajout des avis :", e)

def add_one_review_to_restaurant(restaurant_id, avis):
    try:
        collection = get_collection_restaurants()
        # Ajoute chaque avis au tableau d'avis du restaurant spécifique
        for avis in avis:
            collection.update_one({"_id": restaurant_id}, {"$push": {"avis": avis}})
    except Exception as e:
        print("Erreur lors de l'ajout des avis au restaurant :", e)


def get_restaurant(restaurant_id):
    try:
        collection = get_collection_restaurants()
        restaurant = collection.find_one({"_id": restaurant_id})
        return restaurant
    except Exception as e:
        print("Erreur lors de la récupération du restaurant :", e)