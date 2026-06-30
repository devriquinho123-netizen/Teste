# ==========================================================
# AULA 12 - Extração de Componentes Conectados (RECONSTRUÇÃO)
# ATENÇÃO: você não tinha uma pasta "aula12" própria.
# A função "componenteConexa" aparece dentro de
# minhasAulas/aula13/esqueletizacao.py (e se repete nas aulas seguintes,
# acumulada). Extraí ela junto com as funções de apoio que usa
# (aplicaDilatacao, pontoPartida, intersecaoResultados, verificaIgualdade),
# que são as mesmas da aula 9/10/11, montando o equivalente ao
# procimg/aula12/extracao.py (extrairComponentesConectados).
# ==========================================================

nomeIm = 'formas.jpg'  # ajuste para a imagem correspondente da aula
import cv2
import numpy
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeIm)

totalPixels = 0
tomCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)


def definirMascaraCruz():
    mascara = [[255, 0, 255], [0, 0, 0], [255, 0, 255]]
    return mascara


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


def pontoPartida(i, j):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    resultado[i][j] = 0
    return resultado


def intersecaoResultados(resultado1, resultado2):
    resultado3 = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for i in range(resultado3.shape[0]):
        for j in range(resultado3.shape[1]):
            if resultado1[i][j] == 0 and resultado2[i][j] == 0:
                resultado3[i][j] = 0
    return resultado3


def verificaIgualdade(img1, img2):
    flag = True
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j] != img2[i][j]:
                flag = False
    return flag


def componenteConexa(mascara, imagemPB, pontoInicial):
    # pontoInicial: tupla (i, j) com um pixel preto dentro do componente desejado
    novaImagem = pontoPartida(pontoInicial[0], pontoInicial[1])
    imagemAnterior = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    k = 1
    while not verificaIgualdade(imagemAnterior, novaImagem):
        print(f"executou {k} vezes")
        dilatacao = aplicaDilatacao(mascara, novaImagem, 1)
        imagemAnterior = novaImagem.copy()
        novaImagem = intersecaoResultados(dilatacao, imagemPB)
        if k % 15 == 0:
            cv2.imshow(f"Imagem na iteracao {k} ", novaImagem)
            cv2.waitKey(0)
        k += 1
    return novaImagem


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

mascaraCruz = definirMascaraCruz()

# Ajuste o ponto inicial (i, j) para um pixel preto dentro do componente que deseja extrair
pontoInicial = (76, 107)
componente = componenteConexa(mascaraCruz, pretoBranco, pontoInicial)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Preto e Branco", pretoBranco)
cv2.imshow("Componente Extraído", componente)
cv2.waitKey(0)
