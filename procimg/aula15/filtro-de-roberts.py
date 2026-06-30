nomeImagem = 'lego.jpg'

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
  margemInicio = 0
  margemFinal = 1
  cinzaConvolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      novaCor = 0

      for a in range(0, len(mascara)):
        for b in range(0, len(mascara[0])):
          novaCor += (int(img[i + a - margemInicio, j + b - margemInicio]) * mascara[a][b])
    
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

def unir(img1, img2):
  imgUnida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      novoValor = img1[i][j] + img2[i][j]
      if novoValor < 0:
        imgUnida[i, j] = 0
      elif novoValor > 255:
        imgUnida[i, j] = 255
      else:
        imgUnida[i, j] = novoValor
  return imgUnida

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

mascara1 = numpy.array([[1, 0], [0, -1]])
mascara2 = numpy.array([[0, 1], [-1, 0]])

cv2.imshow("Tons de Cinza", resize(cinza))
img1 = convolucionar(cinza, mascara1)
cv2.imshow("Roberts Horizontal", resize(img1))
img2 = convolucionar(cinza, mascara2)
cv2.imshow("Roberts Vertical", resize(img2))
img3 = unir(img1, img2)
cv2.imshow("Roberts Junto", resize(img3))

cv2.waitKey(0)