# ==========================================================
# AULA 14 - Filtros Estatísticos (Média/Baixa, Mediana, Moda, Ordem)
# Baseado em: minhasAulas/aula14/filtros.py
# (mantidas apenas aplicaFiltroBaixo, aplicaFiltroMediana, aplicaFiltroModa,
#  aplicaFiltroOrdem, encontraModa e somaMascara, que são o conteúdo real
#  desta aula. Removidas todas as funções de morfologia/esqueleto/contorno
#  que estavam acumuladas no arquivo - já isoladas nas aulas 10 a 13)
# ==========================================================

nomeIm = 'ruido.png'
import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeIm)

totalPixels = 0
tomCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)


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
        for i in range(tomCinza.shape[0] - (len(mascara) - 1)):
            for j in range(tomCinza.shape[1] - (len(mascara) - 1)):
                soma = 0
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            soma += int(int(tomCinza[i + k][j + l]) * mascara[k][l])
                        else:
                            soma += int(int(resultado[i + k][j + l]) * mascara[k][l])
                soma = soma // somaMascara(mascara)
                resultado[i][j] = soma
    return resultado


def aplicaFiltroMediana(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0] - (len(mascara) - 1)):
            for j in range(tomCinza.shape[1] - (len(mascara) - 1)):
                elementos = []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            elementos.append(int(int(tomCinza[i + k][j + l]) * mascara[k][l]))
                        else:
                            elementos.append(int(int(resultado[i + k][j + l]) * mascara[k][l]))
                elementos.sort()
                indice = len(elementos) // 2
                resultado[i][j] = elementos[indice]
    return resultado


def encontraModa(lista):
    moda = quant = 0
    for i in lista:
        if quant < lista.count(i):
            moda = i
            quant = lista.count(i)
    return moda


def aplicaFiltroModa(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0] - (len(mascara) - 1)):
            for j in range(tomCinza.shape[1] - (len(mascara) - 1)):
                elementos = []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            elementos.append(int(int(tomCinza[i + k][j + l]) * mascara[k][l]))
                        else:
                            elementos.append(int(int(resultado[i + k][j + l]) * mascara[k][l]))
                moda = encontraModa(elementos)
                resultado[i][j] = moda
    return resultado


def aplicaFiltroOrdem(mascara, tomCinza, tipo, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0] - (len(mascara) - 1)):
            for j in range(tomCinza.shape[1] - (len(mascara) - 1)):
                elementos = []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if q == 0:
                            elementos.append(int(int(tomCinza[i + k][j + l]) * mascara[k][l]))
                        else:
                            elementos.append(int(int(resultado[i + k][j + l]) * mascara[k][l]))
                resultado[i][j] = max(elementos) if (tipo == 1) else min(elementos)
    return resultado


histograma = 256 * [0]
for i in range(imagem.shape[0]):
    for j in range(imagem.shape[1]):
        tomCinza[i][j] = (imagem[i][j].sum() // 3)
        histograma[tomCinza[i][j]] += 1
        if tomCinza[i][j] < 100:
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

q = int(input("Entre com o tamanho da mascara: "))
mascara = definirMascara(q)
resultadoBaixo = aplicaFiltroBaixo(mascara, tomCinza)
resultadoMediana = aplicaFiltroMediana(mascara, tomCinza)
resultadoModa = aplicaFiltroModa(mascara, tomCinza)
resultadoOrdemMax = aplicaFiltroOrdem(mascara, tomCinza, 1)
resultadoOrdemMin = aplicaFiltroOrdem(mascara, tomCinza, 0)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Tons de Cinza", tomCinza)
cv2.imshow("Imagem Filtro Baixo (Média)", resultadoBaixo)
cv2.imshow("Imagem Filtro Mediana", resultadoMediana)
cv2.imshow("Imagem Filtro Moda", resultadoModa)
cv2.imshow("Imagem Filtro Ordem Max", resultadoOrdemMax)
cv2.imshow("Imagem Filtro Ordem Min", resultadoOrdemMin)
cv2.waitKey(0)
