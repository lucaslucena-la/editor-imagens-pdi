"""
Algoritmos de reamostragem de imagens.

Responsável por:
- vizinho mais próximo
- bilinear
"""

import numpy as np

def redimensionar_vizinho_mais_proximo(imagem, nova_largura, nova_altura):
    """
    Redimensiona uma imagem usando o método do vizinho mais próximo.

    Args:
        imagem (numpy.ndarray): Imagem de entrada.
        nova_largura (int): Nova largura da imagem.
        nova_altura (int): Nova altura da imagem.

    Returns:
        numpy.ndarray: Imagem redimensionada.
    """

    # obtém as dimensões da imagem original
    altura_original, largura_original = imagem.shape[:2]

    # Cria uma nova imagem com as dimensões desejadas
    if len(imagem.shape) == 3: # se a imagem for colorida (3 canais)
        imagem_redimensionada = np.zeros((nova_altura, nova_largura, imagem.shape[2]), dtype=np.uint8) # mantém o número de canais da imagem original
    else:
        imagem_redimensionada = np.zeros((nova_altura, nova_largura), dtype=np.uint8) # imagem em escala de cinza (1 canal)

    # Calcula os fatores de escala
    escala_x  = largura_original / nova_largura
    escala_y = altura_original / nova_altura

    # Para cada pixel na nova imagem, calcula o pixel correspondente na imagem original
    for y in range(nova_altura):
        for x in range(nova_largura):
            # Calcula as coordenadas correspondentes na imagem original
            x_original = int(x * escala_x)
            y_original = int(y * escala_y)

            # Garante que as coordenadas estejam dentro dos limites da imagem original
            x_original = min(x_original, largura_original - 1)
            y_original = min(y_original, altura_original - 1)

            # Atribui o valor do pixel correspondente da imagem original à nova imagem
            imagem_redimensionada[y, x] = imagem[y_original, x_original]

    return imagem_redimensionada