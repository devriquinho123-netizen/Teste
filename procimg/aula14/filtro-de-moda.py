nomeImagem = 'perry.jfif'

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

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      arrayPixels = []

      for a in range(0, len(mascara)):
        for b in range(0, len(mascara[0])):
          arrayPixels.append(img[i + a - margemInicio, j + b - margemInicio])
      
      valores, contagens = numpy.unique(arrayPixels, return_counts=True)
      indiceModa = numpy.argmax(contagens)
      moda = valores[indiceModa]

      cinzaConvolucionada[i, j] = moda

  return cinzaConvolucionada

def convolucionarQtd(qtd, img, mascara):
  imgRecursiva = convolucionar(img, mascara)
  for i in range(qtd - 1):
    imgRecursiva = convolucionar(imgRecursiva, mascara)
  return imgRecursiva

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
imgConvolucionada = convolucionar(cinza, masc(7))
cv2.imshow("Convolucionada Moda", resize(imgConvolucionada))

cv2.waitKey(0)