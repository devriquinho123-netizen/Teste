nomeImagem = 'jota.jpg'

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

def erodir(img, mascara, procurandoPreto = False):
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
            if img[i + a - margemInicio, j + b - margemInicio] / 255 == 1 and mascara[a][b] == 1:
              qtdEncontrada += 1

    
      if qtdEncontrada == qtdProcurada: # Fit
        cinzaConvolucionada[i, j] = 0 if procurandoPreto else 255
      else:
        cinzaConvolucionada[i, j] = 255 if procurandoPreto else 0

  return cinzaConvolucionada

def erodirQtd(qtd, img, mascara, procurandoPreto = False):
  imgRecursiva = erodir(img, mascara, procurandoPreto)
  for i in range(qtd - 1):
    imgRecursiva = erodir(imgRecursiva, mascara, procurandoPreto)
  return imgRecursiva

def dilatar(img, mascara, procurandoPreto = False):
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

def dilatarQtd(qtd, img, mascara, procurandoPreto = False):
  imgRecursiva = dilatar(img, mascara, procurandoPreto)
  for i in range(qtd - 1):
    imgRecursiva = dilatar(imgRecursiva, mascara, procurandoPreto)
  return imgRecursiva

def abertura(img, mascara, procurandoPreto = False):
  return dilatar(erodir(img, mascara, procurandoPreto), mascara, procurandoPreto)

def intersecao(img1, img2, procurandoPreto = False):
  imgIntersecao = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if img1[i][j] == img2[i][j]:
        imgIntersecao[i, j] = img1[i][j]
      else:
        imgIntersecao[i, j] = (255 if procurandoPreto else 0)
  return imgIntersecao

def diferenca(img1, img2, procurandoPreto = False):
  img1Subtraida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if procurandoPreto:
        if img1[i][j] == 0 and img2[i][j] == 255:
          img1Subtraida[i, j] = 0
        else:
          img1Subtraida[i, j] = 255
      else:
        if img1[i][j] == 255 and img2[i][j] == 0:
          img1Subtraida[i, j] = 255
        else:
          img1Subtraida[i, j] = 0
  return img1Subtraida

def unir(img1, img2, procurandoPreto = False):
  imgUnida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if procurandoPreto:
        if img1[i][j] == 0 or img2[i][j] == 0:
          imgUnida[i, j] = 0
        else:
          imgUnida[i, j] = 255
      else:
        if img1[i][j] == 255 or img2[i][j] == 255:
          imgUnida[i, j] = 255
        else:
          imgUnida[i, j] = 0
  return imgUnida

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

mascara = numpy.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

def esqueletizar(img, procurandoPreto = False):
  imgVazia = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if procurandoPreto else 0)
  imgEsqueleto = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if procurandoPreto else 0)
  imgErodida = img.copy()
  imgAberta = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (0 if procurandoPreto else 255)

  while not numpy.array_equal(imgAberta, imgVazia):
    imgAberta = abertura(imgErodida, mascara, procurandoPreto)
    imgDiferenca = diferenca(imgErodida, imgAberta, procurandoPreto)
    imgEsqueleto = unir(imgEsqueleto, imgDiferenca, procurandoPreto)
    imgErodida = erodir(imgErodida, mascara, procurandoPreto)

  return imgEsqueleto

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))

imgEsqueleto = esqueletizar(pretoBranco, False)
cv2.imshow("Esqueleto", resize(imgEsqueleto))
imgEsqueletizada = diferenca(pretoBranco, imgEsqueleto, False)
cv2.imshow("Esqueletizado", resize(imgEsqueletizada))

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