from pymongo import MongoClient

# Połącz się z serwerem MongoDB (lokalnym lub zdalnym)
client = MongoClient('mongodb://localhost:27017/')

# Wybierz bazę danych
db = client['nazwa_bazy_danych']

# Wybierz kolekcję
collection = db['nazwa_kolekcji']

# Tworzenie dokumentu
doc = {"klucz": "wartość", "klucz2": "wartość2"}

# Zapisz dokument do kolekcji
collection.insert_one(doc)