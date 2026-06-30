nomeImagem = 'pizza.png'

import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

img_cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
img_curva2R = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
img_curvaRmais100 = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
img_curvaNegativo = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
img_curvaParabolica = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)

def curva2R(pixel):
    return 255 if (2*pixel > 255) else 2*pixel

def curvaRmais100(pixel):
    return 255 if (pixel + 100 > 255) else pixel + 100

def curvaNegativo(pixel):
    return 255 - pixel

def curvaParabolica(pixel):
    return ((pixel/256)**2) * 256 # (pixel**2)/256

for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
        cor = (imagem[i][j].sum()) // 3
        img_cinza[i, j] = cor
        img_curva2R[i, j] = curva2R(cor)
        img_curvaRmais100[i, j] = curvaRmais100(cor)
        img_curvaNegativo[i, j] = curvaNegativo(cor)
        img_curvaParabolica[i, j] = curvaParabolica(cor)
    
fig, ((x0y0, x0y1), (x1y0, x1y1)) = plt.subplots(2, 2, sharex=True)
subplots = [x0y0, x0y1, x1y0, x1y1]
curvas = [
    { 'label': 's = 2r',             'function': curva2R},
    { 'label': 's = r + 100',        'function': curvaRmais100},
    { 'label': 's = 255 - r',        'function': curvaNegativo},
    { 'label': 's = ((1/256)*r)**2', 'function': curvaParabolica},
]

pixel = list(range(256))
y = 256*[0]

for i in range(4):
    for j in range(256):
        y[j] = curvas[i]['function'](j)
    subplots[i].plot(pixel, y, color="red")
    subplots[i].set_xlabel("Origem")
    subplots[i].set_ylabel("Destino")
    subplots[i].set_title("Curva de tom: " + curvas[i]['label'])

def resize(img):
    return cv2.resize(img, (400, 400), interpolation=cv2.INTER_AREA)

cv2.imshow("Tons de Cinza", resize(img_cinza))
cv2.imshow("s = 2r", resize(img_curva2R))
cv2.imshow("s = r + 100", resize(img_curvaRmais100))
cv2.imshow("Negativo", resize(img_curvaNegativo))
cv2.imshow("Parabolica", resize(img_curvaParabolica))

fig.tight_layout()
plt.show()

cv2.waitKey(0)