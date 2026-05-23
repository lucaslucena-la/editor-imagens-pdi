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

    def salvar_imagem(self, caminho):
        """
        Salva a imagem atual no disco.
        """

        # Verifica se existe imagem carregada
        if self.imagem_atual is not None:

            # Salva imagem utilizando OpenCV
            cv2.imwrite(caminho, self.imagem_atual)

    def resetar_imagem(self):
        """
        Restaura a imagem atual para a imagem original.
        """

        # Verifica se existe imagem original carregada
        if self.imagem_original is not None:

            # Restaura a imagem atual para a original
            self.imagem_atual = self.imagem_original.copy()