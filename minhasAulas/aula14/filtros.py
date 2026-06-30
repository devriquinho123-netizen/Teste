nomeIm = 'ruido.png'
import cv2 
import numpy 
import matplotlib.pyplot as plt 
imagem = cv2.imread(nomeIm) 

totalPixels = 0
tomCinza =  numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 
pretoBranco= numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 

def definirMascaraCruz():
   # mascara= [[1,2,1],[2,4,2],[1,2,1]]
    mascara= [[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4], [1,4,7,4,1]]
    return mascara

def definirMascara(n):
    mascara=[]
    for i in range(n):
        mascara.append([])
        for j in range(n):
            mascara[i].append(1)
    return mascara


def aplicaErosao(mascara, pretoBranco, quant):
    #filtro=[]
    meioMascara= len(mascara)//2
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]),255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(pretoBranco.shape[0]-(len(mascara)-1)):
            #filtro.append([0]*tomCinza.shape[1])
            for j in range(pretoBranco.shape[1]-(len(mascara)-1)):
                hit=True 
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q==0):
                            if(mascara[k][l]==0):
                                hit= hit and  not(pretoBranco[i+k][j+l])  
                        else:
                            if(mascara[k][l]==0):
                                hit= hit and  not(resultado[i+k][j+l])  
                if(hit):
                    resultado[i+meioMascara][j+meioMascara]=0
                else:
                    resultado[i+meioMascara][j+meioMascara]=255
    return resultado


def aplicaDilatacao(mascara, pretoBranco, quant):
    #filtro=[]
    resultado = numpy.full((imagem.shape[0]+2, imagem.shape[1]+2, quant),255, dtype=numpy.uint8)
    imagemDilatada= numpy.full((imagem.shape[0]+2, imagem.shape[1]+2), 255, dtype=numpy.uint8)
    for v in range(quant-1):
        for m in range(imagem.shape[0]):
            for n in range(imagem.shape[1]):
                resultado[m][n][v]= 255 
    for q in range(quant):
        for i in range(pretoBranco.shape[0]-(len(mascara)-1)):
            #filtro.append([0]*tomCinza.shape[1])
            for j in range(pretoBranco.shape[1]-(len(mascara)-1)):
                hit=False
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q==0):
                            if(mascara[k][l]==0):
                                hit= hit or not(pretoBranco[i+k][j+l])  
                        else:
                            if(mascara[k][l]==0):
                                hit= hit or not(resultado[i+k][j+l][q-1])  
                if(hit):
                    resultado[i+1][j+1][q]=0
                else:
                    resultado[i+1][j+1][q]=255                     
    for m in range(imagem.shape[0]):
            for n in range(imagem.shape[1]):
                imagemDilatada[m][n]= resultado[m][n][quant-1]                 
               
    return imagemDilatada




def aplicaFiltroBaixo(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]),255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                soma= 0
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        #print(f"{tomCinza[i+k][j+l]}  * {mascara[k][l]} \n")
                        if(q == 0):
                            soma+= int(int(tomCinza[i+k][j+l]) * mascara[k][l])
                        else:
                            soma+= int(int(resultado[i+k][j+l]) * mascara[k][l])
                soma=soma // somaMascara(mascara)
                resultado[i][j]=soma
    return resultado
                    



def aplicaFiltroMediana(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]),255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                elementos= []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q == 0):
                            elementos.append(int(int(tomCinza[i+k][j+l]) * mascara[k][l]))
                        else:
                             elementos.append(int(int(resultado[i+k][j+l]) * mascara[k][l]))
                elementos.sort()
                indice= len(elementos)//2
                resultado[i][j]=elementos[indice]
    return resultado 



def aplicaFiltroModa(mascara, tomCinza, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]),255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                elementos= []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q == 0):
                            elementos.append(int(int(tomCinza[i+k][j+l]) * mascara[k][l]))
                        else:
                             elementos.append(int(int(resultado[i+k][j+l]) * mascara[k][l]))
                moda= encontraModa(elementos)
                resultado[i][j]=moda
    return resultado 



def aplicaFiltroOrdem(mascara, tomCinza,tipo, quant=1):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]),255, dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-(len(mascara)-1)):
            for j in range(tomCinza.shape[1]-(len(mascara)-1)):
                elementos= []
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q == 0):
                            elementos.append(int(int(tomCinza[i+k][j+l]) * mascara[k][l]))
                        else:
                             elementos.append(int(int(resultado[i+k][j+l]) * mascara[k][l]))
                resultado[i][j]= max(elementos) if (tipo==1) else  min(elementos)
    return resultado 
                    

def encontraModa(lista):
    moda=quant=0
    for i in lista:
        if quant<lista.count(i):
            moda=i
            quant=lista.count(i)
    return moda


def complementoPretoBranco(pretoBranco):
    resultado = numpy.zeros((pretoBranco.shape[0], pretoBranco.shape[1]), dtype=numpy.uint8)
    for i in range(pretoBranco.shape[0]):
        for j in range(pretoBranco.shape[1]):
            if(pretoBranco[i][j]==0):
                resultado[i][j]=255
            else:
                resultado[i][j]= 0
    return resultado

def aplicarAbertura(mascara, pretoBranco, quant=1):
    erosao= aplicaErosao(mascara, pretoBranco, quant)
    resultado= aplicaDilatacao(mascara, erosao, quant)
    return resultado

def aplicarFechamento(mascara, pretoBranco, quant):
    dilatacaoLocal= aplicaDilatacao(mascara, pretoBranco, quant)
    resultado= aplicaErosao(mascara, dilatacaoLocal, quant)
    return resultado


def encontraContorno(img1, img2):
    resultado = numpy.full((img1.shape[0], img1.shape[1]), 255, dtype=numpy.uint8)
    for i in range(resultado.shape[0]):
        for j in range(resultado.shape[1]):
            if(img1[i][j]==0 and img2[i][j]==255):
                resultado[i][j]=0
    return resultado


def pontoPartida( i, j):
    resultado = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    resultado[i][j]=0
    return resultado


def intersecaoResultados(resultado1, resultado2):
    resultado3 = numpy.full((imagem.shape[0], imagem.shape[1]), 255, dtype=numpy.uint8)
    for i in range(resultado3.shape[0]):
        for j in range(resultado3.shape[1]):
            if(resultado1[i][j]== 0 and resultado2[i][j]==0):
                resultado3[i][j]= 0
    return resultado3

def verificaIgualdade(img1, img2):
    flag=True
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if(img1[i][j]!=img2[i][j]):
                flag=False
    return flag


def preencheBuraco(mascara,imagemComplementar, imagemPB):
    novaImagem= pontoPartida(50,100)
    imagemAnterior= numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    k=1
    while(not verificaIgualdade(imagemAnterior, novaImagem)):
        print(f"entrou: {k} vezes")
        dilatacao= aplicaDilatacao(mascara, novaImagem, 1)
        imagemAnterior=novaImagem.copy()
        novaImagem= intersecaoResultados(dilatacao, imagemComplementar)
        if(k%10==0):
            cv2.imshow(f"NovaImagem na iteracao {k} ", novaImagem)
            cv2.imshow(f"ImagemAnterior na iteracao {k} ", imagemAnterior)
            cv2.waitKey(0)
        k+=1
        
    imagemPretoBranco= imagemPB.copy()    
    for i in range(imagemPretoBranco.shape[0]):
        for j in range(imagemPretoBranco.shape[1]):
            if(imagemPretoBranco[i][j]==255 and novaImagem[i][j]==0):
                imagemPretoBranco[i][j]=0
    
    return imagemPretoBranco


def componenteConexa(mascara, imagemPB):
    novaImagem= pontoPartida(76, 107)
    imagemAnterior= numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    k=1
    while(not verificaIgualdade(imagemAnterior, novaImagem)):
        print(f"executou {k} vezes")
        dilatacao= aplicaDilatacao(mascara, novaImagem, 1)
        imagemAnterior=novaImagem.copy()
        novaImagem= intersecaoResultados(dilatacao, imagemPB)
        if(k%15==0):
            cv2.imshow(f"Imagem na iteracao {k} ", novaImagem)
            cv2.waitKey(0)
        k+=1
    return novaImagem




def verificaVazio(imagem1):
    imagemVazio= numpy.full((imagem1.shape[0], imagem1.shape[1]),255,  dtype=numpy.uint8)
    return verificaIgualdade(imagem1, imagemVazio)


def uniao(img1, img2):
    resp= img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if(img2[i][j]==0):
                resp[i][j]=0
    return resp

def diferenca(img1, img2):
    resp=  img1.copy()
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if(img1[i][j]==0 and img2[i][j]==0):
                resp[i][j]=255
    return resp



def unirEsqueleto(imgPB, esqComp):
    res= imgPB.copy()
    for i in range(imgPB.shape[0]):
        for j in range(imgPB.shape[1]):
            if(imgPB[i][j]==0 and esqComp[i][j]==255):
                res[i][j]=255
    return res



def esqueletizacao(imagemPB, mascara):
    imagemAux= imagemPB.copy()
    resultadoAux= aplicarAbertura(mascara, imagemAux)
    resultadoFinal= diferenca(imagemAux, resultadoAux)
    cv2.imshow(f"Resultado final 1", resultadoFinal)
    cv2.waitKey(0) 
    q=1
    while(not verificaVazio(resultadoAux)):
        print(f"executando {q} vezes a erosão\n")
        imagemAux= aplicaErosao(mascara, imagemAux, 1)
        resultadoAux= aplicarAbertura(mascara, imagemAux)
        resultadoFinal= uniao(resultadoFinal, diferenca(imagemAux, resultadoAux))   
        if(q%10==0):
            cv2.imshow(f"Resultado da  {q}º abertura", resultadoAux)
            cv2.imshow(f"Resultado da  {q}º uniao das diferencas", resultadoFinal)
            cv2.waitKey(0)     
        q+=1
    return resultadoFinal


def somaMascara(mascara):
    soma=0
    for i in mascara:
        for j in i:
            soma+= j
    return soma      
                


histograma = 256*[0]
for i in range(imagem.shape[0]):     
     for j in range(imagem.shape[1]):
         tomCinza[i][j] = (imagem[i][j].sum()//3)
         histograma[tomCinza[i][j]] += 1 
         if(tomCinza[i][j]<100):
             pretoBranco[i][j]= 0
         else:
             pretoBranco[i][j]=255  
         
         
pixel = 256*[0]
for i in range(256):
    pixel[i] = i
plt.xlabel('pixel')
plt.ylabel('qtd')
plt.title('Histograma - imagem tons de cinza')
plt.bar(pixel, histograma, color='blue')
plt.show()

q= int(input("Entre com o tamanho da mascara: "))
mascara= definirMascara(q)
resultado= aplicaFiltroBaixo(mascara,tomCinza)
resultado2= aplicaFiltroMediana(mascara,tomCinza)
resultado3= aplicaFiltroModa(mascara, tomCinza)
resultado4= aplicaFiltroOrdem(mascara, tomCinza, 1)
resultado5= aplicaFiltroOrdem(mascara, tomCinza, 0)


cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Tons de Cinza", tomCinza)
cv2.imshow("Imagem Filtro Baixo", resultado)
cv2.imshow("Imagem Filtro Mediana", resultado2)
cv2.imshow("Imagem Filtro Moda", resultado3)
cv2.imshow("Imagem Filtro Ordem Max", resultado4)
cv2.imshow("Imagem Filtro Ordem Min", resultado5)
cv2.waitKey(0)
