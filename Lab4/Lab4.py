import cv2
import numpy as np

# Función para determinar si una función tiene inverso o no
# si b * c - a * d es 0 significa que no tiene inverso, pero
# si no es 0, significa que sí tiene.
def mapeo_inverso_existe(a, b, c, d):
  result = b * c - a * d
  return result != 0

# Función para generar el plano w a través del
# plano z representado por una imagen y las
# constantes de a, b, c y d.
def generacion_plano_w(image, a, b, c, d):
  # Primero se revisa si el mapeo inverso se puede hacer
  # debido a que se utiliza
  if not mapeo_inverso_existe(a,b,c,d):
    return image
  (h, w) = image.shape[:2]
  higherX = 0
  higherY = 0
  # En esta parte se calcula cuál es el tamaño
  # de la imagen resultante
  for x in range(h):
    for y in range(w):
      num = complex(x, y)
      new =  (a * num + b) / (c * num + d)
      if higherX < int(new.real):
        higherX = int(new.real)
      if higherY < int(new.imag):
        higherY = int(new.imag)
  
  # Aquí se genera el plano w, esto se realiza
  # a partir de la inversa para poder rellenar
  # de manera correcta los pixeles
  wResult = np.zeros((higherX, higherY, 3), dtype = "uint8")
  for x in range(h):
    for y in range(w):
      num = complex(x, y)
      new =  (-d * num + b) / (c * num - a)
      newX = int(new.real)
      newY = int(new.imag)
      if(abs(newX) < h) and (abs(newY) < w):
          wResult[x][y] = image[newX][newY]
  return wResult

# Esta es la función de mapeo lineal, es decir
# donde solo se necesita el plano z y las constantes
# a y b, las constante c se considera como 0 y la
# constante d como 1. Hace lo mismo que la función
# anterior solo que con estas consideraciones
def mapeo_lineal(image, a, b):
  if not mapeo_inverso_existe(a,b,0,1):
    return image
  (h, w) = image.shape[:2]
  higherX = 0
  higherY = 0
  for x in range(h):
    for y in range(w):
      num = complex(x, y)
      new =  a * num + b
      if higherX < int(new.real):
        higherX = int(new.real)
      if higherY < int(new.imag):
        higherY = int(new.imag)
  wResult = np.zeros((higherX, higherY, 3), dtype = "uint8")
  for x in range(higherX):
    for y in range(higherY):
      num = complex(x, y)
      new =  (num - b) / a
      newX = int(new.real)
      newY = int(new.imag)
      if(abs(newX) < h) and (abs(newY) < w):
          wResult[x][y] = image[newX][newY]
  return wResult

image = cv2.imread("Original.png")

# La demostración del punto A, que al b ser 0 y
# a pertenece a los reales y no es 0, se produce 
# una magnificación
PruebaA = mapeo_lineal(image, 4, 0)
cv2.imwrite("PruebaA.png", PruebaA)

# La demostración del punto B, que al b ser 0 y
# a pertenece a los complejos y no es 0 o es real, 
# se produce una magnificación y una rotación 
PruebaB = mapeo_lineal(image, 2.1 + 2.1j, 0)
cv2.imwrite("PruebaB.png", PruebaB)

# La demostración del punto C, que al a ser 1 y
# b no es 0, se produce un desplazamiento
PruebaC = mapeo_lineal(image, 1, 100)
cv2.imwrite("PruebaC.png", PruebaC)

# La demostración del punto D, que al a ser diferente 
# de 0 y b diferente de 0 también, se produce una 
# magnificación una rotación y un desplazamiento
PruebaD = mapeo_lineal(image, 2.1 + 2.1j, 100)
cv2.imwrite("PruebaD.png", PruebaD)


