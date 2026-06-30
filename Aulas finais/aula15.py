nomeIm = 'lua.jpg'
import cv2
import numpy
import matplotlib.pyplot as plt
imagem = cv2.imread(nomeIm)

totalPixels = 0
tomCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)


def definirMascaraSobel(direcao):
    if(direcao == "x"):
        mascara = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    else:
        mascara = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    return mascara


def definirMascaraRobert(direcao):
    if(direcao == "x"):
        mascara = [[1, 0], [0, -1]]
    else:
        mascara = [[0, 1], [-1, 0]]
    return mascara


def definirMascaraPrewitt(direcao):
    if(direcao == "x"):
        mascara = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    else:
        mascara = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    return mascara


def definirMascaraLaplaciano(opcao):
    if(opcao == 1):
        mascara = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    elif(opcao == 2):
        mascara = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    else:
        mascara = [[1, -2, 1], [-2, 4, -2], [1, -2, 1]]
    return mascara


def definirMascara(n):
    mascara = []
    for i in range(n):
        mascara.append([])
        for j in range(n):
            mascara[i].append(1)
    return mascara


def somaMascara(mascara):
    soma = 0
    for i in mascara:
        for j in i:
            soma += j
    return soma


def aplicaFiltroBaixo(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                soma = 0
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q == 0):
                            soma += int(int(tomCinza[i+k][j+l]) * mascara[k][l])
                        else:
                            soma += int(int(resultado[i+k][j+l]) * mascara[k][l])
                soma = soma // somaMascara(mascara)
                resultado[i][j] = soma
    return resultado


def aplicaFiltro(mascara, tomCinza, quant=1):
    resultado = numpy.full((tomCinza.shape[0] + len(mascara), tomCinza.shape[1] + len(mascara)), 255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                soma = 0
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q == 0):
                            soma += int(int(tomCinza[i+k][j+l]) * mascara[k][l])
                        else:
                            soma += int(int(resultado[i+k][j+l]) * mascara[k][l])
                resultado[i][j] = max(min(abs(soma), 255), 0)
    return resultado


def diferenca2(img1, img2):
    resp = img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            resp[i][j] = max(int(img1[i][j]) - int(img2[i][j]), 0)
    return resp


def unir2(img1, img2, k=1):
    resp = img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            resp[i][j] = min(int(img1[i][j]) + k * int(img2[i][j]), 255)
    return resp


def juntarFiltros(img1, img2):
    resultado = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
    for i in range(tomCinza.shape[0]):
        for j in range(tomCinza.shape[1]):
            resultado[i][j] = min(int(img1[i][j]) + int(img2[i][j]), 255)
    return resultado


def resize(img):
    return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)


histograma = 256*[0]
for i in range(imagem.shape[0]):
    for j in range(imagem.shape[1]):
        tomCinza[i][j] = (imagem[i][j].sum()//3)
        histograma[tomCinza[i][j]] += 1
        if(tomCinza[i][j] < 100):
            pretoBranco[i][j] = 0
        else:
            pretoBranco[i][j] = 255

pixel = 256*[0]
for i in range(256):
    pixel[i] = i
plt.xlabel('pixel')
plt.ylabel('qtd')
plt.title('Histograma - imagem tons de cinza')
plt.bar(pixel, histograma, color='blue')
plt.show()

# Sobel
mascaraSobelX = definirMascaraSobel("x")
mascaraSobelY = definirMascaraSobel("y")
sobelX = aplicaFiltro(mascaraSobelX, tomCinza, 1)
sobelY = aplicaFiltro(mascaraSobelY, tomCinza, 1)
sobelJunto = juntarFiltros(sobelX, sobelY)

# Roberts
mascaraRobertX = definirMascaraRobert("x")
mascaraRobertY = definirMascaraRobert("y")
robertX = aplicaFiltro(mascaraRobertX, tomCinza, 1)
robertY = aplicaFiltro(mascaraRobertY, tomCinza, 1)
robertJunto = juntarFiltros(robertX, robertY)

# Prewitt
mascaraPrewittX = definirMascaraPrewitt("x")
mascaraPrewittY = definirMascaraPrewitt("y")
prewittX = aplicaFiltro(mascaraPrewittX, tomCinza, 1)
prewittY = aplicaFiltro(mascaraPrewittY, tomCinza, 1)
prewittJunto = juntarFiltros(prewittX, prewittY)

# Laplaciano
mascaraLaplaciano1 = definirMascaraLaplaciano(1)
mascaraLaplaciano2 = definirMascaraLaplaciano(2)
mascaraLaplaciano3 = definirMascaraLaplaciano(3)
laplaciano1 = aplicaFiltro(mascaraLaplaciano1, tomCinza, 1)
laplaciano2 = aplicaFiltro(mascaraLaplaciano2, tomCinza, 1)
laplaciano3 = aplicaFiltro(mascaraLaplaciano3, tomCinza, 1)

# Alto Reforço: tomCinza - filtroBaixo(tomCinza), depois soma k vezes essa máscara à imagem original
q = int(input("Entre com o tamanho da mascara de suavizacao: "))
mascaraBaixa = definirMascara(q)
k = int(input("Entre com o valor de k: "))
suavizada = aplicaFiltroBaixo(mascaraBaixa, tomCinza)
resultadoMask = diferenca2(tomCinza, suavizada)
resultadoAltoReforco = unir2(tomCinza, resultadoMask, k)

cv2.imshow("imagem Tons de Cinza", resize(tomCinza))
cv2.imshow("Sobel X", resize(sobelX))
cv2.imshow("Sobel Y", resize(sobelY))
cv2.imshow("Sobel Junto", resize(sobelJunto))
cv2.imshow("Roberts X", resize(robertX))
cv2.imshow("Roberts Y", resize(robertY))
cv2.imshow("Roberts Junto", resize(robertJunto))
cv2.imshow("Prewitt X", resize(prewittX))
cv2.imshow("Prewitt Y", resize(prewittY))
cv2.imshow("Prewitt Junto", resize(prewittJunto))
cv2.imshow("Laplaciano 1", resize(laplaciano1))
cv2.imshow("Laplaciano 2", resize(laplaciano2))
cv2.imshow("Laplaciano 3", resize(laplaciano3))
cv2.imshow("Imagem Borrada", resize(suavizada))
cv2.imshow("Mascara do Alto Reforco", resize(resultadoMask))
cv2.imshow(f"Imagem com Alto Reforco (k={k})", resize(resultadoAltoReforco))

cv2.waitKey(0)
