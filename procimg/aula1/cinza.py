nomeImagem = 'pudim.jpg'

import cv2
import numpy

imagem = cv2.imread(nomeImagem)

print('Largura em pixels: ', end='')
print(imagem.shape[1])
print('Altura em pixels: ', end='')
print(imagem.shape[0])
print('Qtd de canais: ', end='')
print(imagem.shape[2])

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        (b, g, r) = imagem[i, j]
        cinza[i, j] = (imagem[i][j].sum()) // 3
        # cinza[i, j] = b/3 + g/3 + r/3

cv2.imshow("Tons de Cinza", cinza)

cv2.imshow("Imagem Original", imagem)
cv2.waitKey(0)

cv2.imwrite("saida.jpg", imagem)