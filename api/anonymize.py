import spacy
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = spacy.load('api/models/en')

class UserRequestIn(BaseModel):
    text: str

class EntitiesOut(BaseModel):
    entities: list
    anonymized_text: str

@app.post("/anonymizeme", response_model=EntitiesOut)
def extract_entities(user_request: UserRequestIn):
    text = user_request.text
    doc = model(text)

    entities = [
        {
            "start": ent.start_char,
            "end": ent.end_char,
            "type": ent.label_,
            "text": ent.text,
        }
        for ent in doc.ents
    ]

    anonymized_text = list(text)

    for entity in entities:
        start = entity["start"]
        end = entity["end"]
        anonymized_text[start:end] = "X" * (end - start)

    anonymized_text = "".join(anonymized_text)
    return {"entities": entities, "anonymized_text": anonymized_text}


# add a simle get route to check if the server is running
@app.get("/")
def read_root():
    return {"Business Data Science 🚀💪"}


