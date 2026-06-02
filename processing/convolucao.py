"""
Algoritmos de convolução espacial.

Responsável por aplicar kernels em imagens.
"""

import numpy as np
import time

def aplicar_convolucao(imagem, kernel):
    """
    Aplica convolução espacial utilizando
    o kernel informado.
    """

    # Obtém as dimensões da imagem 
    altura, largura = imagem.shape[:2] 

    # Verifica se imagem é colorida
    imagem_colorida = len(imagem.shape) == 3

    # Obtém as dimensões do kernel
    altura_kernel, largura_kernel = kernel.shape

    # centro do kernel
    margem_x = largura_kernel // 2
    margem_y = altura_kernel // 2

    # Cria imagem de saída preenchida com zeros
    imagem_saida = np.zeros_like(imagem)

    # percorre imagem ignorando bordas
    for y in range(margem_y, altura - margem_y):
        for x in range(margem_x,largura - margem_x):

            # Processa cada canal separadamente
            if imagem_colorida:
                for canal in range(imagem.shape[2]):
                    soma = 0.0
                    # Percorre kernel
                    for ky in range(altura_kernel):
                        for kx in range(largura_kernel):
                            # Coordenada correspondente
                            pixel_y = (y + ky - margem_y)
                            pixel_x = (x + kx - margem_x)
                            soma += (imagem[pixel_y,pixel_x,canal]*kernel[ky, kx])

                    imagem_saida[y,x,canal] = np.clip(soma,0,255)

    return imagem_saida.astype(np.uint8)

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