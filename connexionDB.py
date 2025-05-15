import pymongo
from pymongo.errors import ConnectionFailure, ConfigurationError, PyMongoError
import urllib.parse
# from colorama import Fore

try:
    url = "mongodb+srv://brunoharison18:xE2NGihtznNYH9Hv@cluster0.cufza.mongodb.net/g-rtx-achat?retryWrites=true&w=majority&appName=Cluster0"
    # url= "mongodb://localhost:27017/g-rtx-achat"
    try:
        client = pymongo.MongoClient(url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        # print(Fore.GREEN)
        print("✅ Connexion à MongoDB réussie!")
        
        db = client['g-rtx-achat']   
    except ConnectionFailure as e:
        # print(Fore.RED)
        print(f"❌ Erreur de connexion à MongoDB: {e}")
    except ConfigurationError as e:
        # print(Fore.RED)
        print(f"❌ Erreur de configuration: {e}")
    except PyMongoError as e:
        # print(Fore.RED)
        print(f"❌ Erreur PyMongo: {e}")
    except Exception as e:
        # print(Fore.RED)
        print(f"❌ Erreur inattendue: {e}")
    # print(Fore.WHITE)
except Exception as e:
    # print(Fore.RED)
    print(f"❌ Erreur lors de la construction de l'URL: {e}")
# print(Fore.WHITE)
    