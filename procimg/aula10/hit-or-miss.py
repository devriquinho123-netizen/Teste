nomeImagem = 'formas.jpg'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 235

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor
    histograma[cor] += 1
    if cor > divisor:
      pretoBranco[i, j] = 255

def masc(num):
  return numpy.ones((num, num), dtype=int)

def fit(img, mascara, procurandoPreto = False):
  margemInicio = math.floor(len(mascara) / 2)
  margemFinal = len(mascara) - margemInicio - 1
  cinzaConvolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  qtdProcurada = numpy.count_nonzero(mascara == 1)

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      qtdEncontrada = 0

      for a in range(0, len(mascara)):
        for b in range(0, len(mascara[0])):
          if procurandoPreto:
            if img[i + a - margemInicio, j + b - margemInicio] == 0 and mascara[a][b] == 1:
              qtdEncontrada += 1
          else:
            if img[i + a - margemInicio, j + b - margemInicio] == 1 and mascara[a][b] == 1:
              qtdEncontrada += 1

    
      if qtdEncontrada == qtdProcurada: # Fit
        cinzaConvolucionada[i, j] = 0 if procurandoPreto else 255
      else:
        cinzaConvolucionada[i, j] = 255 if procurandoPreto else 0

  return cinzaConvolucionada

def fitQtd(qtd, img, mascara, procurandoPreto = False):
  imgRecusiva = fit(img, mascara, procurandoPreto)
  for i in range(qtd - 1):
    imgRecusiva = fit(imgRecusiva, mascara, procurandoPreto)
  return imgRecusiva

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

def inverte(img):
  imgInvertida = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i][j] == 255:
        imgInvertida[i, j] = 0
      else:
        imgInvertida[i, j] = 255
  return imgInvertida

def intersecao(img1, img2):
  imgIntersecao = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if img1[i][j] == img2[i][j]:
        imgIntersecao[i, j] = img1[i][j]
      else:
        imgIntersecao[i, j] = 255
  return imgIntersecao

def resize(img):
  return cv2.resize(img, (284, 253), interpolation=cv2.INTER_AREA)

mascSize = 15

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))

imgErodida = fitQtd(1, pretoBranco, masc(mascSize), True)
cv2.imshow("Erodida", resize(imgErodida))

imgComplemento = inverte(pretoBranco)
cv2.imshow("Complemento", resize(imgComplemento))

mascaraC = 1 - numpy.pad(masc(mascSize), pad_width=1)
imgComplementoErodida = fitQtd(1, imgComplemento, mascaraC, True)
cv2.imshow("Complemento Erodida", resize(imgComplementoErodida))

imgIntersecao = intersecao(imgErodida, imgComplementoErodida)
cv2.imshow("Intersecao", resize(imgIntersecao))

imgIntersecaoDilatada = hitQtd(1, imgIntersecao, masc(mascSize), True)
cv2.imshow("Intersecao Dilatada", resize(imgIntersecaoDilatada))

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