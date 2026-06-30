nomeImagem = 'bandeira-franca.jpg'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

#imagem.shape[1] (Largura em pixels)
#imagem.shape[0] (Altura em pixels)
#imagem.shape[2] (Qtd de canais)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
cor1 = numpy.ones((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) * 255
cor2 = numpy.ones((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) * 255
cor3 = numpy.ones((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) * 255
histograma = 256*[0]

corte1 = 73
corte2 = 156

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cor = (imagem[i][j].sum()) // 3
        cinza[i, j] = cor
        if (cor <= corte1):
            cor1[i, j] = cor
        elif (cor <= corte2):
            cor2[i, j] = cor
        else:
            cor3[i, j] = cor
        histograma[cor] += 1

pixel = 256*[0]
for i in range(256):
    pixel[i] = i

plt.xlabel("Cor")
plt.ylabel("Quantidade")
plt.title("Histograma da imagem em Tons de Cinza")
plt.bar(pixel, histograma, color='black', width = 1)
#plt.show()

def resize(img):
    return cv2.resize(img, (600, 360), interpolation=cv2.INTER_AREA)

cv2.imshow("Imagem Original", resize(imagem))
cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Cor 1", resize(cor1))
cv2.imshow("Cor 2", resize(cor2))
cv2.imshow("Cor 3", resize(cor3))
cv2.waitKey(0)
