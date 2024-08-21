# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10pxarwTT2WgGYw4wDe8qitzYuOLi52du
"""

!pip install opencv-python==4.6.0
!sudo apt install tesseract-ocr
!pip install pytesseract==0.3.9

! git clone https://github.com/sthemonica/text-recognize

import pytesseract
import numpy as np
import cv2
import re
import os
import matplotlib.pyplot as plt

from PIL import Image, ImageFont, ImageDraw
from pytesseract import Output
from google.colab.patches import cv2_imshow

!mkdir tessdata

!wget -O ./tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata?raw=true
!wget -O ./tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata?raw=true

project = '/content/text-recognize/Imagens/Projeto'
caminho = [os.path.join(project, f) for f in os.listdir(project)]
print(caminho)

def mostrar(img):
  fig = plt.gcf()
  fig.set_size_inches(20, 10)
  plt.axis("off")
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  plt.show

for imagem in caminho:
  imagem = cv2.imread(imagem)
  mostrar(imagem)

config_tesseract = "--tessdata-dir tessdata"

def OCR_processa(img, config_tesseract):
  text = pytesseract.image_to_string(img, lang='por', config=config_tesseract)
  return text

texto_completo = ''
nome_txt = 'resultados_ocr.txt'

for imagem in caminho:
  img = cv2.imread(imagem)
  nome_imagem = os.path.split(imagem)[-1]
  nome_divisao = '==================\n' + str(nome_imagem)
  texto_completo = texto_completo + nome_divisao + '\n'
  texto = OCR_processa(img, config_tesseract)
  texto_completo = texto_completo + texto

texto_completo

arquivo_txt = open(nome_txt, 'w+')
arquivo_txt.write(texto_completo + '\n')
arquivo_txt.close()

termo_pesquisa = 'learning'

with open (nome_txt) as f:
  ocorrencias = [i.start() for i in re.finditer(termo_pesquisa, f.read())]

ocorrencias

for imagem in caminho:
  img = cv2.imread(imagem)
  nome_imagem = os.path.split(imagem)[-1]
  print('==================\n' + str(nome_imagem))
  texto = OCR_processa(img, config_tesseract)
  ocorrencias = [i.start() for i in re.finditer(termo_pesquisa, texto)]

  print('Número de ocorrências para o termo: {}: {}'.format(termo_pesquisa, len(ocorrencias)))
  print('\n')

fonte_dir = '/content/text-recognize/Imagens/calibri.ttf'

def escreve_texto(texto, x, y, img, fonte_dir, cor=(50, 50, 255), tamanho=16):
  fonte = ImageFont.truetype(fonte_dir, tamanho)
  img_pil = Image.fromarray(img)
  draw = ImageDraw.Draw(img_pil)
  draw.text((x, y-tamanho), texto, font=fonte, fill=cor)

  return img
fonte_dir = '/content/text-recognize/Imagens/calibri.ttf'

min_conf = 30 #@param {type:"slider", min:0, max:100}

def caixa_texto(i, resultado, img, cor=(255,100,0)):
  x = resultado["left"][i]
  y = resultado["top"][i]
  w = resultado["width"][i]
  h = resultado["height"][i]
  cv2.rectangle(img, (x, y), (x + w, y + h), cor, 2)

  return x, y, img

def OCR_processa_imagem(img, termo_pesquisa, config_tesseract, min_conf):
  resultado = pytesseract.image_to_data(img, config=config_tesseract, lang='por', output_type=pytesseract.Output.DICT)
  num_ocorrencias = 0
  for i in range(0, len(resultado['text'])):
    confianca = int(resultado['conf'][i])
    if confianca > min_conf:
      texto = resultado['text'][i]
      if termo_pesquisa in texto:
        x, y, img = caixa_texto(i, resultado, img, (0,0,255))
        img = escreve_texto(texto, x, y, img, fonte_dir, (50,50,255), 14)
        num_ocorrencias += 1

  return img, num_ocorrencias

termo_pesquisa = 'learning'

for i in caminho:
  img = cv2.imread(imagem)
  img_original = img.copy()

  nome_imagem = os.path.split(imagem)[-1]
  print('=====================\n' + str(nome_imagem))
  img, numero_ocorrencias = OCR_processa_imagem(img, termo_pesquisa, config_tesseract, min_conf)
  print('Número de ocorrências para o termo: {}: {}'.format(termo_pesquisa, nome_imagem, numero_ocorrencias))
  print('\n')

mostrar(img)



