nomeImagem = 'sala.jfif'

import cv2
import numpy
import math

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor

# Máscara de Bordas
mascara1 = [[0,  1, 0], [1, -4, 1], [0,  1, 0]]
divisor1 = 1

# Máscara de Bordas mais fortes
mascara2 = [[1,  1, 1], [1, -8, 1], [1,  1, 1]]
divisor2 = 1

# Máscara de Média 3x3
mascara3 = numpy.ones((3, 3), dtype=int)
divisor3 = mascara3.size

# Máscara de Média 4x4
mascara4 = numpy.ones((4, 4), dtype=int)
divisor4 = mascara4.size

# Máscara de Média 5x5
mascara5 = numpy.ones((5, 5), dtype=int)
divisor5 = mascara5.size

# Máscara de Média 8x8
mascara6 = numpy.ones((8, 8), dtype=int)
divisor6 = mascara6.size

# Máscara de Média 11x11
mascara7 = numpy.ones((11, 11), dtype=int)
divisor7 = mascara7.size

# Máscara de Média 2x2
mascara8 = numpy.ones((2, 2), dtype=int)
divisor8 = mascara8.size

mascara = mascara1
divisor = divisor1
margemInicio = math.floor(len(mascara) / 2)
margemFinal = len(mascara) - margemInicio - 1

def convolucionar(img):
  cinzaConvolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)

  for i in range(margemInicio, img.shape[0] - margemFinal):
    for j in range(margemInicio, img.shape[1] - margemFinal):
      novaCor = 0

      for a in range(0, len(mascara)):
        for b in range(0, len(mascara[0])):
          novaCor += (int(img[i + a - margemInicio, j + b - margemInicio]) * mascara[a][b]) / divisor
    
      if novaCor < 0:
        cinzaConvolucionada[i, j] = 0
      elif novaCor > 255:
        cinzaConvolucionada[i, j] = 255
      else:
        cinzaConvolucionada[i, j] = novaCor

  return cinzaConvolucionada

def resize(img):
  return cv2.resize(img, (365, 242), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Tons de Cinza Convolucionada", resize(convolucionar(cinza)))
cv2.imshow("Tons de Cinza Convolucionada 2", resize(convolucionar(convolucionar(cinza))))

cv2.waitKey(0)