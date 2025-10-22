import numpy as np
import pandas as pd
import requests
import json
import csv
from time import sleep

def diccionarios_a_csv(documento, lista, columnas, primero=False):

    if isinstance(lista, str):
        lista = json.loads(lista)


    df=pd.json_normalize(lista, sep='_')

    df=df[['game_name','score','publish_date','game_id']]

    df = df.reset_index(drop=True)
    
    modo = 'w' if primero else 'a'
    escribir_header = primero


    df.to_csv(documento, mode=modo, header=escribir_header, index=False)


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



doc="Partes_separadas_del_proyecto/Alonso/llave.txt"

with open(doc, mode="r", encoding="utf-8") as lista:
    llave = lista.readline().rstrip()

sesion= requests.session()
sesion.headers.update({'User-Agent': 'stingray49 PUC proyect https://github.com/claudiocanales721/Proyecto-cs-de-datos (aaqueveque@estudante.uc.cl)'})




offset=15300
primero=True
no_ultimo=True
contador=154
while no_ultimo:
    respuesta=gamespotapi(llave,sesion,offset)
    juegos=respuesta['results']

    if len(juegos) < 100:
        no_ultimo=False

    diccionarios_a_csv('data/gamespot.csv', juegos, primero)


    primero=False
    offset+=100
    contador+=1

    print(f'Se guardó el request N°{contador}, con {len(juegos)} juegos, en total hay {offset} juegos')




