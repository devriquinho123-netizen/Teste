nomeImagem = 'formas.jpg'

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

def hit(img, mascara, procurandoPreto = False):
  margemInicio = math.floor(len(mascara) / 2)
  margemFinal = len(mascara) - margemInicio - 1
  cinzaConvolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      encontrou = False
      
      a = 0
      while a < len(mascara) and not encontrou:
        b = 0
        while b < len(mascara[0]) and not encontrou:
          if procurandoPreto:
            if mascara[a][b] == 1 and img[i + a - margemInicio, j + b - margemInicio] == 0:
              encontrou = True
          else:
            if mascara[a][b] == 1 and img[i + a - margemInicio, j + b - margemInicio] / 255 == 1:
              encontrou = True
          b += 1
        a += 1
    
      if encontrou:
        cinzaConvolucionada[i, j] = 0 if procurandoPreto else 255
      else:
        cinzaConvolucionada[i, j] = 255 if procurandoPreto else 0

  return cinzaConvolucionada

def hitQtd(qtd, img, mascara, procurandoPreto = False):
  imgRecursiva = hit(img, mascara, procurandoPreto)
  for i in range(qtd - 1):
    imgRecursiva = hit(imgRecursiva, mascara, procurandoPreto)
  return imgRecursiva

def intersecao(img1, img2, procurandoPreto = False):
  imgIntersecao = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if img1[i][j] == img2[i][j]:
        imgIntersecao[i, j] = img1[i][j]
      else:
        imgIntersecao[i, j] = (255 if procurandoPreto else 0)
  return imgIntersecao

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

mascara = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

def extrairComponentesConectados(img, pixels, componentesPretos = False):
  imgExtraida = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if componentesPretos else 0)
  imgExtraidaAnterior = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if componentesPretos else 0)

  for pixel in pixels:  
    imgExtraida[pixel[1], pixel[0]] = 0 if componentesPretos else 255

  cv2.imshow("Inicial", resize(imgExtraida))

  while not numpy.array_equal(imgExtraidaAnterior, imgExtraida):
    imgExtraidaAnterior = imgExtraida.copy()
    imgExtraida = hitQtd(1, imgExtraida, mascara, componentesPretos)
    imgExtraida = intersecao(imgExtraida, img, componentesPretos)

  return imgExtraida

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))

pixels = [[140, 100]]
imgExtraida = extrairComponentesConectados(pretoBranco, pixels, True)
cv2.imshow("Componentes Extraídos", resize(imgExtraida))

pixel = list(range(256))
fig, ((x0y0)) = plt.subplots(1, 1, sharex=True)
subplots = [x0y0]
histogramas = [histograma]
labels = ["Histograma"]

for i in range(len(histogramas)):
  subplots[i].bar(pixel, histogramas[i], color='black', width = 1)
  subplots[i].set_xlabel("Cor")
  subplots[i].set_ylabel("Quantidade")
  subplots[i].set_title(labels[i])

fig.tight_layout()
#plt.show()

cv2.waitKey(0)