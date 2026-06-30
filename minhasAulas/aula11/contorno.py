nomeIm = 'contornoTeste.png'
import cv2 
import numpy 
import matplotlib.pyplot as plt 
imagem = cv2.imread(nomeIm) 

totalPixels = 0
tomCinza =  numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 
pretoBranco= numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 

def definirMascaraCruz():
    mascara= [[255,0,255],[0,0,0],[255,0,255]]
    return mascara

def definirMascara(n):
    mascara=[]
    for i in range(n):
        mascara.append([])
        for j in range(n):
            mascara[i].append(0)
    return mascara



def aplicaErosao(mascara, pretoBranco, quant):
    #filtro=[]
    meioMascara= len(mascara)//2
    resultado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
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
    resultado = numpy.zeros((imagem.shape[0]+2, imagem.shape[1]+2, quant), dtype=numpy.uint8)
    imagemDilatada= numpy.zeros((imagem.shape[0]+2, imagem.shape[1]+2), dtype=numpy.uint8)
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


def aplicarAbertura(mascara, pretoBranco, quant):
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
 


mascara= definirMascara(3)
mascaraCruz= definirMascaraCruz()

quant= int(input("Entre com quantas vezes você quer aplicar as operacoes: "))
erosao1= aplicaErosao(mascara, pretoBranco, quant)
resultadoFinal1= encontraContorno(pretoBranco, erosao1)

erosao2= aplicaErosao(mascaraCruz, pretoBranco, quant)
resultadoFinal2= encontraContorno(pretoBranco, erosao2)

cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Preto e Branco", pretoBranco)
cv2.imshow("Erosao da imagem com elemento estruturante quadrado", erosao1)
cv2.imshow("Resultado Final com elemento estruturante quadrado", resultadoFinal1)
cv2.imshow("Erosao da imagem com elemento estruturante cruz", erosao2)
cv2.imshow("Resultado Final com elemento estruturante cruz", resultadoFinal2)
cv2.waitKey(0)
