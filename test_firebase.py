import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 1. Autenticazione
cred = credentials.Certificate("chiave.json")
firebase_admin.initialize_app(cred)

# 2. Inizializziamo il database
db = firestore.client()

# 3. Creiamo un dato (il nostro famoso dizionario Python!)
nuovo_sensore = {
    "id": "SN-001",
    "temperatura": 30,
    "stato": "offline",
    "ultimo_aggiornamento": firestore.SERVER_TIMESTAMP # Funzione figa: mette l'ora del server
}

# 4. Invio al Cloud
# Creiamo una "collezione" chiamata 'sensori' e aggiungiamo il documento
db.collection("sensori").add(nuovo_sensore)

print("Dato inviato con successo su Firebase!")