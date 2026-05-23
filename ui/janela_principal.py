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
from processing.intensidade import aplicar_negativo, ajustar_brilho, ajustar_contraste
from processing.reamostragem import redimensionar_vizinho_mais_proximo
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox

from ui.dialog_redimensionar import DialogRedimensionar

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

        # Menu Transformações
        menu_transformacoes = barra_menu.addMenu("Transformações")

        # Menu Reamostragem
        menu_reamostragem = barra_menu.addMenu("Reamostragem")

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

        # Ação "Negativo"
        acao_negativo = QAction("Negativo", self)
        acao_negativo.triggered.connect(self.aplicar_negativo)

        # Adiciona a ação "Negativo" ao menu "Transformações"
        menu_transformacoes.addAction(acao_negativo)

        # Ação "Aumentar Brilho"
        acao_aumentar_brilho = QAction("Aumentar Brilho", self)
        acao_aumentar_brilho.triggered.connect(self.aumentar_brilho)

        # Adiciona a ação "Aumentar Brilho" ao menu "Transformações"
        menu_transformacoes.addAction(acao_aumentar_brilho)

        # Ação "Diminuir Brilho"
        acao_diminuir_brilho = QAction("Diminuir Brilho", self)
        acao_diminuir_brilho.triggered.connect(self.diminuir_brilho)    

        # Adiciona a ação "Diminuir Brilho" ao menu "Transformações"
        menu_transformacoes.addAction(acao_diminuir_brilho)

        # Ação "Ajustar Contraste"
        acao_ajustar_contraste = QAction("Ajustar Contraste", self)
        acao_ajustar_contraste.triggered.connect(self.ajustar_contraste)

        # Adiciona a ação "Ajustar Contraste" ao menu "Transformações"
        menu_transformacoes.addAction(acao_ajustar_contraste)

        # Ação "Redimensionar (Vizinho mais próximo)"
        acao_redimensionar_vizinho = QAction("Redimensionar (Vizinho mais próximo)", self)
        acao_redimensionar_vizinho.triggered.connect(self.redimensionar_vizinho)

        # Adiciona a ação "Redimensionar (Vizinho mais próximo)" ao menu "Reamostragem"
        menu_reamostragem.addAction(acao_redimensionar_vizinho)




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
        imagem = self.gerenciador_imagem.obter_imagem_atual()

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
        # Verifica se não existe imagem carregada
        if self.gerenciador_imagem.imagem_atual is None:
            return

        # Abre janela de salvamento de arquivo
        caminho_imagem, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem", "", "Imagens (*.png *.jpg *.jpeg)")

        # verifica se o usuário selecionou um caminho
        if caminho_imagem:

            # Salva a imagem usando o gerenciador de imagens
            self.gerenciador_imagem.salvar_imagem(caminho_imagem)

            # Exibe mensagem de sucesso
            QMessageBox.information(
                self,
                "Imagem salva",
                f"Imagem salva com sucesso em:\n{caminho_imagem}"
            )

    def resetar_imagem(self):
        """
        Restaura a imagem atual para a imagem original.
        """

        # Verifica se existe imagem carregada
        if self.gerenciador_imagem.imagem_original is None:
            return

        # Restaura a imagem usando o gerenciador de imagens
        self.gerenciador_imagem.resetar_imagem()

        # Exibe a imagem restaurada na interface
        self.exibir_imagem()

    def aplicar_negativo(self):
        """
        Aplica o efeito de negativo na imagem atual.
        """

        # Obtem a imagem atual do gerenciador de imagens
        imagem = self.gerenciador_imagem.obter_imagem_atual()

        # Verifica se existe imagem carregada
        if imagem is None:
            return

        # Aplica o efeito de negativo usando a função do módulo de processamento
        imagem_negativa = aplicar_negativo(imagem)

        # Atualiza a imagem atual no gerenciador
        self.gerenciador_imagem.imagem_atual = imagem_negativa

        # Exibe a imagem modificada na interface
        self.exibir_imagem()

    # método genério de ajuste de brilho
    def aplicar_brilho(self, valor):
        """
        Aplica ajuste de brilho na imagem atual.

        Args:
            valor (int): Valor a ser adicionado aos pixels para ajustar o brilho. Pode ser positivo ou negativo.
        """

        # Obtem a imagem atual do gerenciador de imagens
        imagem = self.gerenciador_imagem.obter_imagem_atual()

        # Verifica se existe imagem carregada
        if imagem is None:
            return

        # Aplica o ajuste de brilho usando a função do módulo de processamento
        imagem_brilho = ajustar_brilho(imagem, valor)

        # Atualiza a imagem atual no gerenciador
        self.gerenciador_imagem.imagem_atual = imagem_brilho

        # Exibe a imagem modificada na interface
        self.exibir_imagem()

    def aumentar_brilho(self):
        """
        Aumenta o brilho da imagem atual.
        """

        valor, ok = QInputDialog.getInt(self, "Aumentar Brilho", "Valor de brilho:", 30, 0, 255)

        if ok:
            # Aplica ajuste de brilho positivo
            self.aplicar_brilho(valor)

    def diminuir_brilho(self):
        """
        Diminui o brilho da imagem atual.
        """

        valor, ok = QInputDialog.getInt(self, "Diminuir Brilho", "Valor de brilho:", 30, 0, 255)

        if ok:
            # Aplica ajuste de brilho negativo
            self.aplicar_brilho(-valor)

    def ajustar_contraste(self):
        """
        Ajusta o contraste da imagem atual.
        """

        # obtém imagem atual do gerenciador de imagens
        imagem = self.gerenciador_imagem.obter_imagem_atual()

        # Verifica se existe imagem carregada
        if imagem is None:
            return
        
        # Solicita ao usuário o fator de contraste
        fator, ok = QInputDialog.getDouble(self, "Ajustar Contraste", "Fator de contraste (0.1 a 3.0):", 1.0, 0.1, 3.0, decimals=1)

        if ok:
            
            # Aplica o ajuste de contraste usando a função do módulo de processamento
            imagem_contraste = ajustar_contraste(imagem, fator)

            # Atualiza a imagem atual no gerenciador
            self.gerenciador_imagem.imagem_atual = imagem_contraste

            # Exibe a imagem modificada na interface
            self.exibir_imagem()

    def redimensionar_vizinho(self):
        """
        Redimensiona a imagem atual usando o método do vizinho mais próximo.
        """

        # obtém imagem atual do gerenciador de imagens
        imagem = self.gerenciador_imagem.obter_imagem_atual()

        # Verifica se existe imagem carregada
        if imagem is None:
            return
        
                # Obtém dimensões atuais
        altura, largura = imagem.shape[:2]

        # Cria janela de diálogo
        dialog = DialogRedimensionar(largura,altura)

        # Executa janela
        if dialog.exec_():

            # Obtém dimensões digitadas
            nova_largura, nova_altura = (dialog.obter_dimensoes())

            # Redimensiona imagem
            imagem_redimensionada = (redimensionar_vizinho_mais_proximo(imagem,nova_largura,nova_altura))

            # Atualiza imagem atual
            self.gerenciador_imagem.imagem_atual = (imagem_redimensionada)

            # Atualiza interface
            self.exibir_imagem()