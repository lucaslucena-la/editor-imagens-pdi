"""
Algoritmos de transformações de intensidade.

Responsável por:
- negativo
- brilho
- contraste
- limiarização
"""

import cv2
import numpy as np

def aplicar_negativo(imagem):
    """
    Aplica o efeito de negativo em uma imagem.

    Args:
        imagem (numpy.ndarray): Imagem de entrada.

    Returns:
        numpy.ndarray: Imagem com efeito de negativo aplicado.

    Fórmula: pixel_negativo = 255 - pixel_original
    """

    # Inverte os valores dos pixels para criar o efeito de negativo
    imagem_negativa = 255 - imagem

    return imagem_negativa