"""
Algoritmos de convolução espacial.

Responsável por aplicar kernels em imagens.
"""

import numpy as np
import time
from numpy.lib.stride_tricks import sliding_window_view

def aplicar_convolucao(imagem, kernel, clip=True):
    """
    Aplica convolução espacial utilizando
    o kernel informado.

    Implementação vetorizada utilizando:
    - sliding_window_view
    - broadcasting
    - NumPy
    """
    # Obtém as dimensões da imagem 
    altura, largura = imagem.shape[:2] 

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
        imagem_padded = np.pad(imagem_float, ((margem_y, margem_y), (margem_x, margem_x), (0, 0)), mode='edge')

        # cria janelas 
        janelas = sliding_window_view(imagem_padded, (altura_kernel, largura_kernel), axis = (0,1))

        # Broadcasting:
        # (H,W,C,kH,kW)
        # (1,1,1,kH,kW)
        resultado = np.sum(janelas * kernel[None, None, None, :, :], axis=(3, 4))
    
    else: # imagem em escala de cinza
        imagem_padded = np.pad(imagem_float, ((margem_y, margem_y), (margem_x, margem_x)), mode='edge')
        
        # cria janelas
        janelas = sliding_window_view(imagem_padded, (altura_kernel, largura_kernel), axis = (0,1))
        
        # Broadcasting:
        # (H,W,kH,kW)
        # (1,1,kH,kW)
        resultado = np.sum(janelas * kernel[None, None, :, :], axis=(2, 3))

    #limita os valores entre 0 e 255
    if clip:
        resultado = np.clip(resultado, 0, 255)
        return resultado.astype(np.uint8)
    return resultado

def kernel_box_3x3():
    """
    Retorna kernel Box 3x3.
    """

    return np.ones((3, 3),dtype=np.float32) / 9.0

def aplicar_box_3x3(imagem):
    """
    Aplica filtro Box 3x3.
    """
    inicio = time.time()

    kernel = kernel_box_3x3()
    resultado = aplicar_convolucao(imagem, kernel)


    fim = time.time()

    print(f"Tempo Box 3x3: "f"{fim - inicio:.2f} segundos")

    return resultado

def kernel_box_5x5():
    """
    Retorna kernel Box 5x5.
    """

    return np.ones((5, 5), dtype=np.float32) / 25.0

def aplicar_box_5x5(imagem):

    """
    Aplica filtro Box 5x5.
    """

    inicio = time.perf_counter()

    kernel = kernel_box_5x5()

    resultado = aplicar_convolucao(imagem, kernel)

    fim = time.perf_counter()

    print(
        f"Tempo Box 5x5: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

def kernel_gaussiano_3x3():
    """
    Retorna kernel Gaussiano 3x3.
    """

    return np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]], dtype=np.float32) / 16.0

def aplicar_gaussiano_3x3(imagem):
    """
    Aplica filtro Gaussiano 3x3.
    """

    inicio = time.perf_counter()

    kernel = kernel_gaussiano_3x3()

    resultado = aplicar_convolucao(imagem, kernel)

    fim = time.perf_counter()

    print(
        f"Tempo Gaussiano 3x3: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

def kernel_gaussiano_5x5():
    """
    Retorna kernel Gaussiano 5x5.
    """
    return np.array(
        [
            [1,  4,  6,  4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1,  4,  6,  4, 1],
        ],
        dtype=np.float32
    ) / 256.0

def aplicar_gaussiano_5x5(imagem):
    """
    Aplica filtro Gaussiano 5x5.
    """
    inicio = time.perf_counter()

    kernel = kernel_gaussiano_5x5()
    resultado = aplicar_convolucao(imagem, kernel)

    fim = time.perf_counter()

    print(
        f"Tempo Gaussiano 5x5: "
        f"{fim - inicio:.3f} segundos"
    )

    return resultado

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

def aplicar_sobel(imagem):
    """
    Aplica filtro Sobel.
    """
    inicio = time.perf_counter()

    kernel_x = kernel_sobel_x()
    kernel_y = kernel_sobel_y()

    gradiente_x = aplicar_convolucao(imagem, kernel_x, clip=False)
    gradiente_y = aplicar_convolucao(imagem, kernel_y, clip=False)

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

def aplicar_laplaciano(imagem):
    """
    Aplica filtro Laplaciano.
    """
    inicio = time.perf_counter()

    kernel = kernel_laplaciano()
    resultado = aplicar_convolucao(imagem, kernel, clip=False)

    # O resultado do Laplaciano pode conter valores negativos, então pegamos o valor absoluto
    resultado = np.abs(resultado)
   
    fim = time.perf_counter()

    print(
        f"Tempo Laplaciano: "
        f"{fim - inicio:.3f} segundos"
    )

    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    return resultado







