from pymongo import MongoClient

client = MongoClient("mongodb://root:password@localhost:27018/")
print("Conectado ao MongoDB")

db = client["my_db"]
users = db["users"]

users.create_index("email", unique=True)

try: 
    users.insert_one({
        "name":"anderson",
        "email":"anderson@email.com",
        "idade":30
    })

    for doc in users.find():
        print(doc)

except Exception:
    print(f"ERROR: EMAIL JÁ CADASTRADO")