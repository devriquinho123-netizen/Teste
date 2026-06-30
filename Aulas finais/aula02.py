# ============================================================
# AULA 02 - Histograma e Limiarização (Thresholding)
# ============================================================
# Baseado nos arquivos: procimg/aula2/histograma.py, histogramas.py,
#                        limiarizacao.py, limiarizacao-2.py
# (Não havia implementação própria do usuário para esta aula.)
# ============================================================

import cv2
import numpy
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Parte 1 - Histograma da imagem em tons de cinza
# ----------------------------------------------------------
nomeImagem = 'pudim.jpg'

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cinza[i, j] = (imagem[i][j].sum()) // 3
        histograma[cinza[i, j]] += 1

print(histograma)

pixel = 256 * [0]
for i in range(256):
    pixel[i] = i

plt.xlabel("Cor")
plt.ylabel("Quantidade")
plt.title("Histograma da imagem em Tons de Cinza")
plt.bar(pixel, histograma, color='black', width=1)
plt.show()

# ----------------------------------------------------------
# Parte 2 - Histogramas por canal (cinza, R, G, B)
# ----------------------------------------------------------
cinza2 = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histogramaCinza = numpy.zeros(256, dtype=int)
histogramaRed = numpy.zeros(256, dtype=int)
histogramaGreen = numpy.zeros(256, dtype=int)
histogramaBlue = numpy.zeros(256, dtype=int)

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cinza2[i, j] = (imagem[i][j].sum()) // 3
        histogramaCinza[cinza2[i, j]] += 1
        histogramaRed[r] += 1
        histogramaGreen[g] += 1
        histogramaBlue[b] += 1

fig, ((x0y0, x0y1), (x1y0, x1y1)) = plt.subplots(2, 2, sharex=True)

subplots = [x0y0, x0y1, x1y0, x1y1]
histogramas = [histogramaCinza, histogramaRed, histogramaGreen, histogramaBlue]
colors = ['black', 'red', 'green', 'blue']
label = ['Cinza', 'Vermelho', 'Verde', 'Azul']

for i in range(4):
    subplots[i].bar(pixel, histogramas[i], color=colors[i], width=1)
    subplots[i].set_xlabel("Cor")
    subplots[i].set_ylabel("Quantidade")
    subplots[i].set_title("Histograma de Tons de " + label[i])

fig.tight_layout()
plt.show()

# ----------------------------------------------------------
# Parte 3 - Limiarização simples (um corte)
# ----------------------------------------------------------
nomeImagem3 = 'arroz-feijao.jpg'

imagem3 = cv2.imread(nomeImagem3)

cinza3 = numpy.zeros((imagem3.shape[0], imagem3.shape[1]), dtype=numpy.uint8)
branco = numpy.zeros((imagem3.shape[0], imagem3.shape[1]), dtype=numpy.uint8)
preto = numpy.zeros((imagem3.shape[0], imagem3.shape[1]), dtype=numpy.uint8)
preto_branco = numpy.zeros((imagem3.shape[0], imagem3.shape[1]), dtype=numpy.uint8)
histograma3 = numpy.zeros(256, dtype=int)

corte = 104

for i in range(0, imagem3.shape[0]):
    for j in range(0, imagem3.shape[1]):
        (b, g, r) = imagem3[i, j]
        cor = (imagem3[i][j].sum()) // 3
        cinza3[i, j] = cor
        if (cor > corte):
            branco[i, j] = cor
            preto[i, j] = 255
            preto_branco[i, j] = 255
        else:
            branco[i, j] = 255
            preto[i, j] = cor
        histograma3[cor] += 1

plt.xlabel("Cor")
plt.ylabel("Quantidade")
plt.title("Histograma da imagem em Tons de Cinza")
plt.bar(pixel, histograma3, color='black', width=1)
# plt.show()

def resize(img):
    return cv2.resize(img, (600, 360), interpolation=cv2.INTER_AREA)

cv2.imshow("Imagem Original", resize(imagem3))
cv2.imshow("Tons de Cinza", resize(cinza3))
cv2.imshow("> 104", resize(branco))
cv2.imshow("< 104", resize(preto))
cv2.imshow("Preto e Branco", resize(preto_branco))
cv2.waitKey(0)

# ----------------------------------------------------------
# Parte 4 - Limiarização em múltiplas faixas (dois cortes)
# ----------------------------------------------------------
nomeImagem4 = 'bandeira-franca.jpg'

imagem4 = cv2.imread(nomeImagem4)

cinza4 = numpy.zeros((imagem4.shape[0], imagem4.shape[1]), dtype=numpy.uint8)
cor1 = numpy.ones((imagem4.shape[0], imagem4.shape[1]), dtype=numpy.uint8) * 255
cor2 = numpy.ones((imagem4.shape[0], imagem4.shape[1]), dtype=numpy.uint8) * 255
cor3 = numpy.ones((imagem4.shape[0], imagem4.shape[1]), dtype=numpy.uint8) * 255
histograma4 = 256 * [0]

corte1 = 73
corte2 = 156

for i in range(0, imagem4.shape[0]):
    for j in range(0, imagem4.shape[1]):
        (b, g, r) = imagem4[i, j]
        cor = (imagem4[i][j].sum()) // 3
        cinza4[i, j] = cor
        if (cor <= corte1):
            cor1[i, j] = cor
        elif (cor <= corte2):
            cor2[i, j] = cor
        else:
            cor3[i, j] = cor
        histograma4[cor] += 1

plt.xlabel("Cor")
plt.ylabel("Quantidade")
plt.title("Histograma da imagem em Tons de Cinza")
plt.bar(pixel, histograma4, color='black', width=1)
# plt.show()

cv2.imshow("Imagem Original", resize(imagem4))
cv2.imshow("Tons de Cinza", resize(cinza4))
cv2.imshow("Cor 1", resize(cor1))
cv2.imshow("Cor 2", resize(cor2))
cv2.imshow("Cor 3", resize(cor3))
cv2.waitKey(0)
