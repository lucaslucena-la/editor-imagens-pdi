"""
Janela principal da aplicação.

Responsável por:
- menus
- exibição da imagem
- interação do usuário
"""

from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QAction, QMessageBox,QInputDialog, QApplication, QActionGroup

from PyQt5.QtCore import Qt

from core.gerenciador_imagens import GerenciadorImagens
from utils.conversoes import cv2_to_qt
from processing.intensidade import aplicar_negativo, ajustar_brilho, ajustar_contraste, transformacao_logaritmica, transformacao_exponencial, expansao_contraste
from processing.reamostragem import redimensionar_vizinho_mais_proximo, redimensionar_bilinear
from processing.convolucao import  aplicar_box, aplicar_sobel, aplicar_laplaciano, aplicar_mediana, aplicar_gaussiano, aplicar_agucamento_laplaciano
from processing.histograma import calcular_histograma, mostrar_histograma, equalizar_histograma
from ui.dialog_redimensionar import DialogRedimensionar
from ui.dialog_gaussiano import (DialogGaussiano)
from ui.dialog_box import (DialogBox)
from ui.dialog_mediana import (DialogMediana)


class JanelaPrincipal(QMainWindow):
    """
      Classe que representa a janela principal da aplicação.
    """
    
# ============================================================================ #
# CONFIGURAÇÕES DA INTERFACE
# ============================================================================ #

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

        # Padding padrão do sistema
        self.tipo_padding = "edge"

        # Cria o menu da interface
        self.criar_menu()

    def criar_menu(self):
        """
        Cria os menus superiores da aplicação.
        """
        # 

        # Barra de menu
        barra_menu = self.menuBar()

        menu_configuracoes = barra_menu.addMenu("Configurações")

        menu_padding = menu_configuracoes.addMenu("Padding")

        # Grupo exclusivo
        grupo_padding = QActionGroup(self)
        grupo_padding.setExclusive(True)

        # Padding por replicação
        acao_padding_replicacao = QAction("Replicação", self, checkable=True)
        acao_padding_replicacao.setChecked(True)
        acao_padding_replicacao.triggered.connect(lambda: self.definir_tipo_padding("edge"))
        grupo_padding.addAction(acao_padding_replicacao)
        menu_padding.addAction(acao_padding_replicacao)

        # padding por reflexão
        acao_padding_reflexao = QAction("Reflexão", self, checkable=True)
        acao_padding_reflexao.triggered.connect(lambda: self.definir_tipo_padding("reflect"))
        grupo_padding.addAction(acao_padding_reflexao)
        menu_padding.addAction(acao_padding_reflexao)

        # zero padding
        acao_padding_zero = QAction("Zero Padding", self, checkable=True)
        acao_padding_zero.triggered.connect(lambda: self.definir_tipo_padding("constant"))
        grupo_padding.addAction(acao_padding_zero)
        menu_padding.addAction(acao_padding_zero)

        # Menu "Arquivo"
        menu_arquivo = barra_menu.addMenu("Arquivo")

        # Menu Transformações
        menu_transformacoes = barra_menu.addMenu("Transformações")

        # Menu Histograma
        menu_histograma = barra_menu.addMenu("Histograma")

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

        # adiciona a ação "Expansão de Contraste" ao menu "Transformações"
        acao_expansao_contraste = QAction("Expansão de Contraste", self)
        acao_expansao_contraste.triggered.connect(self.aplicar_expansao_contraste)

        # Adiciona a ação "Expansão de Contraste" ao menu "Transformações"
        menu_transformacoes.addAction(acao_expansao_contraste)

        # adiciona a ação "Transformação Logarítmica" ao menu "Transformações"
        acao_transformacao_logaritmica = QAction("Transformação Logarítmica", self)
        acao_transformacao_logaritmica.triggered.connect(self.aplicar_transformacao_logaritmica)
        
        # Adiciona a ação "Transformação Logarítmica" ao menu "Transformações"
        menu_transformacoes.addAction(acao_transformacao_logaritmica)

        # adiciona a ação "Transformação Exponencial" ao menu "Transformações"
        acao_transformacao_exponencial = QAction("Transformação Exponencial", self)
        acao_transformacao_exponencial.triggered.connect(self.aplicar_transformacao_exponencial)

        # Adiciona a ação "Transformação Exponencial" ao menu "Transformações"
        menu_transformacoes.addAction(acao_transformacao_exponencial)

        # adiciona a ação "Mostrar Histograma" ao menu "Histograma"
        acao_mostrar_histograma = QAction("Mostrar Histograma", self)
        acao_mostrar_histograma.triggered.connect(self.mostrar_histograma)

        # Adiciona a ação "Mostrar Histograma" ao menu "Histograma"
        menu_histograma.addAction(acao_mostrar_histograma)

        # adiciona a ação "Equalizar Histograma" ao menu "Histograma"
        acao_equalizar_histograma = QAction("Equalizar Histograma", self)
        acao_equalizar_histograma.triggered.connect(self.aplicar_equalizacao_histograma)

        # Adiciona a ação "Equalizar Histograma" ao menu "Histograma"
        menu_histograma.addAction(acao_equalizar_histograma)

        # Ação "Redimensionar (Vizinho mais próximo)"
        acao_redimensionar_vizinho = QAction("Redimensionar (Vizinho mais próximo)", self)
        acao_redimensionar_vizinho.triggered.connect(self.redimensionar_vizinho)

        # Adiciona a ação "Redimensionar (Vizinho mais próximo)" ao menu "Reamostragem"
        menu_reamostragem.addAction(acao_redimensionar_vizinho)

        # Ação "Redimensionar (Bilinear)"
        acao_redimensionar_bilinear = QAction("Redimensionar (Bilinear)", self)
        acao_redimensionar_bilinear.triggered.connect(self.redimensionar_bilinear)

        # Adiciona a ação "Redimensionar (Bilinear)" ao menu "Reamostragem"
        menu_reamostragem.addAction(acao_redimensionar_bilinear)

        # Menu "Filtros"
        menu_filtros = barra_menu.addMenu("Filtros")

        # Submenu "Aguçamento"
        menu_agucamento = menu_filtros.addMenu("Aguçamento")

        # Ação "Aguçamento Laplaciano"
        acao_agucamento_laplaciano = QAction("Aguçamento Laplaciano", self)
        acao_agucamento_laplaciano.triggered.connect(self.aplicar_agucamento_laplaciano)

        # Adiciona a ação "Aguçamento Laplaciano" ao submenu "Aguçamento"
        menu_agucamento.addAction(acao_agucamento_laplaciano)

        # Ação "Filtro Sobel"
        acao_filtro_sobel = QAction("Filtro Sobel", self)
        acao_filtro_sobel.triggered.connect(self.aplicar_sobel)

        # Adiciona a ação "Filtro Sobel" ao menu "Filtros"
        menu_filtros.addAction(acao_filtro_sobel)

        # Ação "Filtro Laplaciano"
        acao_filtro_laplaciano = QAction("Filtro Laplaciano", self)
        acao_filtro_laplaciano.triggered.connect(self.aplicar_laplaciano)

        # Adiciona a ação "Filtro Laplaciano" ao menu "Filtros"
        menu_filtros.addAction(acao_filtro_laplaciano)


        #-------------------------------------------

        # Ação "Filtro Gaussiano"
        acao_gaussiano = QAction("Gaussiano",self)
        acao_gaussiano.triggered.connect(self.aplicar_gaussiano)

        # Adiciona a ação "Filtro Gaussiano " ao menu "Filtros"
        menu_filtros.addAction(acao_gaussiano)

        # Ação "Filtro Box "
        acao_box = QAction("Box ", self)
        acao_box.triggered.connect(self.aplicar_box)

        # Adiciona a ação "Filtro Box " ao menu "Filtros"
        menu_filtros.addAction(acao_box)

        # Ação "Filtro Mediana"
        acao_filtro_mediana = QAction("Filtro Mediana", self)
        acao_filtro_mediana.triggered.connect(self.aplicar_mediana)

        # Adiciona a ação "Filtro Mediana" ao menu "Filtros"
        menu_filtros.addAction(acao_filtro_mediana)

    def definir_tipo_padding(self, tipo):
        """
        Define o tipo de padding a ser utilizado nos filtros.

        Args:
            tipo (str): Tipo de padding ("edge", "reflect" ou "constant").
        """
        self.tipo_padding = tipo
        QMessageBox.information(
            self,
            "Tipo de Padding",
            f"Tipo de padding definido para: {tipo}"
        )

# ============================================================================ #
# OPERAÇÕES DE ARQUIVO
# ============================================================================ #

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

# ============================================================================ #
# TRANSFORMAÇÕES DE INTENSIDADE
# ============================================================================ #

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

    def aplicar_brilho(self, valor):
        """
        Aplica ajuste de brilho na imagem atual.

        Args:
            valor (int): Valor a ser adicionado aos pixels para ajustar o brilho. Pode ser positivo ou negativo.
        """

        # Obtem a imagem atual do gerenciador de imagens
        imagem_base = self.gerenciador_imagem.imagem_original

        # Verifica se existe imagem carregada
        if imagem_base is None:
            return
        
        # Acumula o offset de brilho
        self.gerenciador_imagem.offset_brilho += valor
        
        # Limita faixa para evitar valores extremos
        if self.gerenciador_imagem.offset_brilho > 255:
            self.gerenciador_imagem.offset_brilho = 255
        elif self.gerenciador_imagem.offset_brilho < -255:
            self.gerenciador_imagem.offset_brilho = -255

        # Recalcula sempre a partir da imagem original
        imagem_brilho = ajustar_brilho(imagem_base, self.gerenciador_imagem.offset_brilho)

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
        imagem_base = self.gerenciador_imagem.imagem_original

        # Verifica se existe imagem carregada
        if imagem_base is None:
            return
        
        # # Fator percentual: negativo diminui, positivo aumenta
        # Ex.: +40 => aumenta; -40 => diminui
        fator, ok = QInputDialog.getInt(self, "Ajustar Contraste", "Fator de contraste (-100 a 100):", 0, -100, 100)

        if not ok:
            return

        # Acumula o offset de contraste
        self.gerenciador_imagem.offset_contraste += fator

        # Limita faixa para evitar valores extremos
        if self.gerenciador_imagem.offset_contraste > 200:
            self.gerenciador_imagem.offset_contraste = 200
        elif self.gerenciador_imagem.offset_contraste < -100:
            self.gerenciador_imagem.offset_contraste = -100

        # mapeita offset percentual para fator de contraste
        # offset = 0   -> fator 1.0 (original)
        # offset = +x  -> fator 1 + x/100
        # offset = -x  -> fator 1/(1 + x/100)
        offset = self.gerenciador_imagem.offset_contraste
        if offset >= 0:
            fator_contraste = 1.0 + (offset / 100.0)
        else:
            fator_contraste = 1.0 / (1.0 + abs(offset) / 100.0)

        # Recalcula sempre a partir da imagem original
        imagem_contraste = ajustar_contraste(imagem_base, fator_contraste)

        # Atualiza a imagem atual no gerenciador
        self.gerenciador_imagem.imagem_atual = imagem_contraste

        # Exibe a imagem modificada na interface
        self.exibir_imagem()

    def aplicar_expansao_contraste(self):
        """
        Aplica expansão linear de contraste.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        imagem_transformada = expansao_contraste(
            imagem
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

    def aplicar_transformacao_logaritmica(self):
        """
        Aplica transformação logarítmica.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        imagem_transformada = (
            transformacao_logaritmica(imagem)
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

    def aplicar_transformacao_exponencial(self):
        """
        Aplica transformação exponencial.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        imagem_transformada = (
            transformacao_exponencial(imagem)
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

# ============================================================================ #
# HISTOGRAMA
# ============================================================================ #

    def mostrar_histograma(self):
        """
        Exibe o histograma da imagem atual.
        """

        imagem = (self.gerenciador_imagem.obter_imagem_atual())

        if imagem is None:
            return

        hist_b, hist_g, hist_r = calcular_histograma(imagem)

        altura, largura = imagem.shape[:2]

        print()
        print("========== TESTE HISTOGRAMA ==========")
        print("Dimensões:", altura, "x", largura)
        print("Total esperado:", altura * largura)

        print("Canal B:", hist_b.sum())
        print("Canal G:", hist_g.sum())
        print("Canal R:", hist_r.sum())
        print("======================================")
        print()

        mostrar_histograma(imagem)

    def aplicar_equalizacao_histograma(self):
        """
        Aplica equalização de histograma
        na imagem atual.
        """

        imagem = (
            self.gerenciador_imagem
            .obter_imagem_atual()
        )

        if imagem is None:
            return

        # Mostra cursor de espera
        QApplication.setOverrideCursor(
            Qt.WaitCursor
        )

        try:

            imagem_equalizada = (
                equalizar_histograma(imagem)
            )

            self.gerenciador_imagem.imagem_atual = (
                imagem_equalizada
            )

            self.exibir_imagem()

        finally:

            QApplication.restoreOverrideCursor()
# ============================================================================ #
# REAMOSTRAGEM DE IMAGENS
# ============================================================================ #

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

    def redimensionar_bilinear(self):
        """
        Redimensiona a imagem atual usando o método de interpolação bilinear.
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
            imagem_redimensionada = (redimensionar_bilinear(imagem,nova_largura,nova_altura))

            # Atualiza imagem atual
            self.gerenciador_imagem.imagem_atual = (imagem_redimensionada)

            # Atualiza interface
            self.exibir_imagem()

# ============================================================================ #
# FILTROS DE DETECÇÃO DE BORDAS
# ============================================================================ #

    def aplicar_sobel(self):
        """
        Aplica filtro Sobel.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        # Mostra cursor de espera
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:

            imagem_filtrada = aplicar_sobel(imagem)

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

        finally:

            # Restaura cursor normal
            QApplication.restoreOverrideCursor()

    def aplicar_laplaciano(self):
        """
        Aplica filtro Laplaciano.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        # Mostra cursor de espera
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:

            imagem_filtrada = aplicar_laplaciano(imagem)

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

        finally:

            # Restaura cursor normal
            QApplication.restoreOverrideCursor()

# ============================================================================ #
# FILTROS DE SUAVIZAÇÃO
# ============================================================================ #    

    def aplicar_box(self):
        """
        Aplica filtro Box parametrizado pelo usuário.
        """

        imagem = (
            self.gerenciador_imagem
            .obter_imagem_atual()
        )

        if imagem is None:
            return

        dialog = DialogBox()

        if dialog.exec_():

            tamanho = dialog.obter_parametros()

            # Mostra cursor de espera durante o processamento
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:

                imagem_filtrada = (
                    aplicar_box(
                        imagem,
                        tamanho_kernel=tamanho,
                        padding=self.tipo_padding
                    )
                )

                self.gerenciador_imagem.imagem_atual = (
                    imagem_filtrada
                )

                self.exibir_imagem()

            finally:

                # Restaura cursor normal após o filtro
                QApplication.restoreOverrideCursor()

    def aplicar_gaussiano(self):
        """
        Aplica filtro gaussiano
        parametrizado.
        """

        imagem = (
            self.gerenciador_imagem
            .obter_imagem_atual()
        )

        if imagem is None:
            return

        dialog = DialogGaussiano()

        if dialog.exec_():

            tamanho, sigma = (
                dialog.obter_parametros()
            )

            imagem_filtrada = (
                aplicar_gaussiano(
                    imagem,
                    tamanho,
                    sigma,
                    padding=self.tipo_padding
                )
            )

            self.gerenciador_imagem.imagem_atual = (
                imagem_filtrada
            )

            self.exibir_imagem()

    def aplicar_mediana(self):
        """
        Aplica filtro de mediana com tamanho de kernel definido pelo usuário.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        tamanho_kernel, ok = QInputDialog.getInt(
            self,
            "Filtro Mediana",
            "Tamanho do kernel (ímpar):",
            7,
            3,
            21,
            2
        )

        if not ok:
            return

        # Garante um kernel ímpar para o cálculo da mediana
        if tamanho_kernel % 2 == 0: # se for par, mostra mensagem de erro e retorna
            QMessageBox.warning(
                self,
                "Kernel inválido",
                "O tamanho do kernel da mediana deve ser ímpar."
            )
            return

        # Mostra cursor de espera
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:

            imagem_filtrada = aplicar_mediana(
                imagem,
                tamanho_kernel=tamanho_kernel,
                padding=self.tipo_padding
            )

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

        finally:

            # Restaura cursor normal
            QApplication.restoreOverrideCursor()


# ============================================================================ #
# AGUÇAMENTO
# ============================================================================ #

    def aplicar_agucamento_laplaciano(self):
        """
        Aplica aguçamento utilizando
        filtro Laplaciano.
        """

        imagem = (
            self.gerenciador_imagem
            .obter_imagem_atual()
        )

        if imagem is None:
            return

        QApplication.setOverrideCursor(
            Qt.WaitCursor
        )

        try:

            resultado = aplicar_agucamento_laplaciano(
                imagem
            )

            self.gerenciador_imagem.imagem_atual = (
                resultado
            )

            self.exibir_imagem()

        finally:

            QApplication.restoreOverrideCursor()