import numpy as np
import pandas as pd
import requests
import json
import csv
from time import sleep


'''Esta funcion toma un texto con forma de json/diccionario y lo 
    agrega a un documeto csv, si no existe el documento lo crea'''
def diccionarios_a_csv(documento: str, lista: str, primero=False):

    #Convertir el texto a json, ya que está en formato diccionario
    if isinstance(lista, str):
        lista = json.loads(lista)

    #convertir el json a Data Frame y prepararlo para ser agregado
    #al docuemto csv
    df=pd.json_normalize(lista, sep='_')
    df=df[['game_name','score','publish_date','game_id','site_detail_url']]
    df = df.reset_index(drop=True)
    
    #Si es el promero crea el docuemto, de lo contrario agrega al final de este
    modo = 'w' if primero else 'a'
    escribir_header = primero
    df.to_csv(documento, mode=modo, header=escribir_header, index=False)


def gamespotapi (llave: str, sesion: requests.Session, offset: int) -> dict|None:

    url='http://www.gamespot.com/api/reviews/?'
    parametros = {
        'api_key': llave, 
        'format': 'json',
        'offset': f'{offset}'
    }

    #Hace como máximo 10 intentos
    for _ in range(10):
        try:
            respuesta = sesion.get(f'{url}', headers= sesion.headers, params=parametros)
            respuesta.raise_for_status()
            return respuesta.json()
        
        #Se informa el error si es que hay y se espera 6 segundos
        except requests.exceptions.HTTPError as e:
            print("HTTPError:", e)
            sleep(6)
        except requests.exceptions.Timeout:
            print("Timeout alcanzado.")
            sleep(6)
        except requests.exceptions.RequestException as e:
            print("Error de red:", e)
            sleep(6)

#Se obtiene la llave personal para contactar con el API
doc="Partes_separadas_del_proyecto/Alonso/llave.txt"
with open(doc, mode="r", encoding="utf-8") as lista:
    llave = lista.readline().rstrip()

#La sesión para optimizar los requests
sesion= requests.session()
sesion.headers.update({'User-Agent': 'stingray49 PUC proyect https://github.com/claudiocanales721/Proyecto-cs-de-datos (aaqueveque@estudante.uc.cl)'})

#este es el bucle que hace todos los requests, usanto las funciones previamente
#definidas
if __name__== '__main__':
    offset=0
    primero=True
    no_ultimo=True
    contador=0
    while no_ultimo:
        respuesta=gamespotapi(llave,sesion,offset)
        try:
            juegos=respuesta['results']
        except:
            print(f'Se detuvo en el request N°{contador} en total hay {offset} juegos')
            break
        
        if len(juegos) < 100:
            no_ultimo=False

        diccionarios_a_csv('Partes_separadas_del_proyecto/Alonso/data/gamespot_api.csv', juegos, primero)
        primero=False
        offset+=100
        contador+=1
        print(f'Se guardó el request N°{contador}, con {len(juegos)} juegos, en total hay {offset} juegos')