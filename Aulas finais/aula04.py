# ============================================================
# AULA 04 - Expansão e Equalização de Histograma
# ============================================================
# Baseado nos arquivos: procimg/aula4/expandir-histograma.py,
#                        procimg/aula4/equalizar-histograma.py
# (Não havia implementação própria do usuário para esta aula.)
# ============================================================

import cv2
import numpy
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Parte 1 - Expansão de Histograma
# ----------------------------------------------------------
nomeImagem = 'lugar.png'

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
cinzaExpandido = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)
histogramaExpandido = numpy.zeros(256, dtype=int)

r1 = 87
r2 = 165

def expandir(cor: int):
    if (cor < r1):
        return 0
    elif (cor > r2):
        return 255
    else:
        return 255 * ((cor - r1) / (r2 - r1))

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        cor = (imagem[i][j].sum()) // 3
        cinza[i, j] = cor
        histograma[cor] += 1

        corExpandida = expandir(cor)
        cinzaExpandido[i, j] = corExpandida
        histogramaExpandido[int(corExpandida)] += 1

def resize(img):
    return cv2.resize(img, (400, 380), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Tons de Cinza Expandido", resize(cinzaExpandido))

pixel = list(range(256))
fig, ((x0y0, x0y1)) = plt.subplots(1, 2, sharex=True)
subplots = [x0y0, x0y1]
histogramas = [histograma, histogramaExpandido]
labels = ["Histograma", "Histograma Expandido"]

for i in range(2):
    subplots[i].bar(pixel, histogramas[i], color='black', width=1)
    subplots[i].set_xlabel("Cor")
    subplots[i].set_ylabel("Quantidade")
    subplots[i].set_title(labels[i])

fig.tight_layout()
plt.show()

cv2.waitKey(0)

# ----------------------------------------------------------
# Parte 2 - Equalização de Histograma
# ----------------------------------------------------------
nomeImagem2 = 'papagaio.png'

imagem2 = cv2.imread(nomeImagem2)

cinza2 = numpy.zeros((imagem2.shape[0], imagem2.shape[1]), dtype=numpy.uint8)
cinzaEqualizado = numpy.zeros((imagem2.shape[0], imagem2.shape[1]), dtype=numpy.uint8)
histograma2 = numpy.zeros(256, dtype=int)
histogramaNormalizado = numpy.zeros(256, dtype=float)
histogramaNormalizadoAcumulado = numpy.zeros(256, dtype=float)
histogramaEqualizado = numpy.zeros(256, dtype=int)

def p(r):
    return histograma2[r] / (imagem2.shape[0] * imagem2.shape[1])

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
        ant = r / 255
        prox = ant + 1 / 255
        if (ts >= ant and ts < prox):
            break
    return r

for i in range(0, imagem2.shape[0]):
    for j in range(0, imagem2.shape[1]):
        cor = (imagem2[i][j].sum()) // 3
        cinza2[i, j] = cor
        histograma2[cor] += 1

for i in range(0, 256):
    histogramaNormalizado[i] = p(i)
    histogramaNormalizadoAcumulado[i] = T(i)
    histogramaEqualizado[Tmenos1(i)] += 1

for i in range(0, imagem2.shape[0]):
    for j in range(0, imagem2.shape[1]):
        corEqualizada = Tmenos1(cinza2[i, j])
        cinzaEqualizado[i, j] = corEqualizada

cv2.imshow("Tons de Cinza", resize(cinza2))
cv2.imshow("Tons de Cinza Equalizado", resize(cinzaEqualizado))

fig2, ((y0y0, y0y1), (y1y0, y1y1)) = plt.subplots(2, 2, sharex=True)
subplots2 = [y0y0, y0y1, y1y0, y1y1]
histogramas2 = [histograma2, histogramaNormalizado, histogramaNormalizadoAcumulado, histogramaEqualizado]
labels2 = ["Histograma", "Histograma Normalizado", "Histograma Normalizado Acumulado", "Histograma Equalizado"]

for i in range(4):
    subplots2[i].bar(pixel, histogramas2[i], color='black', width=1)
    subplots2[i].set_xlabel("Cor")
    subplots2[i].set_ylabel("Quantidade")
    subplots2[i].set_title(labels2[i])

fig2.tight_layout()
plt.show()

cv2.waitKey(0)
