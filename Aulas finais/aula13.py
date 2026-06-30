# ==========================================================
# AULA 13 - Esqueletização (Transformação Esqueleto via Abertura)
# Baseado em: minhasAulas/aula13/esqueletizacao.py
# (mantidas apenas as funções realmente usadas no pipeline de
#  esqueletização: erosão, dilatação, abertura -auxiliar-, diferença,
#  união e a função "esqueletizacao" em si. Removidas as funções de
#  contorno, preencheBuraco e componenteConexa, que já foram isoladas
#  nos arquivos das aulas 11 e 12)
# ==========================================================

nomeIm = 'letraE.png'
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
            mascara[i].append(0)
    return mascara


def aplicaErosao(mascara, pretoBranco, quant):
    meioMascara = len(mascara) // 2
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
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
                    resultado[i + meioMascara][j + meioMascara] = 0
                else:
                    resultado[i + meioMascara][j + meioMascara] = 255
    return resultado


def aplicaDilatacao(mascara, pretoBranco, quant):
    resultado = numpy.full((imagem.shape[0] + 2, imagem.shape[1] + 2, quant), 255, dtype=numpy.uint8)
    imagemDilatada = numpy.full((imagem.shape[0] + 2, imagem.shape[1] + 2), 255, dtype=numpy.uint8)
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


def aplicarAbertura(mascara, pretoBranco, quant=1):
    erosao = aplicaErosao(mascara, pretoBranco, quant)
    resultado = aplicaDilatacao(mascara, erosao, quant)
    return resultado


def verificaIgualdade(img1, img2):
    flag = True
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j] != img2[i][j]:
                flag = False
    return flag


def verificaVazio(imagem1):
    imagemVazio = numpy.full((imagem1.shape[0], imagem1.shape[1]), 255, dtype=numpy.uint8)
    return verificaIgualdade(imagem1, imagemVazio)


def uniao(img1, img2):
    resp = img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img2[i][j] == 0:
                resp[i][j] = 0
    return resp


def diferenca(img1, img2):
    resp = img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j] == 0 and img2[i][j] == 0:
                resp[i][j] = 255
    return resp


def esqueletizacao(imagemPB, mascara):
    imagemAux = imagemPB.copy()
    resultadoAux = aplicarAbertura(mascara, imagemAux)
    resultadoFinal = diferenca(imagemAux, resultadoAux)
    cv2.imshow(f"Resultado final 1", resultadoFinal)
    cv2.waitKey(0)
    q = 1
    while not verificaVazio(resultadoAux):
        print(f"executando {q} vezes a erosão\n")
        imagemAux = aplicaErosao(mascara, imagemAux, 1)
        resultadoAux = aplicarAbertura(mascara, imagemAux)
        resultadoFinal = uniao(resultadoFinal, diferenca(imagemAux, resultadoAux))
        if q % 10 == 0:
            cv2.imshow(f"Resultado da  {q}º abertura", resultadoAux)
            cv2.imshow(f"Resultado da  {q}º uniao das diferencas", resultadoFinal)
            cv2.waitKey(0)
        q += 1
    return resultadoFinal


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

mascara = definirMascara(3)
esqueleto = esqueletizacao(pretoBranco, mascara)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Preto e Branco", pretoBranco)
cv2.imshow("Esqueleto da imagem", esqueleto)
cv2.waitKey(0)
