"""
Gerenciador central de imagens.

Responsável por:
- carregar imagens
- armazenar imagem original
- armazenar imagem atual
"""

import cv2

class GerenciadorImagens:
    """
    Classe responsável por gerenciar as imagens da aplicação.
    """

    def __init__(self):

        # imagem original carregada
        self.imagem_original = None

        # imagem atualmente modificada
        self.imagem_atual = None

    def carregar_imagem(self, caminho):
        """
        Carrega uma imagem utilizando OpenCV.

        Args:
            caminho (str): Caminho para a imagem a ser carregada.
        """

        # OpenCV lê imagem em formato BGR
        imagem = cv2.imread(caminho)

        # Salva a cópia da imasgem original
        self.imagem_original = imagem.copy()

        # Define a imagem atual como a original
        self.imagem_atual = self.imagem_original.copy()