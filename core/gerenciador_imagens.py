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

        # offset acumulado de brilho
        self.offset_brilho = 0
        
        # offset acumulado de contraste
        self.offset_contraste = 0

    def carregar_imagem(self, caminho):
        """
        Carrega uma imagem utilizando OpenCV.

        Args:
            caminho (str): Caminho para a imagem a ser carregada.
        """

        # OpenCV lê imagem em formato BGR
        imagem = cv2.imread(caminho)

        if imagem is None:
            raise ValueError("Não foi possível carregar a imagem."
        )
        
        # Salva a cópia da imagem original
        self.imagem_original = imagem.copy()

        # Define a imagem atual como a original
        self.imagem_atual = self.imagem_original.copy()

        # zera ajustes acumulados ao carregar nova imagem
        self.offset_brilho = 0
        self.offset_contraste = 0

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

            # Reseta o offset de brilho acumulado
            self.offset_brilho = 0

            # Reseta o offset de contraste acumulado
            self.offset_contraste = 0

    def obter_imagem_atual(self):
        """
        Retorna a imagem atualmente exibida.
        """

        return self.imagem_atual
