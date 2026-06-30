nomeImagem = 'bolas.jpg'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 225

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

def inverte(img):
  imgInvertida = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i][j] == 255:
        imgInvertida[i, j] = 0
      else:
        imgInvertida[i, j] = 255
  return imgInvertida

def resize(img):
  return cv2.resize(img, (287, 285), interpolation=cv2.INTER_AREA)

mascara = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

def preencher(img, pixels, buracosPretos = False):
  imgInvertida = inverte(img)
  imgBuracos = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (0 if buracosPretos else 255)
  imgBuracosAnterior = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (0 if buracosPretos else 255)

  for pixel in pixels:  
    imgBuracos[pixel[1], pixel[0]] = 255 if buracosPretos else 0

  cv2.imshow("Buracos Iniciais", resize(imgBuracos))

  while not numpy.array_equal(imgBuracosAnterior, imgBuracos):
    imgBuracosAnterior = imgBuracos.copy()
    imgBuracos = hitQtd(1, imgBuracos, mascara, not buracosPretos)
    imgBuracos = intersecao(imgBuracos, imgInvertida, not buracosPretos)

  cv2.imshow("Invertida", resize(imgInvertida))
  cv2.imshow("Buracos", resize(imgBuracos))
  
  imgPreenchida = unir(img, imgBuracos)
  return imgPreenchida

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))

pixels = [[33, 33], [103, 27], [200, 25], [143, 83], [258, 80], [53, 90], [3, 102], [100, 114], [232, 132], [59, 166], [132, 172], [284, 199], [216, 209], [32, 254], [130, 260], [224, 264], [284, 274]]
imgPreenchida = preencher(pretoBranco, pixels, True)
cv2.imshow("Preenchida", resize(imgPreenchida))

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