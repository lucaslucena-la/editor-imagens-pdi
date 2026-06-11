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

        # caminho da imagem carregada
        self.caminho_imagem = None

        # histórico de estados para desfazer alterações
        self.historico = []

        # histórico de estados para refazer alterações
        self.historico_refazer = []

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

        # Armazena caminho da imagem ativa
        self.caminho_imagem = caminho

        # Define a imagem atual como a original
        self.imagem_atual = self.imagem_original.copy()

        # Limpa histórico ao carregar nova imagem
        self.historico = []
        self.historico_refazer = []

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

            # Limpa histórico ao resetar a imagem
            self.historico = []
            self.historico_refazer = []

            # Reseta o offset de brilho acumulado
            self.offset_brilho = 0

            # Reseta o offset de contraste acumulado
            self.offset_contraste = 0

    def obter_imagem_atual(self):
        """
        Retorna a imagem atualmente exibida.
        """

        return self.imagem_atual

    def salvar_estado(self):
        """
        Salva o estado atual da imagem
        para permitir desfazer.
        """

        # Verifica se existe imagem carregada
        if self.imagem_atual is None:
            return

        # Armazena imagem e offsets atuais no histórico
        self.historico.append({
            "imagem": self.imagem_atual.copy(),
            "offset_brilho": self.offset_brilho,
            "offset_contraste": self.offset_contraste
        })

        # Nova edição invalida o caminho atual de refazer
        self.historico_refazer = []

    def desfazer(self):
        """
        Restaura o último estado salvo da imagem.
        """

        # Verifica se existe histórico para desfazer
        if not self.historico:
            return False

        # Recupera o estado mais recente da pilha
        estado_anterior = self.historico.pop()

        # Armazena o estado atual para permitir refazer
        self.historico_refazer.append({
            "imagem": self.imagem_atual.copy(),
            "offset_brilho": self.offset_brilho,
            "offset_contraste": self.offset_contraste
        })

        self.imagem_atual = estado_anterior["imagem"].copy()
        self.offset_brilho = estado_anterior["offset_brilho"]
        self.offset_contraste = estado_anterior["offset_contraste"]

        return True

    def refazer(self):
        """
        Restaura o último estado desfeito da imagem.
        """

        # Verifica se existe histórico para refazer
        if not self.historico_refazer:
            return False

        # Guarda o estado atual para permitir novo desfazer
        self.historico.append({
            "imagem": self.imagem_atual.copy(),
            "offset_brilho": self.offset_brilho,
            "offset_contraste": self.offset_contraste
        })

        # Recupera o estado mais recente desfeito
        estado_refeito = self.historico_refazer.pop()

        self.imagem_atual = estado_refeito["imagem"].copy()
        self.offset_brilho = estado_refeito["offset_brilho"]
        self.offset_contraste = estado_refeito["offset_contraste"]

        return True

    def possui_historico(self):
        """
        Informa se existe histórico para desfazer.
        """

        return len(self.historico) > 0

    def possui_refazer(self):
        """
        Informa se existe histórico para refazer.
        """

        return len(self.historico_refazer) > 0
