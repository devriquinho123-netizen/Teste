nomeImagem = 'lua.jpg'

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

def filtroDeMedia(img, num):
  mascara = masc(num)
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

def unir(img1, img2, k):
  imgUnida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      novoValor = int(img1[i][j]) + k * int(img2[i][j])
      if novoValor < 0:
        imgUnida[i, j] = 0
      elif novoValor > 255:
        imgUnida[i, j] = 255
      else:
        imgUnida[i, j] = novoValor
  return imgUnida

def subtrair(img1, img2):
  img1Subtraida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      novoValor = int(img1[i][j]) - int(img2[i][j])
      if novoValor < 0:
        img1Subtraida[i, j] = 0
      elif novoValor > 255:
        img1Subtraida[i, j] = 255
      else:
        img1Subtraida[i, j] = novoValor
  return img1Subtraida

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
imgPassaBaixa = filtroDeMedia(cinza, 3)
cv2.imshow("Embaçado", resize(imgPassaBaixa))
imgDiferenca = subtrair(cinza, imgPassaBaixa)
cv2.imshow("Máscara", resize(imgDiferenca))
imgFinal = unir(cinza, imgDiferenca, 2)
cv2.imshow("Final", resize(imgFinal))

cv2.waitKey(0)