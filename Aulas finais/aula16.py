nomeIm = 'esqueletoQuadrado.png'
import cv2
import numpy
import matplotlib.pyplot as plt
imagem = cv2.imread(nomeIm)

totalPixels = 0
tomCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
pretoBranco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)


def resize(img):
    return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)


# Rotulação por 4-conectividade (vizinhos: cima e esquerda)
def conectividade4(pretoBranco):
    resultado = numpy.full((pretoBranco.shape[0], pretoBranco.shape[1]), 255, dtype=numpy.uint8)
    marcador = 1
    paresEquivalentes = []
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(pretoBranco[i][j] == 0):
                if(i-1 >= 0 and pretoBranco[i-1][j] == 0 and j-1 >= 0 and pretoBranco[i][j-1] == 0 and resultado[i-1][j] != resultado[i][j-1]):
                    paresEquivalentes.append([min(resultado[i-1][j], resultado[i][j-1]), max(resultado[i-1][j], resultado[i][j-1])])
                    resultado[i][j] = resultado[i-1][j]
                elif(i-1 >= 0 and pretoBranco[i-1][j] == 0):
                    resultado[i][j] = resultado[i-1][j]
                elif(j-1 >= 0 and pretoBranco[i][j-1] == 0):
                    resultado[i][j] = resultado[i][j-1]
                else:
                    resultado[i][j] = marcador
                    marcador += 5
    dicionario = {}
    for k in paresEquivalentes:
        if(k[0] not in dicionario.keys()):
            dicionario[k[0]] = [k[1]]
        else:
            dicionario[k[0]].append(k[1])

    for i in range(resultado.shape[0]):
        for j in range(resultado.shape[1]):
            if resultado[i][j] in dicionario.keys():
                continue
            else:
                for k, l in dicionario.items():
                    if(resultado[i][j] in l):
                        resultado[i][j] = k

    print(dicionario.items())
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(resultado[i][j] != 255):
                resultado[i][j] *= 5
    return resultado


# Rotulação por 8-conectividade (vizinhos: cima, esquerda e diagonal superior-esquerda)
# Acertar lógica da diagonal
def conectividade8(pretoBranco):
    resultado = numpy.full((pretoBranco.shape[0], pretoBranco.shape[1]), 255, dtype=numpy.uint8)
    marcador = 1
    paresEquivalentes = []
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(pretoBranco[i][j] == 0):
                if(i-1 >= 0 and pretoBranco[i-1][j] == 0 and j-1 >= 0 and pretoBranco[i][j-1] == 0 and resultado[i-1][j] != resultado[i][j-1]):
                    paresEquivalentes.append([min(resultado[i-1][j], resultado[i][j-1]), max(resultado[i-1][j], resultado[i][j-1])])
                    resultado[i][j] = resultado[i-1][j]
                elif(i-1 >= 0 and pretoBranco[i-1][j] == 0):
                    resultado[i][j] = resultado[i-1][j]
                elif(j-1 >= 0 and pretoBranco[i][j-1] == 0):
                    resultado[i][j] = resultado[i][j-1]
                elif(j-1 >= 0 and i-1 >= 0 and pretoBranco[i-1][j-1] == 0):
                    resultado[i][j] = resultado[i-1][j-1]
                else:
                    resultado[i][j] = marcador
                    marcador += 5
    dicionario = {}
    for k in paresEquivalentes:
        if(k[0] not in dicionario.keys()):
            dicionario[k[0]] = [k[1]]
        else:
            dicionario[k[0]].append(k[1])

    for i in range(resultado.shape[0]):
        for j in range(resultado.shape[1]):
            if resultado[i][j] in dicionario.keys():
                continue
            else:
                for k, l in dicionario.items():
                    if(resultado[i][j] in l):
                        resultado[i][j] = k

    print(dicionario.items())
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(resultado[i][j] != 255):
                resultado[i][j] *= 5
    return resultado


# Esqueletização por distância às bordas (objeto): para cada pixel preto, calcula a
# menor distância até encontrar um pixel branco nas 4 direções (cima/baixo/esquerda/direita);
# o esqueleto fica marcado nos pixels que atingem a distância máxima encontrada na imagem.
# código certo, não mexa!
def esqueletoNovo(pretoBranco):
    resultado = numpy.full((pretoBranco.shape[0], pretoBranco.shape[1]), 255, dtype=numpy.uint8)
    maximo = 0
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(pretoBranco[i][j] == 0):
                cont = 1
                while(True):
                    if(pretoBranco[i-cont][j] == 255 or pretoBranco[i+cont][j] == 255):
                        break
                    elif(pretoBranco[i][j-cont] == 255 or pretoBranco[i][j+cont] == 255):
                        break
                    else:
                        cont += 1
                maximo = max(maximo, cont)
                resultado[i][j] = cont
    for i in range(resultado.shape[0]):
        for j in range(resultado.shape[1]):
            if(resultado[i][j] == maximo):
                resultado[i][j] = 255

    return resultado


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

rotulada4 = conectividade4(pretoBranco)
rotulada8 = conectividade8(pretoBranco)
esqueleto = esqueletoNovo(pretoBranco)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Tons de Cinza", resize(tomCinza))
cv2.imshow("imagem Preto e Branco", resize(pretoBranco))
cv2.imshow("Componentes Rotulados - 4 Conectividade", resize(rotulada4))
cv2.imshow("Componentes Rotulados - 8 Conectividade", resize(rotulada8))
cv2.imshow("Esqueleto por distancia as bordas", resize(esqueleto))

cv2.waitKey(0)
