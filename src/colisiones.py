def punto_en_rectangulo(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def detectar_colision(rect_1, rect_2):
    #Revisa si algun punto del rect_1 esta dentro de rect_2
    if (punto_en_rectangulo(rect_1.topleft, rect_2) or \
        punto_en_rectangulo(rect_1.topright, rect_2) or \
        punto_en_rectangulo(rect_1.bottomleft, rect_2) or \
        punto_en_rectangulo(rect_1.bottomright, rect_2)):
        return True
    
    #Revisa si algun punto del rect_1 esta dentro de rect_2
    if (punto_en_rectangulo(rect_2.topleft, rect_1) or \
        punto_en_rectangulo(rect_2.topright, rect_1) or \
        punto_en_rectangulo(rect_2.bottomleft, rect_1) or \
        punto_en_rectangulo(rect_2.bottomright, rect_1)):
        return True
    
    #Si no encuentra ninguna colision, devuelve False
    return False

def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int])->float:
    return ((pto_1[0] - pto_2[0]) ** 2 + (pto_1[1] - pto_2[1]) ** 2) ** 0.5

def calcular_radio(rect):
    return rect.width // 2

def dectectar_colision_circulos(rect_1, rect_2):
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

