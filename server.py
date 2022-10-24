from multiprocessing import allow_connection_pickling
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import true

app = FastAPI()

origins = [''] #O endereço digitado neste campo será aquele que terá permissão para consumir a API que você elaborou.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=true,   #middleware faz o tratamento de informações entre response e request, dando/bloqueando permissões.
    allow_methods=["*"],
    allow_headers=["*"]
)

class Animal(BaseModel):
    id: Optional[str]
    nome: str
    idade: int
    sexo: str
    cor: str
    
bancodados: List[Animal] = []
    

@app.get('/')
def home():
    return{"msg":"api-on"}


@app.get('/animais')
def listaanimais():
    return bancodados



@app.post('/addanimais')
def addanimais(animal: Animal):
    animal.id = str(uuid4())
    bancodados.append(animal)
    return animal.id


@app.get('/animais/{animal_id}')
def get_animal_id(animal_id: str):
    for animal in bancodados:
        if animal.id == animal_id:
            return animal
        return {'erro':'animal não encontrado'}

   
@app.delete('/animais/{animal_id}')
def delete_animal_id(animal_id: str):
    posicao = -1
    for index, animal in enumerate(bancodados):
        if animal.id == animal_id:
            posicao = index
            break
        
        if posicao != -1:
            bancodados.pop(posicao) #pop, método de deleção por índice
            return{'msg': 'animal deletado com sucesso'}
        else:
            return {'erro': 'animal não localizado'}