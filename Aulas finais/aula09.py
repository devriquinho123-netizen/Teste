# ==========================================================
# AULA 9 - Erosão e Dilatação (variações de máscara, 3x3 e 5x5)
# Baseado em: minhasAulas/aula9/convolucaoGeneralizado (1).py
# (escolhida por ser a versão completa, com aplicaDilatacao incluída;
#  a outra cópia "convolucaoGeneralizado.py" da mesma pasta não tinha dilatação)
# ==========================================================

nomeIm = 'estrelas.jpg'
import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeIm)

totalPixels = 0
tomCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)


def definirMascara(n):
    mascara = [[255, 0, 255], [0, 0, 0], [255, 0, 255]]
    return mascara


def definirMascara5x5():
    mascara = [[255, 255, 0, 255, 255],
               [255, 0, 0, 0, 255],
               [0, 0, 0, 0, 0],
               [255, 0, 0, 0, 255],
               [255, 255, 0, 255, 255]]
    return mascara


def aplicaErosao(mascara, pretoBranco, quant):
    resultado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    for q in range(quant):
        for i in range(pretoBranco.shape[0] - (len(mascara) - 1)):
            for j in range(pretoBranco.shape[1] - (len(mascara) - 1)):
                hit = True
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            if mascara[k][l] == 0:
                                hit = hit and not (pretoBranco[i + k][j + l])
                        else:
                            if mascara[k][l] == 0:
                                hit = hit and not (resultado[i + k][j + l])
                if hit:
                    resultado[i + 1][j + 1] = 0
                else:
                    resultado[i][j] = 255
    return resultado


def aplicaDilatacao(mascara, pretoBranco, quant):
    resultado = numpy.zeros((imagem.shape[0] + 2, imagem.shape[1] + 2, quant), dtype=numpy.uint8)
    imagemDilatada = numpy.zeros((imagem.shape[0] + 2, imagem.shape[1] + 2), dtype=numpy.uint8)
    for v in range(quant - 1):
        for m in range(imagem.shape[0]):
            for n in range(imagem.shape[1]):
                resultado[m][n][v] = 255
    for q in range(quant):
        for i in range(pretoBranco.shape[0] - (len(mascara) - 1)):
            for j in range(pretoBranco.shape[1] - (len(mascara) - 1)):
                hit = False
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            if mascara[k][l] == 0:
                                hit = hit or not (pretoBranco[i + k][j + l])
                        else:
                            if mascara[k][l] == 0:
                                hit = hit or not (resultado[i + k][j + l][q - 1])
                if hit:
                    resultado[i + 1][j + 1][q] = 0
                else:
                    resultado[i + 1][j + 1][q] = 255

    for m in range(imagem.shape[0]):
        for n in range(imagem.shape[1]):
            imagemDilatada[m][n] = resultado[m][n][quant - 1]

    return imagemDilatada


histograma = 256 * [0]
for i in range(imagem.shape[0]):
    for j in range(imagem.shape[1]):
        tomCinza[i][j] = (imagem[i][j].sum() // 3)
        histograma[tomCinza[i][j]] += 1
        if tomCinza[i][j] < 210:
            pretoBranco[i][j] = 0
        else:
            pretoBranco[i][j] = 255

pixel = 256 * [0]
for i in range(256):
    pixel[i] = i

plt.xlabel('pixel')
plt.ylabel('qtd')
plt.title('Histograma - imagem tons de cinza')
plt.bar(pixel, histograma, color='blue')
plt.show()

mascara = definirMascara5x5()
mascara2 = definirMascara(3)
quant = int(input("Entre com quantas vezes você quer aplicar a erosão: "))
erosao = aplicaErosao(mascara, pretoBranco, quant)
dilatacao1 = aplicaDilatacao(mascara, erosao, quant)
dilatacao2 = aplicaDilatacao(mascara2, erosao, quant)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Preto e Branco", pretoBranco)
cv2.imshow("Erosao da imagem", erosao)
cv2.imshow("Dilatação da imagem com mascara 5x5 em cima da erosão", dilatacao1)
cv2.imshow("Dilatação da imagem com mascara 3x3 em cima da erosão", dilatacao2)
cv2.waitKey(0)
