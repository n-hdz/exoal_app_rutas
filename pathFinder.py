from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import math

class ImageCroper(object):

    def __init__(self, img_src):
        self.img_src = img_src
        
    def crop(self):
        file = Image.open(self.img_src)
        width, height = file.size
        # Descomponer archivo de imagen en Matriz bidimensional
        pixels = list(file.getdata())
        Matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
        x_plane = []
        y_plane = []
        perimeter = [(230, 184, 151),
                     (233, 99, 64),
                     (233, 86, 74),
                     (236, 78, 60),
                     (236, 78, 61),
                     (237, 91, 79),
                     (234, 67, 53),
                     (245, 155, 114),
                     (242, 137, 129),
                     (242, 139, 130),
                     (244, 157, 150),
                     (235, 97, 74),
                     (235, 80, 67),
                     (235, 107, 81),
                     (235, 110, 100),
                     (236, 153, 146),
                     (241, 174, 168),
                     (240, 114, 104),
                     (240, 117, 107),
                     (240, 111, 84),
                     (240, 120, 110),
                     (240, 124, 115),
                     (247, 185, 180),
                     (249, 205, 202)]
        # Caminata matricial de vision m�quina para discriminar bordes
        for h in range(height):
           for w in range(width):
               # Si la caminata encuentra informaci�n de vialidad asociada a colonia
               if Matrix[h][w] in perimeter:
                   y_plane.append(h)
                   x_plane.append(w)

        left = min(x_plane)
        top = min(y_plane)
        right = max(x_plane) + 3
        lower = max(y_plane) + 2

        crop = file.crop((left, top, right, lower))
        return crop

class PixelReader(object):

    def __init__(self, img_src, marker_one, marker_two):
        self.img_src = img_src
        self.marker_one = marker_one
        self.marker_two = marker_two

    def read(self):
        # Conversion de data de formulario en variables de programa
        file = Image.open(self.img_src)
        marker_one_arr = self.marker_one.split(',')
        marker_two_arr = self.marker_two.split(',')

        for i in range(0, 3):
            marker_one_arr[i] = int(marker_one_arr[i])
            marker_two_arr[i] = int(marker_two_arr[i])

        marker_one = tuple(marker_one_arr)
        marker_two = tuple(marker_two_arr)

        width, height = file.size
        # Descomponer archivo de imagen en Matriz bidimensional
        pixels = list(file.getdata())
        Matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
        new_image = []
        match = [(255, 255, 255), (252, 252, 252)]
        ui = [
                (66, 133, 244),
                (77, 181, 70),
                (16, 189, 255),
                (239, 116, 182),
                (75, 150, 243), 
                (123, 158, 176), 
                (116, 149, 166), 
                (109, 156, 214), 
                (142, 187, 247),
                (149, 193, 248),
                (170, 173, 175),
                (191, 219, 251),
                (162, 187, 195),
                (207, 219, 233),
                (251, 251, 215),
                (224, 243, 224),
                (222, 222, 222),
                (222, 222, 223),
                (240, 125, 186),
                (241, 149, 198),
                (242, 180, 213),
                (243, 197, 222),
                (255, 158, 103),
                (217, 146, 110)
            ]
        match_marker = (0, 255, 0)
        weight_count = 0
        sqr_mts = 0
        # Caminata matricial de vision m�quina para discriminar bordes
        for h in range(height):
           for w in range(width):
               # Si la caminata encuentra informaci�n de vialidad asociada a colonia
               if Matrix[h][w] in match:
                   # Discrimina Indicadores de Interfaz de usuario Tolerancia 2
                   if not (
                           # Este - Oeste
                           Matrix[h][w - 1] in ui or Matrix[h][w + 1] in ui or
                           # Norte - Sur
                           Matrix[h - 1][w] in ui or Matrix[h][w] in ui or
                           # Noreste - Noroeste
                           Matrix[h - 1][w - 1] in ui or Matrix[h][w + 1] in ui or 
                           # Sureste - Suroeste
                           Matrix[h][w - 1] in ui or Matrix[h - 1][w + 1] in ui or
                           # Este - Oeste
                           Matrix[h][w - 2] in ui or Matrix[h][w + 2] in ui or
                           # Norte - Sur
                           Matrix[h - 2][w] in ui or Matrix[h + 2][w] in ui or
                           # Noreste - Noroeste
                           Matrix[h - 2][w - 2] in ui or Matrix[h + 2][w + 2] in ui or 
                           # Sureste - Suroeste
                           Matrix[h + 2][w - 2] in ui or Matrix[h - 2][w + 2] in ui
                      ):
                       new_image.append(match_marker)
                       sqr_mts += 1
                   else:
                       new_image.append(Matrix[h][w])
               else:
                   new_image.append(Matrix[h][w])

        # Crear mapa indicando rutas
        im = Image.new("RGB", (width, height))
        im.putdata(new_image)
        im.save('C:\\Users\\neftali.hernandez\\Documents\\exoal_app_rutas\\static\\maps\\temp.png')

        pixels = list(im.getdata())
        Matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
        new_image = []
        marked_mts = 0
        # Caminata matricial de vision m�quina para discriminar bordes
        for h in range(height):
           for w in range(width):
               # Si la caminata encuentra informaci�n de vialidad asociada a colonia
               if Matrix[h][w] == match_marker:                   
                    if marked_mts >= math.floor(sqr_mts / 2):
                        new_image.append(marker_one)
                    else:
                        marked_mts += 1
                        new_image.append(marker_two)
               else:
                   new_image.append(Matrix[h][w])
        mapped = Image.new("RGB", (width, height))
        mapped.putdata(new_image)

        return mapped