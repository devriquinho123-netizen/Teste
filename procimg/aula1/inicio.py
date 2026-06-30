nomeImagem = 'python-logo.png'

import cv2

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