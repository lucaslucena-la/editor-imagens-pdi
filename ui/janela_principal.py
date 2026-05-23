"""
Janela principal da aplicação.

Responsável por:
- menus
- exibição da imagem
- interação do usuário
"""

from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QAction

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from core.gerenciador_imagens import GerenciadorImagens
from utils.conversoes import cv2_to_qt

class JanelaPrincipal(QMainWindow):
    """
      Classe que representa a janela principal da aplicação.
    """

    def __init__(self):
        super().__init__()


        # Classe responsável pelas imagens
        self.gerenciador_imagem = GerenciadorImagens()

        # configurações iniciais da janela
        self.setWindowTitle("Editor de Imagens")
        self.setGeometry(100, 100, 1000, 700)

        # Área onde a imagem será exibida
        self.label_imagem = QLabel(self)

        # centraliza a imagem na janela
        self.label_imagem.setAlignment(Qt.AlignCenter)

        # Define o QLabel como widget central da janela
        self.setCentralWidget(self.label_imagem)

        # Cria o menu da interface
        self.criar_menu()

    def criar_menu(self):
        """
        Cria os menus superiores da aplicação.
        """

        # Barra de menu
        barra_menu = self.menuBar()

        # Menu "Arquivo"
        menu_arquivo = barra_menu.addMenu("Arquivo")

        # Ação "Abrir"
        acao_abrir = QAction("Abrir Imagem", self)
        acao_abrir.triggered.connect(self.abrir_imagem)

        # Adiciona a ação "Abrir" ao menu "Arquivo"
        menu_arquivo.addAction(acao_abrir)

        # Ação "Salvar"
        acao_salvar = QAction("Salvar Imagem", self)
        acao_salvar.triggered.connect(self.salvar_imagem)

        # Adiciona a ação "Salvar" ao menu "Arquivo"
        menu_arquivo.addAction(acao_salvar)

        # Ação "Resetar"
        acao_resetar = QAction("Resetar Imagem", self)
        acao_resetar.triggered.connect(self.resetar_imagem)

        # Adiciona a ação "Resetar" ao menu "Arquivo"
        menu_arquivo.addAction(acao_resetar)

    def abrir_imagem(self):
        """
        Abre uma imagem escolhida pelo usuário.
        """
        # Abre janela de seleção de arquivo
        caminho_imagem, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg)")

        # verifica se o usuário selecionou um arquivo
        if caminho_imagem:

            # Carrega a imagem usando o gerenciador de imagens
            self.gerenciador_imagem.carregar_imagem(caminho_imagem)

            # Exibe a imagem na interface
            self.exibir_imagem()

    def exibir_imagem(self):
        """
        Exibe a imagem atual na interface.
        """

        # Obtém a imagem atual do gerenciador
        imagem = self.gerenciador_imagem.obter_imagem_atual

        # cria objeto de imagem do Qt a partir do caminho da imagem carregada
        pixmap = cv2_to_qt(imagem)

        # Ajusta o tamanho da imagem para caber na área de exibição
        pixmap = pixmap.scaled(self.label_imagem.width(), self.label_imagem.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Exibe a imagem no QLabel
        self.label_imagem.setPixmap(pixmap)

    def salvar_imagem(self):
        """
        Salva a imagem atual.
        """
        # Verifica se existe imagem carregada
        if self.gerenciador_imagem.imagem_atual is not None:
            return

        # Abre janela de salvamento de arquivo
        caminho_imagem, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem", "", "Imagens (*.png *.jpg *.jpeg)")

        # verifica se o usuário selecionou um caminho
        if caminho_imagem:

            # Salva a imagem usando o gerenciador de imagens
            self.gerenciador_imagem.salvar_imagem(caminho_imagem)

    def resetar_imagem(self):
        """
        Restaura a imagem atual para a imagem original.
        """

        # Restaura a imagem usando o gerenciador de imagens
        self.gerenciador_imagem.resetar_imagem()

        # Exibe a imagem restaurada na interface
        self.exibir_imagem()
        
