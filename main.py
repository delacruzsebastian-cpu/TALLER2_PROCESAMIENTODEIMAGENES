from imageShape import *

if __name__ == '__main__':
    height_image = int(input('ingrese el alto de la imagen: '))  # se ingresa el alto de la imagen
    width_image = int(input('ingrese el ancho de la imagen: '))  # se ingresa el ancho de la imagen
    image = imageShape(height_image, width_image)  # se llama la clase
    image.generateshape()  # se llama el metodo para generar la imagen con la figura
    image.showShape()  # se llama el metodo para mostrar la imagen por 5 segundos
    generated_image, image_class = image.getShape()
    clasificacion = image.whatShape(generated_image)  # resultado del metodo de clasificación
    print(f'La figura se clasificó en: {clasificacion}')
    print('clasificacion realizada existosa') if clasificacion == image_class else print('clasificacion realizada fallida')