"""
Algoritmos de reamostragem de imagens.

Responsável por:
- vizinho mais próximo
- bilinear
"""

import numpy as np
"""
Algoritmos de reamostragem de imagens.

Responsável por:
- vizinho mais próximo
- bilinear
"""

import numpy as np

def redimensionar_vizinho_mais_proximo(imagem, nova_largura, nova_altura):
    
    """
    Redimensiona uma imagem usando o método do vizinho mais próximo
    de forma vetorizada com NumPy (sem loops de pixels).

    Args:
        imagem (numpy.ndarray): Imagem de entrada.
        nova_largura (int): Nova largura da imagem.
        nova_altura (int): Nova altura da imagem.

    Returns:
        numpy.ndarray: Imagem redimensionada.
    """

    # obtém as dimensões da imagem original
    altura_original, largura_original = imagem.shape[:2]

    # calcula fatores de escala (mesma lógica da versão com loops) 
    # imag_original / nova_imagem
    escala_x = largura_original / nova_largura
    escala_y = altura_original / nova_altura

    # cria os índices do grid de destino
    # arange: gera um array de 0 até nova_largura-1 (mesma lógica da versão com loops)
    x = np.arange(nova_largura)
    y = np.arange(nova_altura)

    # cria a malha de coordenadas (cada posição do destino)
    xx, yy = np.meshgrid(x, y)

    # mapeia cada posição do destino para a posição na imagem original
    # broadcasting: xx e yy (matrizes) são multiplicados por escala (escalares)
    x_idx = (xx * escala_x).astype(np.int32)
    y_idx = (yy * escala_y).astype(np.int32)

    # garante que os índices estejam dentro dos limites
    x_idx = np.clip(x_idx, 0, largura_original - 1)
    y_idx = np.clip(y_idx, 0, altura_original - 1)

    # indexação vetorizada: obtém todos os pixels de uma vez
    if len(imagem.shape) == 3:
        imagem_redimensionada = imagem[y_idx, x_idx, :]
    else:
        imagem_redimensionada = imagem[y_idx, x_idx]

    return imagem_redimensionada.astype(np.uint8)

def redimensionar_bilinear(imagem, nova_largura, nova_altura):
    """
    Redimensiona uma imagem utilizando
    interpolação bilinear vetorizada.

    Utiliza:
    - meshgrid
    - broadcasting
    - indexação avançada NumPy
    """

    # obtém as dimensões da imagem original
    altura_original, largura_original = imagem.shape[:2]

    # coordenadas do grid de destino
    x = np.arange(nova_largura)
    y = np.arange(nova_altura)

    # cria a malha de coordenadas (cada posição do destino)
    xx, yy = np.meshgrid(x, y)

    # mapeia para coordenadas da imagem original
    escala_x = xx * ((largura_original - 1) / max(nova_largura - 1,1))
    escala_y = yy * ((altura_original - 1) / max(nova_altura - 1,1))

    # coordenadas dos 4 pixels vizinhos
    x1 = np.floor(escala_x).astype(np.int32)
    y1 = np.floor(escala_y).astype(np.int32)

    x2 = np.clip(x1 + 1, 0, largura_original - 1)
    y2 = np.clip(y1 + 1, 0, altura_original - 1)

    # Distâncias fracionárias
    dx = escala_x - x1
    dy = escala_y - y1

    # Para imagens coloridas, precisamos manter a dimensão dos canais
    if len(imagem.shape) == 3:

        dx = dx[..., None]  # (H,W,1)
        dy = dy[..., None]  # (H,W,1)

        # Obtém os 4 pixels vizinhos de forma vetorizada
        p11 = imagem[y1, x1]  # (H,W,C)
        p12 = imagem[y1, x2]  # (H,W,C) 
        p21 = imagem[y2, x1]  # (H,W,C)
        p22 = imagem[y2, x2]  # (H,W,C)

    else:

        # Imagem em escala de cinza
        p11 = imagem[y1, x1]  # (H,W)
        p12 = imagem[y1, x2]  # (H,W)
        p21 = imagem[y2, x1]  # (H,W)
        p22 = imagem[y2, x2]  # (H,W)
    
    # Interpolação bilinear
    imagem_interpolada = (p11 * (1 - dx) * (1 - dy) +
                            p12 * dx * (1 - dy) +
                            p21 * (1 - dx) * dy +
                            p22 * dx * dy)
    
    # Limita os valores entre 0 e 255
    imagem_interpolada = np.clip(imagem_interpolada, 0, 255)
    return imagem_interpolada.astype(np.uint8)