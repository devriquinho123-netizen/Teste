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
        esquerdaCima = imgComRotulos[i - 1, j - 1] if i > 0 and j > 0 else 0
        direitaCima = imgComRotulos[i - 1, j + 1] if i > 0 and j < img.shape[1] else 0
        esquerda = imgComRotulos[i - 1, j] if i > 0 else 0
        cima = imgComRotulos[i, j - 1] if j > 0 else 0

        vizinhos = []
        if esquerdaCima != 0:
          vizinhos.append(esquerdaCima)
        if direitaCima != 0:
          vizinhos.append(direitaCima)
        if esquerda != 0:
          vizinhos.append(esquerda)
        if cima != 0:
          vizinhos.append(cima)

        if vizinhos:
          menorRotulo = min(vizinhos)
          imgComRotulos[i, j] = menorRotulo

          for rotuloExistente in vizinhos:
            if rotuloExistente != menorRotulo:
              equivalencias[rotuloExistente] = menorRotulo
        else:
          imgComRotulos[i, j] = rotulo
          rotulo += 1
    
  rotulos_diferentes = set([])
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      pixel = imgComRotulos[i, j]

      if pixel != 0 and pixel in equivalencias:
        imgComRotulos[i, j] = equivalencias[pixel]

      if imgComRotulos[i, j] != 0:
        rotulos_diferentes.add(imgComRotulos[i, j])
        imgComRotulos[i, j] = imgComRotulos[i, j] * 30
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