import math


def calcular_angulo(p1, p2, p3):
    """
    Calcula o ângulo em graus no ponto p2 (vértice).
    p1, p2, p3 são tuplas (x, y).
    """
    v1_x = p1[0] - p2[0]
    v1_y = p1[1] - p2[1]
    
    v2_x = p3[0] - p2[0]
    v2_y = p3[1] - p2[1]
    
    produto_escalar = v1_x * v2_x + v1_y * v2_y
    
    mag_v1 = math.sqrt(v1_x**2 + v1_y**2)
    mag_v2 = math.sqrt(v2_x**2 + v2_y**2)
    
    cosseno_theta = produto_escalar / (mag_v1 * mag_v2)
    cosseno_theta = max(-1.0, min(1.0, cosseno_theta))
    
    angulo_radianos = math.acos(cosseno_theta)
    
    angulo_graus = math.degrees(angulo_radianos)
    
    return angulo_graus


def distancia_euclidiana(a, b):
    """
    Calculates the Euclidean distance between two (x, y) points.
    """
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
