nomeImagem = 'retangulo.jpg'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 80

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor
    histograma[cor] += 1
    if cor > divisor:
      pretoBranco[i, j] = 255

def masc(num):
  return numpy.ones((num, num), dtype=int)

def esqueletonizar(img):
  imgEsqueleto = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  imgLinhaEsqueleto = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  maxDist = 0

  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i, j] != 255:
        distancias = []
        for (deslocY, deslocX) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
          dist = 0
          while True:
            dist += 1
            y = i + (deslocY * dist)
            x = j + (deslocX * dist)
            pixel = img[y, x] if (0 <= y < img.shape[0] and 0 <= x < img.shape[1]) else 255
            if pixel == 255:
              break
          distancias.append(dist)
        
        dist = min(distancias)
        imgEsqueleto[i, j] = dist
        if dist > maxDist:
          maxDist = dist

  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if imgEsqueleto[i, j] == maxDist:
        imgLinhaEsqueleto[i, j] = 255
    
  return (imgEsqueleto, imgLinhaEsqueleto)

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))
(esqueleto, linhaEsqueleto) = esqueletonizar(pretoBranco)
cv2.imshow("Esqueleto", resize(esqueleto))
cv2.imshow("Linha Esqueleto", resize(linhaEsqueleto))

cv2.waitKey(0)