import numpy as np
import pandas as pd
import requests
import json
from time import sleep




def gamespotapi (llave, sesion, offset):

    url='http://www.gamespot.com/api/reviews/?'

    parametros = {
        'api_key': llave, 
        'format': 'json',
        'offset': f'{offset}'
    }

    for _ in range(10):
        try:
            respuesta = sesion.get(f'{url}', headers= sesion.headers, params=parametros)
            respuesta.raise_for_status()
            #print(f'{respuesta.text}\n\n\n' )
            return respuesta.json()
        
        except requests.exceptions.HTTPError as e:
            print("HTTPError:", e)
            sleep(6)

        except requests.exceptions.Timeout:
            print("Timeout alcanzado.")
            sleep(6)

        except requests.exceptions.RequestException as e:
            print("Error de red:", e)
            sleep(6)

        
try:
    documento=open('data/gamespot_reseñas.json', mode="x", encoding="utf-8")
    documento.close()
except FileExistsError:
    print("Ya está creado en documento")

doc="Partes_separadas_del_proyecto/Alonso/llave.txt"

with open(doc, mode="r", encoding="utf-8") as lista:
    llave = lista.readline().rstrip()

sesion= requests.session()
sesion.headers.update({'User-Agent': 'stingray49 PUC proyect https://github.com/claudiocanales721/Proyecto-cs-de-datos (aaqueveque@estudante.uc.cl)'})


offset=0
no_ultimo=True
contador=0
while no_ultimo:
    respuesta=gamespotapi(llave,sesion,offset)
    juegos=respuesta['results']

    if len(juegos) < 100:
        no_ultimo=False

    with open('data/gamespot_reseñas.json', 'a', encoding='utf-8') as f:
        json.dump(juegos, f, indent=4)
    
    offset+=100
    contador+=1

    print(f'Se guardó el request N°{contador}, con {len(juegos)} juegos, en total hay {offset} juegos')



