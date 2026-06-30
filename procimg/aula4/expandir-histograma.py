nomeImagem = 'lugar.png'

import cv2
import numpy
import matplotlib.pyplot as plt

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
        return 255*((cor-r1)/(r2-r1))

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
    subplots[i].bar(pixel, histogramas[i], color='black', width = 1)
    subplots[i].set_xlabel("Cor")
    subplots[i].set_ylabel("Quantidade")
    subplots[i].set_title(labels[i])

fig.tight_layout()
plt.show()

cv2.waitKey(0)