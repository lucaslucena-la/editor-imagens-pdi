"""
Funções auxiliares de conversão.

Responsável por converter imagens
entre OpenCV e PyQt.
"""

import cv2
from PyQt5.QtGui import QImage, QPixmap

def cv2_to_qt(cv_img):
    """
    Converte uma imagem OpenCV (BGR)
    para QPixmap do PyQt.
    """
    # Converte de BGR para RGB
    imagem_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

    # Obtém as dimensões da imagem
    altura, largura, canais = imagem_rgb.shape

    # Quantidade de bytes por linha
    bytes_por_linha = canais * largura

    # Cria um QImage a partir dos dados da imagem
    qt_img = QImage(imagem_rgb.data, largura, altura, bytes_por_linha, QImage.Format_RGB888)

    # Converte o QImage para QPixmap
    qt_pixmap = QPixmap.fromImage(qt_img)

    return qt_pixmap
    