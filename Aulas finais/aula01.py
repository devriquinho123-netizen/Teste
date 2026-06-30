# ============================================================
# AULA 01 - Introdução ao OpenCV: leitura de imagem, propriedades
#           e separação de canais de cor
# ============================================================
# Baseado nos arquivos: procimg/aula1/inicio.py, cinza.py, canais.py
# (Não havia implementação própria do usuário para esta aula em
# "minhasAulas", então o conteúdo foi reconstruído a partir do procimg.)
# ============================================================

import cv2
import numpy

# ----------------------------------------------------------
# Parte 1 - Leitura da imagem e propriedades básicas
# ----------------------------------------------------------
nomeImagem = 'python-logo.png'

imagem = cv2.imread(nomeImagem)

print('Largura em pixels: ', end='')
print(imagem.shape[1])
print('Altura em pixels: ', end='')
print(imagem.shape[0])
print('Qtd de canais: ', end='')
print(imagem.shape[2])

print('Número de linhas: ', end='')
print(imagem.shape)
print('Qtd de elementos: ', end='')
print(imagem.size)
print('Qtd de dimensões: ', end='')
print(imagem.ndim)

(b, g, r) = imagem[0, 0]
print(b, g, r)

cv2.imshow("Imagem Original", imagem)
cv2.waitKey(0)

cv2.imwrite("saida.jpg", imagem)

# ----------------------------------------------------------
# Parte 2 - Conversão para tons de cinza (média dos canais)
# ----------------------------------------------------------
nomeImagem2 = 'pudim.jpg'

imagem2 = cv2.imread(nomeImagem2)

cinza = numpy.zeros((imagem2.shape[0], imagem2.shape[1]), dtype=numpy.uint8)

for i in range(0, imagem2.shape[0]):
    for j in range(0, imagem2.shape[1]):
        (b, g, r) = imagem2[i, j]
        cinza[i, j] = (imagem2[i][j].sum()) // 3
        # cinza[i, j] = b/3 + g/3 + r/3

cv2.imshow("Tons de Cinza", cinza)
cv2.imshow("Imagem Original 2", imagem2)
cv2.waitKey(0)

# ----------------------------------------------------------
# Parte 3 - Separação dos canais B, G e R
# ----------------------------------------------------------
nomeImagem3 = 'python-logo.png'

imagem3 = cv2.imread(nomeImagem3)

canalBlue = numpy.zeros((imagem3.shape[0], imagem3.shape[1], imagem3.shape[2]), dtype=numpy.uint8)
canalGreen = numpy.zeros((imagem3.shape[0], imagem3.shape[1], imagem3.shape[2]), dtype=numpy.uint8)
canalRed = numpy.zeros((imagem3.shape[0], imagem3.shape[1], imagem3.shape[2]), dtype=numpy.uint8)

canalBlue[:, :, 0] = imagem3[:, :, 0]
canalGreen[:, :, 1] = imagem3[:, :, 1]
canalRed[:, :, 2] = imagem3[:, :, 2]

cv2.imshow("Canal Blue", canalBlue)
cv2.imshow("Canal Green", canalGreen)
cv2.imshow("Canal Red", canalRed)

cv2.imshow("Imagem Original 3", imagem3)
cv2.waitKey(0)
