import cv2
import numpy as np

# Función para determinar si una función tiene inverso o no
# si b * c - a * d es 0 significa que no tiene inverso, pero
# si no es 0, significa que sí tiene.
def mapeo_inverso_existe(a, b, c, d):
  result = b * c - a * d
  return result != 0

def calcula_tamanno(h, w, a, b, c ,d):
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
  
  return higherXPositive, higherXNegative, higherYPositive, higherYNegative


# Función que representa al mapeo bilineal, 
# genera el plano w con la imagen a través del plano z 
# de a, b, c y d.
def mapeo_bilineal(image, a, b, c, d):
  # Primero se revisa si el mapeo inverso se puede hacer
  if not mapeo_inverso_existe(a,b,c,d):
    return image

  (h, w) = image.shape[:2]
  higherXPositive, higherXNegative, higherYPositive, higherYNegative = calcula_tamanno(h, w, a, b, c ,d)
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
        newX = higherYNegative - abs(newY)
      wResult[newX][newY] = image[x][y]
  return wResult

# Función que hace la transformación de la
# imagen usando mapeo inverso.
# Genera el plano w a través del plano z 
# representado por una imagen y las constantes 
# de a, b, c y d.
def mapeo_inverso(image, a, b, c, d):
  # Primero se revisa si el mapeo inverso se puede hacer
  # debido a que se utiliza
  if not mapeo_inverso_existe(a,b,c,d):
    return image

  (h, w) = image.shape[:2]
  higherXPositive, higherXNegative, higherYPositive, higherYNegative = calcula_tamanno(h, w, a, b, c ,d)
  h2 = higherXPositive + higherXNegative + 1
  w2 = higherYPositive + higherYNegative + 1
  wResult = np.zeros((h2, w2, 3), dtype = "uint8")
  
  # Mapeo de los puntos en el plano w
  # tomando los resultados que se obtiene
  # al sacar la inversa
  for x in range(h2):
    for y in range(w2):
      num = complex(x, y)
      inv =  (-d * num + b) / (c * num - a)
      invX = round(inv.real)
      invY = round(inv.imag)
      if invX < h and invY < w and invX >= 0 and invY >= 0:
        wResult[x][y] = image[invX][invY]

  return wResult

# Función para hacer la interpolación en
# colindacia N, solo se hacen los calculos
# si la N = 4 o N = 8 
def interpolacion(image, N):
  (h, w) = image.shape[:2]
  wResult = np.zeros((h, w, 3), dtype = "uint8")
  # Se crean las matrices para calcular el
  # promedio solo con los valores deseados
  if(N == 4):
    vals = np.array([[0,1,0],[1,0,1],[0,1,0]]) / 4
  elif(N == 8):
    vals = np.array([[1,1,1],[1,0,1],[1,1,1]]) / 8
  for x in range(h):
    for y in range(w):
      mean = 0
      for xVals in range(vals.shape[0]):
        for yVals in range(vals.shape[1]):
          if vals[xVals][yVals] != 0:
            imgX = x+xVals-1
            imgY = y+yVals-1
            # Se ajusta el X y Y de la imagen
            # original para obtener los valores
            # correctos, en este caso los bordes
            # toman el valor que tenga el punto
            # que se revisa actualmente
            if imgX < 0 or imgX >= h-1:
              imgX = x
            if imgY < 0 or imgY >= w-1:
              imgY = y
            mean += vals[xVals][yVals] * image[imgX][imgY]
      wResult[x][y] = mean
  return wResult


image = cv2.imread("Original.png")

# Punto 2 mapeo directo con los valores
# a = 2.1+2.1j; b = 0; c = 0.003; d = 1+1j
imagen2 = mapeo_bilineal(image, 2.1+2.1j, 0, 0.003, 1+1j)
cv2.imwrite("imagen2.png", imagen2)

# Punto 3 mapeo inverso con los valores
# a = 2.1+2.1j; b = 0; c = 0.003; d = 1+1j
imagen3 = mapeo_inverso(image, 2.1+2.1j, 0, 0.003, 1+1j)
cv2.imwrite("imagen3.png", imagen3)

# Punto 4 mapeo inverso e interpolación en
# colindancia N=4
imagen4 = interpolacion(imagen3, 4)
cv2.imwrite("imagen4.png", imagen4)

# Punto 5 mapeo inverso e interpolación en
# colindancia N=8
imagen5 = interpolacion(imagen3, 8)
cv2.imwrite("imagen5.png", imagen5)

# Punto 6 imagen2 con filtro gausseano
# máscara 5x5
imagen6 = cv2.GaussianBlur(imagen2,(5,5),0)
cv2.imwrite("imagen6.png", imagen6)

# Punto 7 imagen4 con filtro gausseano
# máscara 5x5
imagen7 = cv2.GaussianBlur(imagen4,(5,5),0)
cv2.imwrite("imagen7.png", imagen7)

# Punto 8 imagen5 con filtro gausseano
# máscara 5x5
imagen8 = cv2.GaussianBlur(imagen5,(5,5),0)
cv2.imwrite("imagen8.png", imagen8)