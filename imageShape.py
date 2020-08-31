import cv2
import numpy as np
import os
import random
import math

class imageShape :  # clase
  def __init__(self,width,height):  # se define el constructor
   self.width = width   #se guarda el ancho de la imagen
   self.height = height #se guarda el alto de la imagen
   self.imagen_disponible = 0 #se inicializa la variable que da la informacion de si existe una imagen disponible

  def generateshape(self): #metodo que  genera y almacena (como self.shape) una imagen de tamaño (width, height) correspondiente a un triangulo (0), cuadrado (1), rectángulo (2),o circulo (3).
   self.shape = np.zeros((self.height,self.width,3), np.uint8) #se genera la imagen en negro
   numero = random.randint(0,3) #se genera un numero aleatorio
   figuras = ['triangulo','cuadrado','rectangulo','circulo'] #se crea una lista con los nombres de las figuras a generar
   self.nombre_fig = figuras[numero] #se guardan los nombres de las figuras
   centro_imagen = (int (self.height/2),int(self.width/2))

   if self.nombre_fig == 'triangulo':   #genera triangulo
    long_lados = int(min(self.width, self.height) / 2) # lados del triangulo
    mitad_lado = int(long_lados / 2)  # longitud de la mitad de un lado
    cen_trian = int(math.sqrt(3) * long_lados / 4)  # longitud de la mitad de altura
    # puntos de ubicación de los vertices del triangulo
    p1 = (mitad_lado, -cen_trian)
    p2 = (-mitad_lado, -cen_trian)
    p3 = (0, cen_trian)
    triangulo = np.array([p1, p2, p3])  # arreglo con los puntos
    triangulo = triangulo.astype(np.int)+centro_imagen #le sumo el centro de la imagen para centrar el triangulo
    cv2.drawContours(self.shape, [triangulo], 0, (255, 255, 0), -1)  # dibuja la figura

   if self.nombre_fig == 'cuadrado':     #genera cuadrado
    lado = int(min(self.width,self.height)/2)  #longitud de los lados del triangulo
    lado_medios=int(lado/2)  #mitad de un lado del triangulo
    # puntosn de ubicacion de los vertices del cuadrado
    p1 = (lado_medios ,0)
    p2 = (0,  lado_medios)
    p3 = (0, -lado_medios)
    p4 = (-lado_medios, 0)
    cuadrado = np.array([p3,p1,p2,p4]) #arreglo con los puntos
    cuadrado = cuadrado.astype(np.int)+centro_imagen #le sumo el centro de la imagen para centrar el cuadrado
    cv2.drawContours(self.shape,[cuadrado],0,(255,200,0),-1) #dibujo el cuadrado

   if self.nombre_fig == 'rectangulo':   #genera el rectangulo
    ancho = int(self.width / 2)  # longitud del ancho
    alto = int(self.height / 2)  # longitud del alto
    # ubicacion de los vertices del rectangulo
    p1 = (int(ancho / 2), int(alto / 2))
    p2 = (int(ancho / 2), -int(alto / 2))
    p3 = (-int(ancho / 2), int(alto / 2))
    p4 = (-int(ancho / 2), -int(alto / 2))
    rectangulo = np.array([p3, p1, p2, p4])   #arreglo con los puntos
    rectangulo = rectangulo.astype(np.int) + centro_imagen #le sumo el centro de la imagen para centrar el cuadrado
    cv2.drawContours(self.shape, [rectangulo], 0, (255, 255, 0), -1)  # se dibuja la figura

   if self.nombre_fig == 'circulo':   #genera el circulo
    cv2.circle(self.shape, (int(self.width / 2), int(self.height / 2)),int(min(self.width, self.height) / 4), (255, 255, 0), -1)
    # se centra y se dibuja la imagen sabiendo que el radio es int(min(self.width, self.height) / 4

   self.imagen_disponible = 1 #se actualiza la variable indicando que hay imagen disponible

  def showShape(self):  # metodo para visualiza la imagen disponible en self.shape durante 5 segundos. Si no hay imagen disponible, visualiza una imagen en negro
    if self.imagen_disponible == 1:
     self.imagen_disponible = 0  # se actualiza el estado de la variable
     cv2.imshow('Figura ', self.shape)  # se muestra la figura
     cv2.waitKey(5000) #durante 5 segundos
    else:
     # si no hay imagen disponible se muestra imagen en negro
     cv2.imshow('imagen', np.zeros((self.height, self.width, 3), np.uint8))
     cv2.waitKey(5000) #durante 5 segundos

  def getShape(self):  # metodo que retorna la imagen generada y un string con el nombre de figura generada: ‘triangle’, ‘square’, ‘rectangle’ o ‘circle’
    return self.shape, self.nombre_fig

  def whatShape(self,input_image): # metodo que recibe una imagen de entrada (de fondo negro y objeto claro) que contiene una figura y la clasifica como ‘triangle’, ‘square’, ‘rectangle’ o ‘circle’.
    #Este método retorna un string con el nombre de tipo de figura resultante.
    imagen_copia = input_image.copy()
    #metodo OTSU para umbralizar
    imagen_grices = cv2.cvtColor(imagen_copia, cv2.COLOR_BGR2GRAY)
    ret, image_Binary = cv2.threshold(imagen_grices, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #se almacenan el contorno en la imagen
    contornos, jerarquia = cv2.findContours(image_Binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    perimetro = cv2.arcLength(contornos[0], True) #perimetro del contorno
    contorno_aprox = cv2.approxPolyDP(contornos[0], 0.04 * perimetro, True) #aproxima el contorno
    if len(contorno_aprox) == 3: #si es un triangulo tendra 3 vertices
        return 'triangulo'
    elif len(contorno_aprox) == 4: #si es un cuadrado o un rectangulo 4 vertices
        shape_name = ''
        #el aspect ratio de la figura
        (x, y, w, h) = cv2.boundingRect(contorno_aprox)
        aspect_ratio = float(w)/h
        #si el aspect ratio es 1 significa que la figura es un cuadrado
        fig_name = 'cuadrado' if aspect_ratio == 1 else 'rectangulo'
        return fig_name

    else: #de otra forma se asumira que la figura es un circulo
        return 'circulo'

