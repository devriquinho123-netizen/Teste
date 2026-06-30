nomeImagem = 'componentes2.jpg'

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

def rotular(img):
  imgComRotulos = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  rotulo = 1
  equivalencias = {}

  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i, j] != 255:
        esquerda = imgComRotulos[i - 1, j] if i - 1 >= 0 else 0
        cima = imgComRotulos[i, j - 1] if j - 1 >= 0 else 0

        if esquerda != 0:
          imgComRotulos[i, j] = esquerda
          if cima != 0: # tem os 2
            visitados = set()
            while esquerda in equivalencias and esquerda not in visitados:
              visitados.add(esquerda)
              esquerda = equivalencias[esquerda]
            equivalencias[cima] = esquerda
        elif cima != 0:
          imgComRotulos[i, j] = cima
        else:
          imgComRotulos[i, j] = rotulo
          rotulo += 1
    
  rotulos_diferentes = set([])
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      pixel = imgComRotulos[i, j]

      if pixel != 0 and pixel in equivalencias:
        imgComRotulos[i, j] = equivalencias[pixel] * 30

      if imgComRotulos[i, j] != 0:
        rotulos_diferentes.add(imgComRotulos[i, j])
      else:
        imgComRotulos[i, j] = 255

  print("Componentes: " + str(len(rotulos_diferentes)))

  return imgComRotulos

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))
rotulada = rotular(pretoBranco)
cv2.imshow("Componentes Rotulados", resize(rotulada))

cv2.waitKey(0)