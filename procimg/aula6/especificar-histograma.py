#nomeImagem = 'arroz-feijao.jpg'
nomeImagem = 'paisagem.jfif'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
cinzaEqualizado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
cinzaEspecificado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)

histograma = numpy.zeros(256, dtype=int)
histogramaNormalizado = numpy.zeros(256, dtype=float)
histogramaNormalizadoAcumulado = numpy.zeros(256, dtype=float)
histogramaEqualizado = numpy.zeros(256, dtype=int)

histogramaEspecificado = numpy.zeros(256, dtype=int)
histogramaEspecificadoNormalizado = numpy.zeros(256, dtype=float)
histogramaEspecificadoNormalizadoAcumulado = numpy.zeros(256, dtype=float)
nivelCinzaHistogramaEspecificadoNormalizadoAcumulado = numpy.zeros(256, dtype=int)
histogramaAposEspecificacao = numpy.zeros(256, dtype=int)

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
  histogramaNormalizado[i] = histograma[i] / (imagem.shape[0] * imagem.shape[1])
  if i > 0:
    histogramaNormalizadoAcumulado[i] = histogramaNormalizadoAcumulado[i-1] + histogramaNormalizado[i]
  else:
    histogramaNormalizadoAcumulado[i] = histogramaEspecificadoNormalizado[i]

nivelCinzaHistogramaEqualizado = colunaTmenos1()

def criarHistogramaEspecificado(n):
  soma = 0
  total = 0
  match n:
    case 0:
      for i in range(0, 256):
        histogramaEspecificado[i] = soma
        total += soma
        soma += 1
    case 1:
      for i in range(0, 256):
        histogramaEspecificado[i] = soma
        total += soma
        soma -= 1
    case 2:
      soma = 123
      for i in range(0, 256):
        histogramaEspecificado[i] = soma
        total += soma
    case 3:
      for i in range(0, 256):
        histogramaEspecificado[i] = soma
        total += soma
        if i >= 256/2:
          soma -= 10
        else:
          soma += 10
    case 4:
      for i in range(0, 256):
        histogramaEspecificado[i] = soma
        total += soma
        if i > 100 and i < 150:
          soma = 100
        if i >= 150:
          soma = 0
    case 5:
      for i in range(0, 256):
        histogramaEspecificado[i] = 2*pow(i-128, 2) + 100
        total += histogramaEspecificado[i]
  return total

total = criarHistogramaEspecificado(4)

for i in range(0, 256):
  histogramaEspecificadoNormalizado[i] = histogramaEspecificado[i] / total
  if i > 0:
    histogramaEspecificadoNormalizadoAcumulado[i] = histogramaEspecificadoNormalizadoAcumulado[i-1] + histogramaEspecificadoNormalizado[i]
  else:
    histogramaEspecificadoNormalizadoAcumulado[i] = histogramaEspecificadoNormalizado[i]
  nivelCinzaHistogramaEspecificadoNormalizadoAcumulado[i] = round(histogramaEspecificadoNormalizadoAcumulado[i] * 255)

def colunaMapeamento():
  col = 256*[255]
  iEsp = 0
  ant = nivelCinzaHistogramaEspecificadoNormalizadoAcumulado[iEsp]
  for iEqu in range(0, 256):
    atual = nivelCinzaHistogramaEqualizado[iEqu]
    while (ant + 1 <= 255) and (atual >= (ant + 0.5)):
      iEsp += 1
      ant = nivelCinzaHistogramaEspecificadoNormalizadoAcumulado[iEsp]
    col[iEqu] = ant
    if (ant == 255): break
  return col

mapeamento = colunaMapeamento()

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = cinza[i, j]
    corEqualizada = nivelCinzaHistogramaEqualizado[cor]
    histogramaEqualizado[corEqualizada] += 1
    cinzaEqualizado[i, j] = corEqualizada

    corEspecificada = mapeamento[cor]
    histogramaAposEspecificacao[corEspecificada] += 1
    cinzaEspecificado[i, j] = corEspecificada

def resize(img):
  return cv2.resize(img, (555, 375), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Tons de Cinza Equalizado", resize(cinzaEqualizado))
cv2.imshow("Tons de Cinza Especificado", resize(cinzaEspecificado))

pixel = list(range(256))
fig, ((x0y0, x0y1), (x1y0, x1y1), (x2y0, x2y1), (x3y0, x3y1), (x4y0, x4y1)) = plt.subplots(5, 2, sharex=True)
subplots = [x0y0, x0y1, x1y0, x1y1, x2y0, x2y1, x3y0, x3y1, x4y0, x4y1]
histogramas = [histograma, histogramaNormalizado, histogramaNormalizadoAcumulado, histogramaEqualizado, histogramaEspecificado, histogramaEspecificadoNormalizado, histogramaEspecificadoNormalizadoAcumulado, nivelCinzaHistogramaEspecificadoNormalizadoAcumulado, mapeamento, histogramaAposEspecificacao]
labels = ["Histograma", "Histograma Normalizado", "Histograma Normalizado Acumulado", "Histograma Equalizado", "Histograma Especificado", "Histograma Especificado Normalizado", "Histograma Especificado Normalizado Acumulado", "Nível Cinza Histograma Especificado Normalizado Acumulado", "Mapeamento", "Histograma Após Especificação"]

for i in range(len(histogramas)):
  subplots[i].bar(pixel, histogramas[i], color='black', width = 1)
  subplots[i].set_xlabel("Cor")
  subplots[i].set_ylabel("Quantidade")
  subplots[i].set_title(labels[i])

fig.tight_layout()
plt.show()

cv2.waitKey(0)