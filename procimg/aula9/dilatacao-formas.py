nomeImagem = 'formas.jpg'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 100

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor
    histograma[cor] += 1
    if cor > divisor:
      pretoBranco[i, j] = 255

# Máscara 3x3 Cruz
mascara3x3Cruz = numpy.array([[0, 1, 0], [1, 1, 1], [0,  1, 0]])

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
          elif mascara[a][b] == 1 and img[i + a - margemInicio, j + b - margemInicio] / 255 == 1:
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

def resize(img):
  return cv2.resize(img, (325, 205), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))
cv2.imshow("Preto e Branco Dilatada 3x3", resize(hitQtd(1, pretoBranco, masc(3), True)))
cv2.imshow("Preto e Branco Dilatada 3x3 Cruz", resize(hitQtd(1, pretoBranco, mascara3x3Cruz, True)))
cv2.imshow("Preto e Branco Dilatada 5x5", resize(hitQtd(1, pretoBranco, masc(5), True)))
cv2.imshow("Preto e Branco Dilatada 7x7", resize(hitQtd(1, pretoBranco, masc(7), True)))
cv2.imshow("Preto e Branco Dilatada 9x9", resize(hitQtd(1, pretoBranco, masc(9), True)))
cv2.imshow("Preto e Branco Dilatada 11x11", resize(hitQtd(1, pretoBranco, masc(11), True)))
cv2.imshow("Preto e Branco Dilatada 13x13", resize(hitQtd(1, pretoBranco, masc(13), True)))
cv2.imshow("Preto e Branco Dilatada 15x15", resize(hitQtd(1, pretoBranco, masc(15), True)))
cv2.imshow("Preto e Branco Dilatada 17x17", resize(hitQtd(1, pretoBranco, masc(17), True)))
cv2.imshow("Preto e Branco Dilatada 19x19", resize(hitQtd(1, pretoBranco, masc(19), True)))
cv2.imshow("Preto e Branco Dilatada 21x21", resize(hitQtd(1, pretoBranco, masc(21), True)))
cv2.imshow("Preto e Branco Dilatada 23x23", resize(hitQtd(1, pretoBranco, masc(23), True)))
cv2.imshow("Preto e Branco Dilatada 25x25", resize(hitQtd(1, pretoBranco, masc(25), True)))
cv2.imshow("Preto e Branco Dilatada 25x25 2x", resize(hitQtd(2, pretoBranco, masc(25), True)))

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