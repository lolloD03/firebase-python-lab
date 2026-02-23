
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("chiave.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()

# La classe finisce dove finisce l'indentazione
class Sensore(BaseModel):
    id: str
    temperatura: float
    stato: str = "online"

@app.get("/")
def home():
    return {"messaggio": "Il mio primo server Backend è attivo!"}

@app.post("/crea-sensore")
def crea_sensore(dato: Sensore):

    sensore_dict = dato.dict()
    if sensore_dict.get("temperatura")> 100 or sensore_dict.get("temperatura")<-50:
        raise HTTPException(status_code=400, detail="Temperatura assurda")
    db.collection("sensori").document(sensore_dict["id"]).set(sensore_dict)

    return {"hai_inviato": dato, "messaggio": "Dati ricevuti correttamente"}


@app.get("/sensori-caldi")
def sensori_caldi():

    docs = db.collection("sensori").stream()
    docs_dict = [doc.to_dict() for doc in docs]
    lista_sensori = [doc for doc in docs_dict if doc["temperatura"]>25]
    return lista_sensori



@app.get("/sensori")
def leggi_sensori(soglia: float = 20.0):
    docs = db.collection("sensori").stream()

    filtrati = [doc.to_dict() for doc in docs if doc.to_dict().get("temperatura",0) > soglia]

    return {
        "soglia_utilizzata": soglia,
        "risultati_trovati": len(filtrati),
        "dati": filtrati
    }