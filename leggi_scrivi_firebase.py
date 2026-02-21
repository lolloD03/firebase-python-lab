import firebase_admin
from firebase_admin import credentials, firestore

# Inizializzazione (se non l'hai già fatta nello stesso script)
if not firebase_admin._apps:
    cred = credentials.Certificate("chiave.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 1. Recuperiamo tutti i documenti della collezione "sensori"
docs = db.collection("sensori").stream()

# 2. Trasformiamoli in una lista di dizionari Python
lista_sensori = []
for doc in docs:
    dati = doc.to_dict()
    dati["id_documento"] = doc.id # Recuperiamo anche l'ID univoco creato da Firebase
    lista_sensori.append(dati)

# Ora hai una lista di dizionari... esattamente come negli esercizi!
print(f"Ho recuperato {len(lista_sensori)} sensori.")

elevati = [dati["id_documento"] for dati in lista_sensori if dati["temperatura"] > 25]

for dati in elevati:
    db.collection("sensori").document(dati).update({"status": "offline"})



