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

def ajustar_brilho(imagem, valor):
    """
    Ajusta o brilho de uma imagem.

    Args:
        imagem (numpy.ndarray): Imagem de entrada.
        valor (int): Valor a ser adicionado aos pixels para ajustar o brilho. Pode ser positivo ou negativo.

    Returns:
        numpy.ndarray: Imagem com brilho ajustado.
    """

    # Converte a imagem para tipo int16 para evitar overflow
    imagem_int = imagem.astype(np.int32)

    # Adiciona o valor de brilho aos pixels
    imagem_brilho = imagem_int + valor

    # Limita os valores dos pixels para o intervalo [0, 255]
    imagem_brilho = np.clip(imagem_brilho, 0, 255)

    # Converte de volta para uint8
    return imagem_brilho.astype(np.uint8)

def ajustar_contraste(imagem, fator):
    """
    Ajusta o contraste da imagem.

    fator > 1  -> aumenta contraste
    0 < fator < 1 -> reduz contraste
    """
    # Converte a imagem para tipo float32 para evitar overflow
    imagem_float = imagem.astype(np.float32)

    # Calcula o valor médio dos pixels para cada canal (R, G, B)
    media = np.mean(imagem_float, axis=(0, 1), keepdims=True)

    # Ajusta o contraste usando a fórmula: pixel_contraste = (pixel - media) * fator + media
    imagem_contraste = (imagem_float - media) * fator + media

    # Limita os valores dos pixels para o intervalo [0, 255]
    imagem_contraste = np.clip(imagem_contraste, 0, 255)

    # Converte de volta para uint8
    return imagem_contraste.astype(np.uint8)