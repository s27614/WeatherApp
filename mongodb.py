import os
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['weather_app']
collection = db['weather_data']

DB_DIR = 'db'
DB_FILE = 'data.json'


def check_database_existence():
    if os.path.exists(DB_DIR) and os.path.isfile(os.path.join(DB_DIR, DB_FILE)):
        if os.path.getsize(os.path.join(DB_DIR, DB_FILE)) > 0:
            return True
    return False

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def write_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def store_weather_data(city, temperature, weather_desc, feels_like, icon_code, local_time, utc_time):
    data = {
        'city': city,
        'temperature': temperature,
        'weather_desc': weather_desc,
        'feels_like': feels_like,
        'icon_code': icon_code,
        'local_time': local_time,
        'utc_time': utc_time
    }
    try:
        result = collection.insert_one(data)
        print(f"Inserted document ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

def dump_data_to_file():
    data = list(collection.find())

    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    file_path = os.path.join(DB_DIR, DB_FILE)
    with open(file_path, 'w') as file:
        json.dump(data, file, default=str)

    print(f"Data dumped to {file_path}")

def initialize_database():
    if not check_database_existence():
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        with open(os.path.join(DB_DIR, DB_FILE), 'w') as file:
            json.dump([], file)
    else:
        initialize_database_from_file(os.path.join(DB_DIR, DB_FILE))

def initialize_database_from_file(filename):
    if check_database_existence():
        data = read_data_from_file(filename)
        if data:
            for document in data:
                try:
                    collection.insert_one(document)
                    print(f"Inserted document from file: {document['_id']}")
                except Exception as e:
                    print(f"Error inserting data from file into MongoDB: {e}")


if __name__ == '__main__':
    initialize_database()
    dump_data_to_file()
    client.close()
