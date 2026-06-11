"""
Algoritmos de histograma.

Responsável por:
- cálculo de histograma
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================ #
# HISTOGRAMA
# ============================================================================ #

def calcular_histograma(imagem):
    """
    Calcula o histograma de uma imagem.

    O histograma representa a frequência
    de ocorrência de cada nível de intensidade.

    Para imagens em escala de cinza:
        retorna um vetor de 256 posições.

    Para imagens coloridas:
        retorna um histograma para cada canal.

    Args:
        imagem (numpy.ndarray):
            Imagem de entrada.

    Returns:
        numpy.ndarray ou tuple:
            Histograma calculado.
    """

    # Imagem colorida (3 canais)
    if len(imagem.shape) == 3: 
        
        # Canal azul
        hist_b = np.bincount(imagem[..., 0].ravel(), minlength=256)
        
        # Canal verde
        hist_g = np.bincount(imagem[..., 1].ravel(), minlength=256)
        
        # Canal vermelho
        hist_r = np.bincount(imagem[..., 2].ravel(), minlength=256)

        return hist_r, hist_g, hist_b
    
    else:  # Imagem em escala de cinza
        hist = np.bincount(imagem.ravel(), minlength=256)
        return hist

def mostrar_histograma(imagem):
    """
    Exibe o histograma da imagem.

    Para imagens coloridas:
        exibe os histogramas dos canais
        Azul, Verde e Vermelho.

    Para imagens em escala de cinza:
        exibe um único histograma.

    Args:
        imagem (numpy.ndarray):
            Imagem de entrada.
    """

    # IMAGEM COLORIDA
    if len(imagem.shape) == 3:

        hist_b, hist_g, hist_r = (calcular_histograma(imagem))

        plt.figure(figsize=(8, 5))
        plt.plot(hist_b, label="Azul")
        plt.plot(hist_g, label="Verde")
        plt.plot(hist_r, label="Vermelho")
        plt.title("Histograma RGB")
        plt.xlabel("Intensidade")
        plt.ylabel("Quantidade de Pixels")
        plt.xlim([0, 255])
        plt.legend()
        plt.grid(True)
        plt.show()

    # ESCALA DE CINZA

    else:

        histograma = calcular_histograma(imagem)
        plt.figure(figsize=(8, 5))
        plt.plot(histograma)
        plt.title("Histograma")
        plt.xlabel("Intensidade")
        plt.ylabel("Quantidade de Pixels")
        plt.xlim([0, 255])
        plt.grid(True)
        plt.show()

# ============================================================================ #
# EQUALIZAÇÃO DE HISTOGRAMA
# ============================================================================ #

def equalizar_histograma(imagem):
    """
    Aplica equalização de histograma.

    Redistribui os níveis de intensidade
    para ocupar melhor toda a faixa dinâmica
    entre 0 e 255.

    Args:
        imagem (numpy.ndarray):
            Imagem de entrada.

    Returns:
        numpy.ndarray:
            Imagem equalizada.
    """

    # ---------------------------------------------------------------------
    # IMAGEM COLORIDA
    # ---------------------------------------------------------------------

    if len(imagem.shape) == 3:

        imagem_equalizada = imagem.copy()

        # Equaliza cada canal separadamente
        for canal in range(3):

            histograma = np.bincount(imagem[:, :, canal].ravel(),minlength=256)

            cdf = histograma.cumsum()

            cdf_normalizada = ((cdf - cdf.min())* 255/ (cdf.max() - cdf.min()))

            tabela = np.clip(cdf_normalizada,0,255).astype(np.uint8)

            imagem_equalizada[:, :, canal] = (tabela[imagem[:, :, canal]])

        return imagem_equalizada

    # ---------------------------------------------------------------------
    # ESCALA DE CINZA
    # ---------------------------------------------------------------------

    histograma = np.bincount(imagem.ravel(),minlength=256
    )

    # Função distribuição acumulada
    cdf = histograma.cumsum()

    # Normalização para faixa 0-255
    cdf_normalizada = ((cdf - cdf.min())* 255/ (cdf.max() - cdf.min()))

    tabela = np.clip(cdf_normalizada,0,255).astype(np.uint8)

    imagem_equalizada = tabela[imagem]

    return imagem_equalizada