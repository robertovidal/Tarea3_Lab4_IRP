import cv2
import os
import numpy as np
import sys

def mapeo_inverso_existe(a, b, c, d):
  result = b * c - a * d
  return result != 0

# En este mapeo se usa el mapeo bilineal en su forma
# lineal, o sea w = (az + b) / (cz + d) pasa a ser
# w = a/c + (bc-ad)/(c(cz + d)) y eso se simplifica
# a w = mu*z_2 +lambda
# Entonces las variables que tiene son:
# z_2 = 1 / z_1,
# z_1 = alfa * z +beta, 
# lambda = a/c,
# mu = bc - ad,
# alfa = c^2,
# beta = c*d
# Esto como se muestra en la página 36 del libro
# Señales y Sistemas Fundamentos Matemáticos de
# Pablo Alvarado Moya
def mapeo_directo(imagen, a, b, c, d):
    if not mapeo_inverso_existe(a,b,c,d):
        return imagen
    
    (alto, ancho) = imagen.shape[:2]

    if c == 0:
        lambda_ = complex(0)
    else:
        lambda_ = complex(a/c)
    mu = complex(b*c-a*d)
    cambioTamanno = np.linalg.norm([mu.real, mu.imag])
    angulo = np.angle(mu)
    nuevoTamanno = (round(ancho*cambioTamanno), round(alto*cambioTamanno))
    res = cv2.resize(imagen,dsize=nuevoTamanno)
    (alto, ancho) = res.shape[:2]
    M = cv2.getRotationMatrix2D((lambda_.real, lambda_.imag), angulo, 1.0)
    imagenNueva = cv2.warpAffine(src=res, M=M, dsize=(ancho, alto))
    
    return imagenNueva

def mapeo_inverso(imagen, a, b, c, d):
    if not mapeo_inverso_existe(a,b,c,d):
        return imagen
    
    (alto, ancho) = imagen.shape[:2]

    alfa = complex(c)**2
    if c == 0:
        lambda_ = complex(0)
    else:
        lambda_ = complex(-d/c)
    mu = complex(b*c-a*d)
    cambioTamanno = np.linalg.norm([mu.real, mu.imag])
    angulo = np.angle(mu)
    nuevoTamanno = (round(ancho/cambioTamanno), round(alto/cambioTamanno))
    res = cv2.resize(imagen,dsize=nuevoTamanno)
    (alto, ancho) = res.shape[:2]
    M = cv2.getRotationMatrix2D((lambda_.real, lambda_.imag), angulo, 1.0)
    imagenNueva = cv2.warpAffine(src=res, M=M, dsize=(ancho, alto))
    
    return imagenNueva

if len(sys.argv) < 5:
    imagen = cv2.imread("Original.png")
    imagen2 = mapeo_directo(imagen, 2.1+2.1j, 0, 0.003, 1+1j)
    #imagen2 = mapeo(imagen, 4, 0, 0, 1)
else:
    imagen = cv2.imread(sys.argv[0])
    imagen2 = mapeo_directo(imagen, complex(sys.argv[1]), complex(sys.argv[2]), complex(sys.argv[3]), complex(sys.argv[4]))
    

cv2.imwrite("imagen2.png", imagen2)