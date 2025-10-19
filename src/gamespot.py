import numpy as np
import pandas as pd
import requests
import json


doc="src/llave.txt"

def gamespotapi (llave, sesion, offset=0):

    url='http://www.gamespot.com/api/reviews/?'

    params = {
        'api_key': llave, 
        'form': 'json'
        #'offset': offset
    }

    try:
        respuesta = sesion.get(f'{url}', params=params, timeout=15)
        respuesta.raise_for_status()
        return respuesta.json()
        
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return None
    except requests.exceptions.Timeout:
        print("Timeout alcanzado.")
        return None
    except requests.exceptions.RequestException as e:
        print("Error de red:", e)
        return None

compilado=[]

with open(doc, mode="r", encoding="utf-8") as lista:
    llave = lista.readline()
    llave = llave.rstrip()
    sesion= requests.session()
    sesion.headers.update({'User-Agent': 'stingray49'})
    respuesta=gamespotapi(llave,sesion)
    print(type(respuesta))
    compilado=compilado.append(respuesta)