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

def expansao_contraste(imagem):
    """
    Aplica expansão linear de contraste.

    Mapeia:
        rmin -> 0
        rmax -> 255

    Expandindo toda a faixa dinâmica
    da imagem.
    """

    # Converte para float32
    imagem_float = imagem.astype(np.float32)

    # Obtém intensidade mínima e máxima
    rmin = np.min(imagem_float)
    rmax = np.max(imagem_float)

    # Evita divisão por zero
    if rmax == rmin:
        return imagem.copy()

    # Expansão linear
    imagem_expandida = (
        (imagem_float - rmin)
        * 255.0
        / (rmax - rmin)
    )

    # Limita valores
    imagem_expandida = np.clip(
        imagem_expandida,
        0,
        255
    )

    return imagem_expandida.astype(np.uint8)

def transformacao_logaritmica(imagem):
    """
    Aplica transformação logarítmica.

    Realça regiões escuras da imagem e comprime
    regiões muito claras.
    """

    # Converte a imagem para tipo float32 para evitar overflow
    imagem_float = imagem.astype(np.float32)

    # constante de escala para normalizar os valores dos pixels
    c = 255 / np.log(1 + 255)

    # Aplica a transformação logarítmica
    imagem_logaritmica = c * np.log(1 + imagem_float)

    # Limita os valores dos pixels para o intervalo [0, 255]
    imagem_logaritmica = np.clip(imagem_logaritmica, 0, 255)

    # Converte de volta para uint8
    return imagem_logaritmica.astype(np.uint8)

def transformacao_exponencial(imagem):
    """
    Aplica transformação exponencial.

    Realça regiões claras da imagem e comprime
    regiões escuras.
    """

    # Converte para float32
    imagem_float = imagem.astype(np.float32)

    # Normaliza para [0,1]
    imagem_normalizada = imagem_float / 255.0

    # Aplica transformação exponencial
    imagem_exp = (np.exp(imagem_normalizada) - 1) / (np.e - 1)

    # Retorna para [0,255]
    imagem_exp *= 255.0

    # Limita os valores
    imagem_exp = np.clip(imagem_exp,0,255)

    return imagem_exp.astype(np.uint8)

