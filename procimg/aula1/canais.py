nomeImagem = 'python-logo'

import cv2
import numpy

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

canalBlue = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)
canalGreen = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)
canalRed = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)

canalBlue[:,:,0] = imagem[:,:,0]
canalGreen[:,:,1] = imagem[:,:,1]
canalRed[:,:,2] = imagem[:,:,2]

cv2.imshow("Canal Blue", canalBlue)
cv2.imshow("Canal Green", canalGreen)
cv2.imshow("Canal Red", canalRed)

cv2.imshow("Imagem Original", imagem)
cv2.waitKey(0)

cv2.imwrite("saida.jpg", imagem)