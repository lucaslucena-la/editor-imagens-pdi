"""
Algoritmos de convolução espacial e filtros.

Este módulo implementa filtros baseados em kernels
utilizando convolução vetorizada com NumPy.

Responsável por:
- convolução genérica
- filtros de suavização
- filtros de detecção de bordas

Técnicas utilizadas:
- Convolução espacial
- Broadcasting
- Sliding Window View
- Padding configurável
"""

import numpy as np
import time
from numpy.lib.stride_tricks import sliding_window_view

# Função genéria de convolução
def aplicar_convolucao(imagem, kernel, clip=True, padding = 'edge'):
    """
    Aplica convolução espacial utilizando
    o kernel informado.

    Implementação vetorizada utilizando:
    - sliding_window_view
    - broadcasting
    - NumPy
    """

    # Obtém as dimensões do kernel
    altura_kernel, largura_kernel = kernel.shape

    # centro do kernel
    margem_x = largura_kernel // 2
    margem_y = altura_kernel // 2

    # Verifica se imagem é colorida
    imagem_colorida = len(imagem.shape) == 3

    # converte para float para evitar overflow
    imagem_float = imagem.astype(np.float32)

    # aplica padding nas bordas
    if imagem_colorida:
        imagem_padded = np.pad(imagem_float, ((margem_y, margem_y), (margem_x, margem_x), (0, 0)), mode=padding)

        # cria janelas 
        janelas = sliding_window_view(imagem_padded, (altura_kernel, largura_kernel), axis = (0,1))

        # Broadcasting:
        # (H,W,C,kH,kW)
        # (1,1,1,kH,kW)
        # posição y, posição x, canal, linha do kernel, coluna do kernel
        resultado = np.sum(janelas * kernel[None, None, None, :, :], axis=(3, 4))
    
    else: # imagem em escala de cinza
        imagem_padded = np.pad(imagem_float, ((margem_y, margem_y), (margem_x, margem_x)), mode=padding)
        
        # cria janelas
        janelas = sliding_window_view(imagem_padded, (altura_kernel, largura_kernel), axis = (0,1))
        
        # Broadcasting:
        # (H,W,kH,kW)
        # (1,1,kH,kW)
        resultado = np.sum(janelas * kernel[None, None, :, :], axis=(2, 3))

    #limita os valores entre 0 e 255
    if clip:
        resultado = np.clip(resultado, 0, 255) # Garante que os valores estejam no intervalo válido para imagens
        return resultado.astype(np.uint8) # Converte de volta para uint8
    return resultado

# ============================================================================ #
# FILTROS DE DETECÇÃO DE BORDAS - SOBEL
# ============================================================================ #
def kernel_sobel_x():
    """
    Retorna kernel Sobel X.
    """
    return np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ],
        dtype=np.float32
    )

def kernel_sobel_y():
    """
    Retorna kernel Sobel Y.
    """
    return np.array(
        [
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ],
        dtype=np.float32
    )

def aplicar_sobel(imagem, padding = 'edge'):
    """
    Aplica filtro Sobel.
    """
    inicio = time.perf_counter()
    
    # Aplica os kernels de Sobel para obter os gradientes nas direções X e Y
    kernel_x = kernel_sobel_x()
    kernel_y = kernel_sobel_y()

    # Aplica convolução para obter os gradientes em X e Y
    gradiente_x = aplicar_convolucao(imagem, kernel_x, clip=False, padding=padding)
    gradiente_y = aplicar_convolucao(imagem, kernel_y, clip=False, padding=padding)

    # Calcula a magnitude do gradiente
    resultado = np.sqrt(gradiente_x**2 + gradiente_y**2)

    fim = time.perf_counter()

    print(
        f"Tempo Sobel: "
        f"{fim - inicio:.3f} segundos"
    )

    # Limita os valores entre 0 e 255 e converte para uint8
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    return resultado

# ============================================================================ #
# FILTROS DE DETECÇÃO DE BORDAS - LAPLACIANO
# ============================================================================ #

def kernel_laplaciano():
    """
    Retorna kernel Laplaciano.

    Destaca regiões onde ocorre
    mudança brusca de intensidade.

    """
    return np.array(
        [
            [0,  1, 0],
            [1, -4, 1],
            [0,  1, 0]
        ],
        dtype=np.float32
    )

def aplicar_laplaciano(imagem, padding = 'edge'):
    """
    Aplica filtro Laplaciano.
    """
    inicio = time.perf_counter()

    kernel = kernel_laplaciano()
    resultado = aplicar_convolucao(imagem, kernel, clip=False, padding=padding)

    # O resultado do Laplaciano pode conter valores negativos, então pegamos o valor absoluto
    resultado = np.abs(resultado) 
   
    fim = time.perf_counter()

    print(
        f"Tempo Laplaciano: "
        f"{fim - inicio:.3f} segundos"
    )

    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    return resultado

# ============================================================================ #
# FILTROS DE SUAVIZAÇÃO - BOX FILTER
# ============================================================================ #

def gerar_kernel_box(tamanho_kernel):
    """
    Gera um kernel Box NxN normalizado.

    Args:
        tamanho_kernel (int): Tamanho ímpar do kernel.

    Returns:
        numpy.ndarray: Kernel Box normalizado.
    """

    # O kernel Box deve ter tamanho ímpar para possuir centro definido
    if tamanho_kernel % 2 == 0:
        raise ValueError("O tamanho do kernel Box deve ser ímpar.")

    # Cria uma matriz de 1s e normaliza pela quantidade total de elementos
    return (
        np.ones((tamanho_kernel, tamanho_kernel), dtype=np.float32)
        / (tamanho_kernel * tamanho_kernel)
    )

def aplicar_box(imagem, tamanho_kernel=3, padding='edge'):
    """
    Aplica filtro Box com tamanho de kernel parametrizado.

    Args:
        imagem (numpy.ndarray): Imagem de entrada.
        tamanho_kernel (int): Tamanho ímpar do kernel Box.
        padding (str): Tipo de padding aplicado nas bordas.

    Returns:
        numpy.ndarray: Imagem filtrada.
    """

    inicio = time.perf_counter()

    # Gera o kernel Box normalizado de acordo com o tamanho informado
    kernel = gerar_kernel_box(tamanho_kernel)

    # Aplica a convolução utilizando o kernel construído dinamicamente
    resultado = aplicar_convolucao(imagem, kernel, padding=padding)

    fim = time.perf_counter()

    print(
        f"Tempo Box {tamanho_kernel}x{tamanho_kernel}: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

# ============================================================================ #
# FILTROS DE SUAVIZAÇÃO - GAUSSIANO
# ============================================================================ #
def gerar_kernel_gaussiano(tamanho, sigma):
    """
    Gera um kernel gaussiano NxN.

    Args:
        tamanho (int): tamanho do kernel.
        sigma (float): desvio padrão da gaussiana.

    Returns:
        numpy.ndarray
    """

    # Kernel deve ser ímpar
    if tamanho % 2 == 0:raise ValueError("O tamanho do kernel deve ser ímpar.")

    # Coordenadas centradas em zero
    eixo = np.arange(-(tamanho // 2),(tamanho // 2) + 1)

    x, y = np.meshgrid(eixo, eixo)

    # Fórmula da Gaussiana 2D
    kernel = np.exp(-(x**2 + y**2)/(2 * sigma**2))

    # Normalização
    kernel = kernel / np.sum(kernel)

    return kernel.astype(np.float32)

def aplicar_gaussiano(imagem,tamanho,sigma,padding="edge"):
    """
    Aplica filtro gaussiano
    parametrizado.
    """

    inicio = time.perf_counter()

    kernel = gerar_kernel_gaussiano(tamanho,sigma)

    resultado = aplicar_convolucao(imagem,kernel,padding=padding)

    fim = time.perf_counter()

    print(
        f"Tempo Gaussiano Personalizado: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

# ============================================================================ #
# FILTROS NÃO LINEARES
# ============================================================================ #
def aplicar_mediana(imagem, tamanho_kernel=3, padding='edge'):
    """
    Aplica filtro de mediana com tamanho de kernel parametrizado.

    Utiliza:
    - sliding_window_view
    - vetorização com NumPy
    - indexação avançada NumPy

    Args:
        imagem (numpy.ndarray): Imagem de entrada.
        tamanho_kernel (int): Tamanho ímpar do kernel de mediana.
        padding (str): Tipo de padding aplicado nas bordas.

    Returns:
        numpy.ndarray: Imagem filtrada.
    """

    inicio = time.perf_counter()

    # O filtro da mediana exige janela ímpar para ter pixel central
    if tamanho_kernel % 2 == 0:
        raise ValueError("O tamanho do kernel da mediana deve ser ímpar.")

    # Calcula a margem necessária com base no tamanho do kernel
    margem = tamanho_kernel // 2

    # Verifica se a imagem é colorida
    if len(imagem.shape) == 3:

        # Imagem colorida: aplica padding apenas nos eixos espaciais,
        # preservando os canais da imagem
        imagem_padded = np.pad(imagem, ((margem, margem), (margem, margem), (0, 0)), mode=padding)

        # Cria janelas deslizantes de tamanho NxN para cada pixel.
        # Saída esperada: (H, W, C, k, k)
        janelas = sliding_window_view(imagem_padded, (tamanho_kernel, tamanho_kernel), axis=(0, 1))

        # Calcula a mediana dentro de cada janela para cada canal
        resultado = np.median(janelas, axis=(3, 4))
    else:
        # Imagem em escala de cinza: padding apenas nos dois eixos
        imagem_padded = np.pad(imagem, ((margem, margem), (margem, margem)), mode=padding)

        # Cria janelas deslizantes de tamanho NxN.
        # Saída esperada: (H, W, k, k)
        janelas = sliding_window_view(imagem_padded, (tamanho_kernel, tamanho_kernel), axis=(0, 1))

        # Calcula a mediana dentro de cada janela
        resultado = np.median(janelas, axis=(2, 3))

    # Garante o intervalo válido de imagem e converte para uint8
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    fim = time.perf_counter()

    print(
        f"Tempo Mediana {tamanho_kernel}x{tamanho_kernel}: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

# ============================================================================ #
# FILTROS DE AGUÇAMENTO
# ============================================================================ #

def aplicar_agucamento_laplaciano(imagem,tamanho_kernel=5,sigma=1.0,padding="edge"):
    """
    Aplica aguçamento utilizando o método Laplaciano .

    Procedimento:

    1. Suaviza a imagem utilizando filtro gaussiano.
    2. Calcula a Laplaciana da imagem suavizada.
    3. Soma a Laplaciana à imagem original.

    Fórmula:

        g(x,y) = f(x,y) + c * Laplaciano

    Como o kernel utilizado possui centro negativo,
    utiliza-se c = -1.

    Args:
        imagem (numpy.ndarray):
            Imagem de entrada.

        tamanho_kernel (int):
            Tamanho do kernel gaussiano.

        sigma (float):
            Desvio padrão da gaussiana.

        padding (str):
            Tipo de padding.

    Returns:
        numpy.ndarray:
            Imagem aguçada.
    """

    inicio = time.perf_counter()

    # -----------------------------------------------------------------
    # ETAPA 1
    # SUAVIZAÇÃO GAUSSIANA
    # -----------------------------------------------------------------

    imagem_suavizada = aplicar_gaussiano(
        imagem,
        tamanho=tamanho_kernel,
        sigma=sigma,
        padding=padding
    )

    # -----------------------------------------------------------------
    # ETAPA 2
    # CÁLCULO DA LAPLACIANA
    # -----------------------------------------------------------------

    kernel = kernel_laplaciano()

    laplaciano = aplicar_convolucao(
        imagem_suavizada,
        kernel,
        clip=False,
        padding=padding
    )

    # -----------------------------------------------------------------
    # ETAPA 3
    # AGUÇAMENTO
    #
    # Como utilizamos o kernel:
    #
    # [ 0  1  0 ]
    # [ 1 -4  1 ]
    # [ 0  1  0 ]
    #
    # o coeficiente c = -1.
    #
    # g = f - laplaciano
    # -----------------------------------------------------------------

    imagem_float = imagem.astype(np.float32)

    resultado = (
        imagem_float
        - laplaciano
    )

    # -----------------------------------------------------------------
    # AJUSTE FINAL
    # -----------------------------------------------------------------

    resultado = np.clip(resultado,0,255
    )

    fim = time.perf_counter()

    print(
        f"Tempo Aguçamento Laplaciano: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado.astype(np.uint8)