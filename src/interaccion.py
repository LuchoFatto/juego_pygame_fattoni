import pygame
from random import randint
from settings import *
from pygame.locals import *
from colisiones import *
import csv
import json

def mostrar_texto(superficie: pygame.Surface, coordenada: tuple[int, int], texto: str, fuente: pygame.font.Font,
                    color: tuple[int, int, int] = WHITE, background_color: tuple[int, int, int] = None) -> None:
    """
    Muestra un texto en una superficie de Pygame en las coordenadas especificadas.

    Args:
        superficie (pygame.Surface): La superficie donde se mostrará el texto.
        coordenada (tuple[int, int]): La posición (x, y) donde se centrará el texto.
        texto (str): El texto a mostrar.
        fuente (pygame.font.Font): La fuente a utilizar para renderizar el texto.
        color (tuple[int, int, int], opcional): El color del texto en formato RGB. Por defecto es blanco (WHITE).
        background_color (tuple[int, int, int], opcional): El color de fondo del texto en formato RGB. Por defecto es None (sin fondo).

    Returns:
        None
    """
    sup_texto = fuente.render(texto, True, color, background_color)
    rect_texto = sup_texto.get_rect(center=coordenada)
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()

def terminar() -> None:
    """
    Termina la ejecución del programa.

    Esta función cierra Pygame y sale del programa.

    Args:
        None

    Returns:
        None
    """
    pygame.quit()
    exit()

def wait_user(tecla: int, quit: int = None):
    """
    Espera a que el usuario presione una tecla específica.

    Args:
        tecla (int): Código de la tecla que se espera.
        quit (int, optional): Código de la tecla para salir del juego. Por defecto es None.
    """
    flag_start = True
    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
                exit()

            if event.type == KEYDOWN:
                if event.key == tecla:
                    flag_start = False
                if quit and event.key == quit:
                    terminar()
                    exit()

def esperar_click_jugador(rect_button: pygame.Rect, rect_exit_button: pygame.Rect) -> None:
    """
    Espera a que el jugador haga clic en uno de los dos botones especificados.

    Esta función entra en un bucle que espera eventos de Pygame. Si se detecta un evento de salida (QUIT),
    se llama a la función `terminar` para cerrar el programa. Si se detecta un clic del ratón (MOUSEBUTTONDOWN)
    en el botón especificado por `rect_button`, se rompe el bucle. Si se detecta un clic del ratón en el botón
    especificado por `rect_exit_button`, se llama a la función `terminar`.

    Args:
        rect_button (pygame.Rect): El rectángulo del botón que el jugador debe hacer clic para continuar.
        rect_exit_button (pygame.Rect): El rectángulo del botón que el jugador debe hacer clic para salir.

    Returns:
        None
    """
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
        escritor_csv.writerow(["oleada", "tiempo"])

        for record in records:
            escritor_csv.writerow([record["oleada"], record["tiempo"]])

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

def orden_lista(funct, lista: list) -> None:
    """
    Ordena una lista según el criterio de la función proporcionada.

    Args:
        funct (function): Función que define el criterio de ordenación.
        lista (list): Lista a ordenar.
    """
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if funct(lista[i], lista[j]):
                swaps_valores(lista, i, j)

def swaps_valores(lista: list, i: int, j: int) -> None:
    """
    Intercambia los valores en las posiciones i y j de una lista.

    Args:
        lista (list): Lista en la que se realizará el intercambio.
        i (int): Índice del primer valor.
        j (int): Índice del segundo valor.
    """
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux

def mostrar_record(record: dict, screen: pygame.Surface, font: pygame.font.Font, distancia_y: tuple[int, int]):
    """
    Muestra un registro en la pantalla.

    Args:
        record (dict): Diccionario que representa un registro.
        screen (pygame.Surface): Superficie donde se mostrará el registro.
        font (pygame.font.Font): Fuente del texto.
        distancia_y (tuple[int, int]): Coordenadas (x, y) del texto.
    """
    mostrar_texto(screen, distancia_y, f"{record["oleada"]:<10} {record["tiempo"]:>10}", font, RED)

def mostrar_records(records: list, screen: pygame.Surface, font: pygame.font.Font):
    """
    Muestra todos los registros en la pantalla.

    Args:
        records (list): Lista de diccionarios que representan los registros.
        screen (pygame.Surface): Superficie donde se mostrarán los registros.
        font (pygame.font.Font): Fuente del texto.
    """
    if len(records) > 0:
        mostrar_texto(screen, (390, 380), "oleada           tiempo", font, BLUE)
        y_offset = 380 + 40
        for record in records:
            distancia_y = (390, y_offset)
            mostrar_record(record, screen, font, distancia_y)
            y_offset += 40
    else:
        print('ERROR: La lista no puede ser recorrida')