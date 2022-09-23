import cv2
import os
import numpy as np
import sys

def mapeo_inverso_existe(a, b, c, d):
  result = b * c - a * d
  return result != 0

def mapeo(imagen, a, b, c, d):
    if not mapeo_inverso_existe(a,b,c,d):
        return imagen
    
    (alto, ancho) = imagen.shape[:2]

    alfa = complex(c)**2
    beta = complex(c*d)
    mu = complex(b*c-a*d)
    cambioTamanno = np.linalg.norm([mu.real, mu.imag])
    angulo = np.angle(alfa)
    nuevoTamanno = (round(ancho*cambioTamanno), round(alto*cambioTamanno))
    res = cv2.resize(imagen,dsize=nuevoTamanno)
    (alto, ancho) = res.shape[:2]
    M = cv2.getRotationMatrix2D((beta.real, beta.imag), angulo, 1.0)
    imagenNueva = cv2.warpAffine(src=res, M=M, dsize=(ancho, alto))
    
    return imagenNueva

if len(sys.argv) < 5:
    imagen = cv2.imread("Original.png")
    imagen2 = mapeo(imagen, 2.1+2.1j, 0, 0.003, 1+1j)
    #imagen2 = mapeo(imagen, 4, 0, 0, 1)
else:
    imagen = cv2.imread(sys.argv[0])
    imagen2 = mapeo(imagen, complex(sys.argv[1]), complex(sys.argv[2]), complex(sys.argv[3]), complex(sys.argv[4]))
    

cv2.imwrite("imagen2.png", imagen2)