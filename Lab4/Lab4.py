import cv2
import numpy as np
import math

# Función para determinar si una función tiene inverso o no
# si b * c - a * d es 0 significa que no tiene inverso, pero
# si no es 0, significa que sí tiene.
def mapeo_inverso_existe(a, b, c, d):
  result = b * c - a * d
  return result != 0

# Función que representa al mapeo bilineal, 
# genera el plano w a través del plano z 
# representado por una imagen y las constantes 
# de a, b, c y d.
def mapeo_bilineal(image, a, b, c, d):
  # Primero se revisa si el mapeo inverso se puede hacer
  # debido a que se utiliza
  if not mapeo_inverso_existe(a,b,c,d):
    return image
  (h, w) = image.shape[:2]
  higherXPositive = 0
  higherXNegative = 0
  higherYPositive = 0
  higherYNegative = 0
  # En esta parte se calcula cuál es el tamaño
  # de la imagen resultante, lo que se hace es 
  # sumar el resultado más grande positivo y
  # negativo para poder colocar en la imagen
  # tanto los resultados positivos como negativos
  # en un mismo plano
  for x in range(h):
    for y in range(w):
      num = complex(x, y)
      new =  (a * num + b) / (c * num + d)
      if new.real >= 0:
        if higherXPositive < round(new.real):
          higherXPositive = round(new.real)
      else:
        if higherXNegative < abs(round(new.real)):
          higherXNegative = abs(round(new.real))
      if new.imag >= 0:
        if higherYPositive < round(new.imag):
          higherYPositive = round(new.imag)
      else:
        if higherYNegative < abs(round(new.imag)):
          higherYNegative = abs(round(new.imag))

  wResult = np.zeros((higherXPositive + higherXNegative + 1, higherYPositive + higherYNegative + 1, 3), dtype = "uint8")
  # Aquí se genera el plano w, utilizando la 
  # fórmula del mapeo bilineal, lo que hace es 
  # pintar de azul los puntos que corresponden 
  # a un punto del plano z.
  for x in range(h):
    for y in range(w):
      num = complex(x, y)
      new =  (a * num + b) / (c * num + d)
      newX = round(new.real)
      newY = round(new.imag)
      # Cuando el resultado es positivo se le
      # suma el resultado del más grande negativo
      # para que quede abajo de los negativos
      if(newX >= 0):
        newX = newX + higherXNegative
      # Los negativos se convierten a la posición
      # que les corresponde
      else:
        newX = higherXNegative - abs(newX)
      if(newY >= 0):
        newY = newY + higherYNegative
      else:
        newY = higherYNegative - abs(newY)
      wResult[newX][newY] = (255, 0, 0)
  return wResult

# Esta es la función de mapeo lineal, es decir
# donde solo se necesita el plano z y las constantes
# a y b, las constante c se considera como 0 y la
# constante d como 1.
def mapeo_lineal(image, a, b):
  # Como es un caso especial del mapeo bilineal, lo 
  # que se hace es que se llama a la función de este 
  # mapeo con los valores de a y b y con c siendo 0 
  # y de siendo 1.
  return mapeo_bilineal(image, a, b, 0, 1)

image = cv2.imread("Original.png")

# La demostración del punto A, que al b ser 0 y
# a pertenece a los reales y no es 0, se produce 
# una magnificación, en este imagen se debería 
# notar que la imagen original se hace más grande
PruebaA = mapeo_lineal(image, 4, 0)
cv2.imwrite("PruebaA1.png", PruebaA)

# En esta imagen se debería notar que la imagen
# original se hace más pequeña
PruebaA2 = mapeo_lineal(image, 0.6, 0)
cv2.imwrite("PruebaA2.png", PruebaA2)

# La demostración del punto B, que al b ser 0 y
# a pertenece a los complejos y no es 0 o es real, 
# se produce una magnificación y una rotación 
PruebaB = mapeo_lineal(image, 2.1 + 2.1j, 0)
cv2.imwrite("PruebaB.png", PruebaB)

# La demostración del punto C, que al a ser 1 y
# b no es 0, se produce un desplazamiento
PruebaC = mapeo_lineal(image, 1, 30 + 50j)
cv2.imwrite("PruebaC.png", PruebaC)

# La demostración del punto D, que al a ser diferente 
# de 0 y b diferente de 0 también, se produce una 
# magnificación una rotación y un desplazamiento
PruebaD = mapeo_lineal(image, 2.1 + 2.1j, 1000 + 50j)
cv2.imwrite("PruebaD.png", PruebaD)


