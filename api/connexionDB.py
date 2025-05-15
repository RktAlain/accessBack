import pymongo

# url="mongodb://localhost:27017/"
url="mongodb+srv://brunoharison18:xE2NGihtznNYH9Hv@cluster0.cufza.mongodb.net/g-rtx-achat?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(url)

db = client['g-rtx-achat']
