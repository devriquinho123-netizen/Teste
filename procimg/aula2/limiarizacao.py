nomeImagem = 'arroz-feijao.jpg'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

#imagem.shape[1] (Largura em pixels)
#imagem.shape[0] (Altura em pixels)
#imagem.shape[2] (Qtd de canais)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
branco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
preto = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
preto_branco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

corte = 104

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cor = (imagem[i][j].sum()) // 3
        cinza[i, j] = cor
        if (cor > corte):
            branco[i, j] = cor
            preto[i, j] = 255
            preto_branco[i, j] = 255
        else:
            branco[i, j] = 255
            preto[i, j] = cor
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
cv2.imshow("> 104", resize(branco))
cv2.imshow("< 104", resize(preto))
cv2.imshow("Preto e Branco", resize(preto_branco))
cv2.waitKey(0)
