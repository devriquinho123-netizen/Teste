nomeImagem = 'pudim.jpg'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

#imagem.shape[1] (Largura em pixels)
#imagem.shape[0] (Altura em pixels)
#imagem.shape[2] (Qtd de canais)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histogramaCinza = numpy.zeros(256, dtype=int)
histogramaRed = numpy.zeros(256, dtype=int)
histogramaGreen = numpy.zeros(256, dtype=int)
histogramaBlue = numpy.zeros(256, dtype=int)

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cinza[i, j] = (imagem[i][j].sum()) // 3
        histogramaCinza[cinza[i, j]] += 1
        histogramaRed[r] += 1
        histogramaGreen[g] += 1
        histogramaBlue[b] += 1

pixel = 256*[0]
for i in range(256):
    pixel[i] = i

fig, ((x0y0, x0y1), (x1y0, x1y1)) = plt.subplots(2, 2, sharex=True)

subplots = [x0y0, x0y1, x1y0, x1y1]
histogramas = [histogramaCinza, histogramaRed, histogramaGreen, histogramaBlue]
colors = ['black', 'red', 'green', 'blue']
label = ['Cinza', 'Vermelho', 'Verde', 'Azul']

for i in range(4):
    subplots[i].bar(pixel, histogramas[i], color=colors[i], width = 1)
    subplots[i].set_xlabel("Cor")
    subplots[i].set_ylabel("Quantidade")
    subplots[i].set_title("Histograma de Tons de " + label[i])

fig.tight_layout()
plt.show()

#cv2.imshow("Tons de Cinza", cinza)
#cv2.imshow("Imagem Original", imagem)
#cv2.waitKey(0)