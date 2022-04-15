import pytesseract
import cv2
import Tools.tools


# Ler Imagem

def converter(id):
    imagem = cv2.imread(f'img\{id}.jpg')
    print(f'{Tools.tools.time()}-{id} - Imagem Lida!')

    caminho = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = caminho

    texto = pytesseract.image_to_string(imagem, lang="por")
    print(f'{Tools.tools.time()}-{id} - Texto Enviado!')

    return texto
