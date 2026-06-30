nomeImagem = 'papagaio.png'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
cinzaEqualizado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)
histogramaNormalizado = numpy.zeros(256, dtype=float)
histogramaNormalizadoAcumulado = numpy.zeros(256, dtype=float)
histogramaEqualizado = numpy.zeros(256, dtype=int)

def p(r):
    return histograma[r] / (imagem.shape[0] * imagem.shape[1])

def T(r):
    soma = 0
    for i in range(0, r):
        soma += p(i)
    return soma

def Tmenos1(s):
    ant = 0
    r = 0
    ts = T(s)
    for r in range(0, 256):
        ant = r/255
        prox = ant + 1/255
        if (ts >= ant and ts < prox):
            break
    return r

def colunaTmenos1meu():
    col = 256*[255]
    ant = 0
    antp = ant / 255
    prox = 1
    proxp = prox / 255
    for atual in range(0, 256):
      sk = histogramaNormalizadoAcumulado[atual]
      if (abs(sk - antp) < abs(sk - proxp)):
        col[atual] = ant
      else:
        while ant <= 254 and (abs(sk - antp) >= abs(sk - proxp)):
          ant = prox
          prox = ant + 1
          antp = ant / 255
          proxp = prox / 255
        col[atual] = ant
      if (ant == 255): break
    return col

def colunaTmenos1():
    col = 256*[255]
    ant = 0
    for atual in range(0, 256):
      sk = histogramaNormalizadoAcumulado[atual]
      while (ant+1) <= 255 and sk >= (ant + 0.5) / 255:
        ant += 1
      col[atual] = ant
      if (ant == 255): break
    return col

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        cor = (imagem[i][j].sum()) // 3
        cinza[i, j] = cor
        histograma[cor] += 1

for i in range(0, 256):
    histogramaNormalizado[i] = p(i)
    histogramaNormalizadoAcumulado[i] = T(i)

quintaColuna = colunaTmenos1()

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        corEqualizada = quintaColuna[cinza[i, j]]
        histogramaEqualizado[corEqualizada] += 1
        cinzaEqualizado[i, j] = corEqualizada

def resize(img):
    return cv2.resize(img, (400, 380), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Tons de Cinza Equalizado", resize(cinzaEqualizado))

pixel = list(range(256))
fig, ((x0y0, x0y1), (x1y0, x1y1)) = plt.subplots(2, 2, sharex=True)
subplots = [x0y0, x0y1, x1y0, x1y1]
histogramas = [histograma, histogramaNormalizado, histogramaNormalizadoAcumulado, histogramaEqualizado]
labels = ["Histograma", "Histograma Normalizado", "Histograma Normalizado Acumulado", "Histograma Equalizado"]

for i in range(4):
    subplots[i].bar(pixel, histogramas[i], color='black', width = 1)
    subplots[i].set_xlabel("Cor")
    subplots[i].set_ylabel("Quantidade")
    subplots[i].set_title(labels[i])

fig.tight_layout()
plt.show()

cv2.waitKey(0)