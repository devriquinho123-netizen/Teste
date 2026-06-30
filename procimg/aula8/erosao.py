nomeImagem = 'moedas.jpg'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 190

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor
    histograma[cor] += 1
    if cor > divisor:
      pretoBranco[i, j] = 255

# Máscara 3x3 Preenchida
mascara3x3 = numpy.ones((3, 3), dtype=int)

# Máscara 3x3 Cruz
mascara3x3Cruz = numpy.array([[0, 1, 0], [1, 1, 1], [0,  1, 0]])

# Máscara 5x5 Preenchida
mascara5x5 = numpy.ones((5, 5), dtype=int)

# Máscara 7x7 Preenchida
mascara7x7 = numpy.ones((7, 7), dtype=int)

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
            qtdEncontrada += mascara[a][b] * (img[i + a - margemInicio, j + b - margemInicio] / 255)

    
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

def resize(img):
  return cv2.resize(img, (478, 374), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(pretoBranco))
cv2.imshow("Preto e Branco Erodida 3x3", resize(fit(pretoBranco, mascara3x3, True)))
cv2.imshow("Preto e Branco Erodida 3x3 Cruz", resize(fit(pretoBranco, mascara3x3Cruz, True)))
cv2.imshow("Preto e Branco Erodida 5x5", resize(fit(pretoBranco, mascara5x5, True)))
cv2.imshow("Preto e Branco Erodida 7x7", resize(fit(pretoBranco, mascara7x7, True)))
cv2.imshow("Preto e Branco Erodida 3x3 - 2x", resize(fitQtd(2, pretoBranco, mascara3x3, True)))
cv2.imshow("Preto e Branco Erodida 7x7 - 2x", resize(fitQtd(2, pretoBranco, mascara7x7, True)))

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
plt.show()

cv2.waitKey(0)