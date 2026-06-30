nomeImagem = 'sala.jfif'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor

def masc(num):
  return numpy.ones((num, num), dtype=int)

def convolucionar(img, mascara):
  margemInicio = math.floor(len(mascara) / 2)
  margemFinal = len(mascara) - margemInicio - 1
  cinzaConvolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  divisor = numpy.sum(mascara)

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      novaCor = 0

      for a in range(0, len(mascara)):
        for b in range(0, len(mascara[0])):
          novaCor += (int(img[i + a - margemInicio, j + b - margemInicio]) * mascara[a][b]) / divisor
    
      if novaCor < 0:
        cinzaConvolucionada[i, j] = 0
      elif novaCor > 255:
        cinzaConvolucionada[i, j] = 255
      else:
        cinzaConvolucionada[i, j] = novaCor

  return cinzaConvolucionada

def convolucionarQtd(qtd, img, mascara):
  imgRecursiva = convolucionar(img, mascara)
  for i in range(qtd - 1):
    imgRecursiva = convolucionar(imgRecursiva, mascara)
  return imgRecursiva

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

mascara = numpy.array([[1, 4, 7, 4, 1], [4, 16, 26, 16, 4], [7, 26, 41, 26, 7], [4, 16, 26, 16, 4], [1, 4, 7, 4, 1]])

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Convolucionada Gaussiana", resize(convolucionar(cinza, mascara)))

cv2.waitKey(0)