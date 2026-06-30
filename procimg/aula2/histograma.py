nomeImagem = 'pudim.jpg'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

#imagem.shape[1] (Largura em pixels)
#imagem.shape[0] (Altura em pixels)
#imagem.shape[2] (Qtd de canais)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cinza[i, j] = (imagem[i][j].sum()) // 3
        histograma[cinza[i, j]] += 1

print(histograma)

pixel = 256*[0]
for i in range(256):
    pixel[i] = i

plt.xlabel("Cor")
plt.ylabel("Quantidade")
plt.title("Histograma da imagem em Tons de Cinza")
plt.bar(pixel, histograma, color='black', width = 1)
plt.show()

#cv2.imshow("Tons de Cinza", cinza)
#cv2.imshow("Imagem Original", imagem)
#cv2.waitKey(0)