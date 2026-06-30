nomeIm = 'moedas.webp'
import cv2 
import numpy 
import matplotlib.pyplot as plt 
imagem = cv2.imread(nomeIm) 

totalPixels = 0
tomCinza =  numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 
pretoBranco= numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8) 

def definirMascara(n):
    mascara= [[255,0,255],[0,0,0],[255,0,255]]
    """for i in range(n):
        mascara.append([0]*n)
        for j in range(n):
            #if((i+j)%2==0):
            mascara[i][j]= 1
            #else:
             #   mascara[i][j]= 0
             """
    return mascara

def definirMascara5x5():
    mascara= [[255,255, 0,255, 255],
              [255,0,0, 0, 255],
              [0,0,0,0,0],
              [255,0,0, 0, 255],
              [255,255, 0,255, 255]]
    """for i in range(n):
        mascara.append([0]*n)
        for j in range(n):
            #if((i+j)%2==0):
            mascara[i][j]= 1
            #else:
             #   mascara[i][j]= 0
             """
    return mascara


def aplicaFiltro(mascara, tomCinza, quant):
    #filtro=[]
    filtro = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    for q in range(quant):
        for i in range(tomCinza.shape[0]-2):
            #filtro.append([0]*tomCinza.shape[1])
            for j in range(tomCinza.shape[1]-2):
                soma= 0
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        #print(f"{tomCinza[i+k][j+l]}  * {mascara[k][l]} \n")
                        if(q == 0):
                            soma+= int(int(tomCinza[i+k][j+l]) * mascara[k][l])
                        else:
                            soma+= int(int(filtro[i+k][j+l]) * mascara[k][l])
                #print(f"valor da soma {soma} \n")
                if(soma<0):
                    filtro[i][j]=0
                elif(soma>255):
                    filtro[i][j]= 255
                else:
                    filtro[i][j]=soma
    return filtro 
                    
    


def aplicaErosao(mascara, pretoBranco, quant):
    #filtro=[]
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
                    resultado[i+1][j+1]=0
                else:
                    resultado[i][j]=255
    return resultado


def aplicaErosao5x5(mascara, pretoBranco, quant):
    #filtro=[]
    resultado = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
    for q in range(quant):
        for i in range(pretoBranco.shape[0]-(len(mascara)-1)):
            #filtro.append([0]*tomCinza.shape[1])
            for j in range(pretoBranco.shape[1]-(len(mascara)-1)):
                hit=True 
                for k in range(len(mascara)):
                    for l in range(len(mascara)):
                        if(q==0):
                            if(k==1 or l ==1):
                                hit= hit and  not(pretoBranco[i+k][j+l])  
                        else:
                            if(k==1 or l ==1):
                                hit= hit and  not(resultado[i+k][j+l])  
                if(hit):
                    resultado[i+1][j+1]=0
                else:
                    resultado[i][j]=255
    return resultado
            
histograma = 256*[0]
for i in range(imagem.shape[0]):     
     for j in range(imagem.shape[1]):
         tomCinza[i][j] = (imagem[i][j].sum()//3)
         histograma[tomCinza[i][j]] += 1 
         if(tomCinza[i][j]<210):
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
 

#n= int(input("Entre com o tamanho da mascara: "))
"""quant= int(input("Entre com quantas vezes você quer aplicar o filtro: "))
mascara= definirMascara(3)
print(f"mascara é {mascara}\n\n")
filtro= aplicaFiltro(mascara, tomCinza, quant)
print(f"O filtro é : {filtro} \n\n")
"""
mascara= definirMascara(3)
quant= int(input("Entre com quantas vezes você quer aplicar a erosão: "))
erosao= aplicaErosao(mascara, pretoBranco, quant)
 
cv2.imshow("tomCinza", tomCinza) 
cv2.imshow("imagem Original", imagem)
cv2.imshow("imagem Preto e Branco", pretoBranco)
cv2.imshow("Erosao da imagem", erosao)
cv2.waitKey(0)
