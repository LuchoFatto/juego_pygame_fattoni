import pygame
from random import randint
from settings import *
from pygame.locals import *
from colisiones import *
import csv
import json

def mostrar_texto(superficie:pygame.Surface, coordenada:tuple[int, int], texto:str, fuente:pygame.font.Font,
                color:tuple[int, int, int]= WHITE, background_color:tuple[int, int, int]=None):
    sup_texto = fuente.render(texto, True, color, background_color)
    rect_texto = sup_texto.get_rect(center= coordenada)
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()

def terminar():
    pygame.quit()
    exit()

#espera a que el usuario presione la tecla indicada
def wait_user(tecla):
    flag_start = True 
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == tecla:
                    flag_start = False

#cuando hace click en un boton hace algo
def esperar_click_jugador(rect_button:pygame.Rect,rect_exit_button:pygame.Rect):
    flag_start_bottom = True 
    while flag_start_bottom:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos, rect_button):
                        flag_start_bottom = False
                    if punto_en_rectangulo(evento.pos, rect_exit_button):
                        terminar()

def cargar_csv(nombre_archivo: str) -> list:
    """
    Carga un archivo CSV y lo convierte en una lista de diccionarios.

    Args:
        nombre_archivo (str): Nombre del archivo CSV (sin extensión).

    Returns:
        list: Lista de diccionarios con los datos del CSV.
    """
    with open(f"{PATH_CSV}{nombre_archivo}.csv") as archivo:
        lista_diccionarios = []
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            lista_diccionarios.append(fila)

    print("El archivo se ha cargado con éxito.")
    return lista_diccionarios

def guardar_csv(nombre_archivo: str, records: list):
    """
    Guarda una lista de diccionarios en un archivo CSV.

    Args:
        nombre_archivo (str): Nombre del archivo CSV (sin extensión).
        records (list): Lista de diccionarios a guardar.
    """
    nueva_ruta = f"{PATH_CSV}{nombre_archivo}.csv"

    with open(nueva_ruta, 'w', newline='', encoding="utf-8") as archivo_modificado:
        escritor_csv = csv.writer(archivo_modificado)
        escritor_csv.writerow(["puesto", "user", "nivel", "tiempo"])

        for record in records:
            escritor_csv.writerow([record["puesto"], record["user"], record["nivel"], record["tiempo"]])

        print(f"Archivo modificado guardado en: {nueva_ruta}")

def cargar_json(nombre_archivo: str) -> list:
    """
    Carga un archivo JSON y lo convierte en una lista de diccionarios.

    Args:
        nombre_archivo (str): Nombre del archivo JSON (sin extensión).

    Returns:
        list: Lista de diccionarios con los datos del JSON.
    """
    ruta = f"{PATH_JSON}{nombre_archivo}.json"
    with open(ruta, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
    return data

def guardar_json(nombre_archivo: str, records: list):
    """
    Guarda una lista de diccionarios en un archivo JSON.

    Args:
        nombre_archivo (str): Nombre del archivo JSON (sin extensión).
        records (list): Lista de diccionarios a guardar.
    """
    nueva_ruta = f"{PATH_JSON}{nombre_archivo}.json"
    with open(nueva_ruta, "w", encoding="utf-8") as archivo:
        json.dump(records, archivo, indent=4)
        print(f"Archivo guardado en: {nueva_ruta}")