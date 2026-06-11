"""
Janela principal da aplicação.

Responsável por:
- menus
- exibição da imagem
- interação do usuário
"""

from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QFileDialog,
    QAction,
    QMessageBox,
    QInputDialog,
    QApplication,
    QActionGroup,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QFrame
)

from PyQt5.QtCore import Qt, QTimer

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

        # Armazena ações dependentes de imagem carregada
        self.acoes_com_imagem = []

        # Armazena controles dependentes de histórico
        self.controles_desfazer = []
        self.controles_refazer = []

        # configurações iniciais da janela
        self.setWindowTitle("Editor de Imagens")
        self.setGeometry(100, 100, 1280, 820)
        self.setMinimumSize(960, 640)

        # Padding padrão do sistema
        self.tipo_padding = "edge"

        # Prepara a estrutura visual da janela principal
        self.criar_area_central()

        # Cria o menu da interface
        self.criar_menu()

        # Cria barra de status com informações da imagem
        self.criar_barra_status()

        # Ajusta o estado inicial da interface
        self.registrar_controle_desfazer(self.botao_desfazer)
        self.registrar_controle_refazer(self.botao_refazer)
        self.atualizar_estado_interface()

    def criar_area_central(self):
        """
        Cria a área central com painel de boas-vindas
        e região de visualização da imagem.
        """

        # Widget base da janela principal
        widget_central = QWidget()

        # Layout principal da tela
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(24, 20, 24, 24)
        layout_principal.setSpacing(16)

        # Cabeçalho com contexto visual da aplicação
        cabecalho = QFrame()
        cabecalho.setObjectName("painelCabecalho")
        cabecalho.setStyleSheet(
            "QFrame#painelCabecalho {"
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 14px;"
            "}"
        )

        layout_cabecalho = QVBoxLayout()
        layout_cabecalho.setContentsMargins(20, 18, 20, 18)
        layout_cabecalho.setSpacing(6)

        self.label_titulo = QLabel("Editor de Imagens")
        self.label_titulo.setStyleSheet(
            "font-size: 24px; font-weight: 700; color: #111827;"
        )

        self.label_subtitulo = QLabel(
            "Abra uma imagem e aplique filtros, transformações e ajustes com visualização imediata."
        )
        self.label_subtitulo.setWordWrap(True)
        self.label_subtitulo.setStyleSheet(
            "font-size: 13px; color: #6b7280;"
        )

        layout_cabecalho.addWidget(self.label_titulo)
        layout_cabecalho.addWidget(self.label_subtitulo)
        cabecalho.setLayout(layout_cabecalho)

        # Painel de boas-vindas quando não há imagem carregada
        self.painel_vazio = QFrame()
        self.painel_vazio.setObjectName("painelVazio")
        self.painel_vazio.setStyleSheet(
            "QFrame#painelVazio {"
            "background-color: #ffffff;"
            "border: 1px dashed #d1d5db;"
            "border-radius: 16px;"
            "}"
        )

        layout_vazio = QVBoxLayout()
        layout_vazio.setContentsMargins(40, 48, 40, 48)
        layout_vazio.setSpacing(12)
        layout_vazio.setAlignment(Qt.AlignCenter)

        self.label_estado_vazio = QLabel("Nenhuma imagem carregada")
        self.label_estado_vazio.setAlignment(Qt.AlignCenter)
        self.label_estado_vazio.setStyleSheet(
            "font-size: 22px; font-weight: 700; color: #111827;"
        )

        self.label_estado_vazio_info = QLabel(
            "Use o menu Arquivo para abrir arquivos PNG, JPG ou JPEG."
        )
        self.label_estado_vazio_info.setAlignment(Qt.AlignCenter)
        self.label_estado_vazio_info.setWordWrap(True)
        self.label_estado_vazio_info.setStyleSheet(
            "font-size: 13px; color: #6b7280;"
        )

        layout_vazio.addWidget(self.label_estado_vazio)
        layout_vazio.addWidget(self.label_estado_vazio_info)
        self.painel_vazio.setLayout(layout_vazio)

        # Área onde a imagem será exibida
        self.label_imagem = QLabel()

        # Centraliza a imagem na janela
        self.label_imagem.setAlignment(Qt.AlignCenter)
        self.label_imagem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_imagem.setMinimumSize(480, 360)
        self.label_imagem.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 16px;"
            "padding: 16px;"
        )

        # Permite navegação em imagens maiores que a área visível
        self.area_imagem = QScrollArea()
        self.area_imagem.setWidgetResizable(True)
        self.area_imagem.setAlignment(Qt.AlignCenter)
        self.area_imagem.setStyleSheet(
            "QScrollArea {"
            "background-color: #ffffff;"
            "border: none;"
            "background: transparent;"
            "}"
        )
        self.area_imagem.setWidget(self.label_imagem)

        # Container da área de edição com ação de desfazer
        self.painel_edicao = QFrame()
        self.painel_edicao.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 16px;"
        )

        layout_painel_edicao = QVBoxLayout()
        layout_painel_edicao.setContentsMargins(16, 16, 16, 16)
        layout_painel_edicao.setSpacing(12)

        # Linha superior da área da imagem
        linha_acoes = QHBoxLayout()
        linha_acoes.setContentsMargins(0, 0, 0, 0)
        linha_acoes.setSpacing(10)

        self.botao_desfazer = QPushButton("<-")
        self.botao_desfazer.setMinimumWidth(52)
        self.botao_desfazer.clicked.connect(self.desfazer_ultima_acao)

        self.botao_refazer = QPushButton("->")
        self.botao_refazer.setMinimumWidth(52)
        self.botao_refazer.clicked.connect(self.refazer_ultima_acao)

        linha_acoes.addStretch()
        linha_acoes.addWidget(self.botao_desfazer)
        linha_acoes.addWidget(self.botao_refazer)

        layout_painel_edicao.addLayout(linha_acoes)
        layout_painel_edicao.addWidget(self.area_imagem, 1)
        self.painel_edicao.setLayout(layout_painel_edicao)

        layout_principal.addWidget(cabecalho)
        layout_principal.addWidget(self.painel_vazio, 1)
        layout_principal.addWidget(self.painel_edicao, 1)

        widget_central.setLayout(layout_principal)

        # Define o widget composto como widget central da janela
        self.setCentralWidget(widget_central)

    def criar_barra_status(self):
        """
        Cria a barra de status com informações da imagem atual.
        """

        # Barra inferior para feedback contínuo ao usuário
        self.statusBar().showMessage("Pronto para abrir uma imagem.")

        self.label_status_arquivo = QLabel("Arquivo: nenhum")
        self.label_status_dimensoes = QLabel("Dimensões: -")
        self.label_status_padding = QLabel(f"Padding: {self.tipo_padding}")

        self.statusBar().addPermanentWidget(self.label_status_arquivo)
        self.statusBar().addPermanentWidget(self.label_status_dimensoes)
        self.statusBar().addPermanentWidget(self.label_status_padding)

    def atualizar_estado_desfazer(self):
        """
        Atualiza o estado dos controles de desfazer.
        """

        # Habilita o desfazer apenas quando existir histórico válido
        possui_imagem = self.gerenciador_imagem.imagem_atual is not None
        possui_historico = self.gerenciador_imagem.possui_historico()
        pode_desfazer = possui_imagem and possui_historico

        for controle in self.controles_desfazer:
            controle.setEnabled(pode_desfazer)

    def atualizar_estado_refazer(self):
        """
        Atualiza o estado dos controles de refazer.
        """

        # Habilita o refazer apenas quando existir histórico válido
        possui_imagem = self.gerenciador_imagem.imagem_atual is not None
        possui_refazer = self.gerenciador_imagem.possui_refazer()
        pode_refazer = possui_imagem and possui_refazer

        for controle in self.controles_refazer:
            controle.setEnabled(pode_refazer)

    def atualizar_estado_interface(self):
        """
        Atualiza a interface conforme a existência
        de imagem carregada.
        """

        # Verifica se existe imagem disponível para edição
        possui_imagem = self.gerenciador_imagem.imagem_atual is not None

        # Exibe painel vazio somente quando necessário
        self.painel_vazio.setVisible(not possui_imagem)
        self.painel_edicao.setVisible(possui_imagem)

        # Habilita ou desabilita ações dependentes de imagem
        for acao in self.acoes_com_imagem:
            acao.setEnabled(possui_imagem)

        # Atualiza o texto principal do cabeçalho
        if possui_imagem:
            self.label_subtitulo.setText(
                "A imagem está pronta para edição. Use o menu superior ou a barra de ferramentas para aplicar operações."
            )
        else:
            self.label_subtitulo.setText(
                "Abra uma imagem e aplique filtros, transformações e ajustes com visualização imediata."
            )

        # Mantém os indicadores inferiores sincronizados
        self.atualizar_status_imagem()

        # Mantém o estado do desfazer sincronizado
        self.atualizar_estado_desfazer()

        # Mantém o estado do refazer sincronizado
        self.atualizar_estado_refazer()

    def atualizar_status_imagem(self, mensagem=None):
        """
        Atualiza os textos da barra de status.

        Args:
            mensagem (str, optional): Mensagem temporária da operação atual.
        """

        # Lê a imagem atual para montar os indicadores da interface
        imagem = self.gerenciador_imagem.imagem_atual

        if imagem is None:
            self.label_status_arquivo.setText("Arquivo: nenhum")
            self.label_status_dimensoes.setText("Dimensões: -")
            self.label_status_padding.setText(f"Padding: {self.tipo_padding}")

            if mensagem is None:
                self.statusBar().showMessage("Pronto para abrir uma imagem.")
            else:
                self.statusBar().showMessage(mensagem, 5000)

            return

        # Atualiza nome do arquivo atual quando disponível
        caminho_arquivo = getattr(self.gerenciador_imagem, "caminho_imagem", None)
        nome_arquivo = caminho_arquivo.split("\\")[-1] if caminho_arquivo else "imagem em memória"

        altura, largura = imagem.shape[:2]

        self.label_status_arquivo.setText(f"Arquivo: {nome_arquivo}")
        self.label_status_dimensoes.setText(f"Dimensões: {largura} x {altura}")
        self.label_status_padding.setText(f"Padding: {self.tipo_padding}")

        if mensagem is None:
            self.statusBar().showMessage("Imagem pronta para edição.")
        else:
            self.statusBar().showMessage(mensagem, 5000)

    def salvar_estado_antes_edicao(self):
        """
        Salva o estado atual antes de editar a imagem.
        """

        # Armazena o estado corrente para permitir desfazer
        self.gerenciador_imagem.salvar_estado()

        # Atualiza disponibilidade dos controles de desfazer
        self.atualizar_estado_desfazer()

        # Atualiza disponibilidade dos controles de refazer
        self.atualizar_estado_refazer()

    def desfazer_ultima_acao(self):
        """
        Desfaz a última alteração realizada na imagem.
        """

        # Tenta restaurar o último estado salvo
        if not self.gerenciador_imagem.desfazer():
            return

        # Atualiza a imagem na interface após desfazer
        self.exibir_imagem()

        # Atualiza o resumo da operação na barra inferior
        self.atualizar_status_imagem(
            "Última alteração desfeita."
        )

        # Mantém o estado dos controles sincronizado
        self.atualizar_estado_desfazer()
        self.atualizar_estado_refazer()

    def refazer_ultima_acao(self):
        """
        Refaz a última alteração desfeita na imagem.
        """

        # Tenta restaurar o último estado desfeito
        if not self.gerenciador_imagem.refazer():
            return

        # Atualiza a imagem na interface após refazer
        self.exibir_imagem()

        # Atualiza o resumo da operação na barra inferior
        self.atualizar_status_imagem(
            "Última alteração refeita."
        )

        # Mantém o estado dos controles sincronizado
        self.atualizar_estado_desfazer()
        self.atualizar_estado_refazer()

    def registrar_acao_com_imagem(self, acao):
        """
        Registra ações que dependem de imagem carregada.

        Args:
            acao (QAction): Ação a ser controlada pela interface.
        """

        self.acoes_com_imagem.append(acao)
        acao.setEnabled(False)

    def registrar_controle_desfazer(self, controle):
        """
        Registra controles vinculados ao desfazer.

        Args:
            controle (QWidget): Controle habilitado quando houver histórico.
        """

        self.controles_desfazer.append(controle)
        controle.setEnabled(False)

    def registrar_controle_refazer(self, controle):
        """
        Registra controles vinculados ao refazer.

        Args:
            controle (QWidget): Controle habilitado quando houver refazer.
        """

        self.controles_refazer.append(controle)
        controle.setEnabled(False)

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
        self.acao_abrir = QAction("Abrir Imagem", self)
        self.acao_abrir.setShortcut("Ctrl+O")
        self.acao_abrir.setStatusTip("Abre uma imagem do disco")
        self.acao_abrir.triggered.connect(self.abrir_imagem)

        # Adiciona a ação "Abrir" ao menu "Arquivo"
        menu_arquivo.addAction(self.acao_abrir)

        # Ação "Salvar"
        self.acao_salvar = QAction("Salvar Imagem", self)
        self.acao_salvar.setShortcut("Ctrl+S")
        self.acao_salvar.setStatusTip("Salva a imagem editada")
        self.acao_salvar.triggered.connect(self.salvar_imagem)

        # Adiciona a ação "Salvar" ao menu "Arquivo"
        menu_arquivo.addAction(self.acao_salvar)
        self.registrar_acao_com_imagem(self.acao_salvar)

        # Ação "Desfazer"
        self.acao_desfazer = QAction("Desfazer", self)
        self.acao_desfazer.setShortcut("Ctrl+Z")
        self.acao_desfazer.setStatusTip("Desfaz a última alteração realizada")
        self.acao_desfazer.triggered.connect(self.desfazer_ultima_acao)
        self.registrar_acao_com_imagem(self.acao_desfazer)
        self.registrar_controle_desfazer(self.acao_desfazer)
        self.addAction(self.acao_desfazer)

        # Ação "Refazer"
        self.acao_refazer = QAction("Refazer", self)
        self.acao_refazer.setShortcut("Ctrl+Y")
        self.acao_refazer.setStatusTip("Refaz a última alteração desfeita")
        self.acao_refazer.triggered.connect(self.refazer_ultima_acao)
        self.registrar_acao_com_imagem(self.acao_refazer)
        self.registrar_controle_refazer(self.acao_refazer)
        self.addAction(self.acao_refazer)

        # Ação "Resetar"
        self.acao_resetar = QAction("Resetar Imagem", self)
        self.acao_resetar.setShortcut("Ctrl+R")
        self.acao_resetar.setStatusTip("Restaura a imagem original carregada")
        self.acao_resetar.triggered.connect(self.resetar_imagem)

        # Adiciona a ação "Resetar" ao menu "Arquivo"
        menu_arquivo.addAction(self.acao_resetar)
        self.registrar_acao_com_imagem(self.acao_resetar)

        # Ação "Negativo"
        self.acao_negativo = QAction("Negativo", self)
        self.acao_negativo.setStatusTip("Aplica o efeito negativo na imagem")
        self.acao_negativo.triggered.connect(self.aplicar_negativo)

        # Adiciona a ação "Negativo" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_negativo)
        self.registrar_acao_com_imagem(self.acao_negativo)

        # Ação "Aumentar Brilho"
        self.acao_aumentar_brilho = QAction("Aumentar Brilho", self)
        self.acao_aumentar_brilho.setStatusTip("Aumenta o brilho da imagem")
        self.acao_aumentar_brilho.triggered.connect(self.aumentar_brilho)

        # Adiciona a ação "Aumentar Brilho" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_aumentar_brilho)
        self.registrar_acao_com_imagem(self.acao_aumentar_brilho)

        # Ação "Diminuir Brilho"
        self.acao_diminuir_brilho = QAction("Diminuir Brilho", self)
        self.acao_diminuir_brilho.setStatusTip("Reduz o brilho da imagem")
        self.acao_diminuir_brilho.triggered.connect(self.diminuir_brilho)

        # Adiciona a ação "Diminuir Brilho" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_diminuir_brilho)
        self.registrar_acao_com_imagem(self.acao_diminuir_brilho)

        # Ação "Ajustar Contraste"
        self.acao_ajustar_contraste = QAction("Ajustar Contraste", self)
        self.acao_ajustar_contraste.setStatusTip("Ajusta o contraste da imagem")
        self.acao_ajustar_contraste.triggered.connect(self.ajustar_contraste)

        # Adiciona a ação "Ajustar Contraste" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_ajustar_contraste)
        self.registrar_acao_com_imagem(self.acao_ajustar_contraste)

        # adiciona a ação "Expansão de Contraste" ao menu "Transformações"
        self.acao_expansao_contraste = QAction("Expansão de Contraste", self)
        self.acao_expansao_contraste.setStatusTip("Aplica expansão linear de contraste")
        self.acao_expansao_contraste.triggered.connect(self.aplicar_expansao_contraste)

        # Adiciona a ação "Expansão de Contraste" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_expansao_contraste)
        self.registrar_acao_com_imagem(self.acao_expansao_contraste)

        # adiciona a ação "Transformação Logarítmica" ao menu "Transformações"
        self.acao_transformacao_logaritmica = QAction("Transformação Logarítmica", self)
        self.acao_transformacao_logaritmica.setStatusTip("Aplica transformação logarítmica")
        self.acao_transformacao_logaritmica.triggered.connect(self.aplicar_transformacao_logaritmica)
        
        # Adiciona a ação "Transformação Logarítmica" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_transformacao_logaritmica)
        self.registrar_acao_com_imagem(self.acao_transformacao_logaritmica)

        # adiciona a ação "Transformação Exponencial" ao menu "Transformações"
        self.acao_transformacao_exponencial = QAction("Transformação Exponencial", self)
        self.acao_transformacao_exponencial.setStatusTip("Aplica transformação exponencial")
        self.acao_transformacao_exponencial.triggered.connect(self.aplicar_transformacao_exponencial)

        # Adiciona a ação "Transformação Exponencial" ao menu "Transformações"
        menu_transformacoes.addAction(self.acao_transformacao_exponencial)
        self.registrar_acao_com_imagem(self.acao_transformacao_exponencial)

        # adiciona a ação "Mostrar Histograma" ao menu "Histograma"
        self.acao_mostrar_histograma = QAction("Mostrar Histograma", self)
        self.acao_mostrar_histograma.setStatusTip("Exibe o histograma da imagem atual")
        self.acao_mostrar_histograma.triggered.connect(self.mostrar_histograma)

        # Adiciona a ação "Mostrar Histograma" ao menu "Histograma"
        menu_histograma.addAction(self.acao_mostrar_histograma)
        self.registrar_acao_com_imagem(self.acao_mostrar_histograma)

        # adiciona a ação "Equalizar Histograma" ao menu "Histograma"
        self.acao_equalizar_histograma = QAction("Equalizar Histograma", self)
        self.acao_equalizar_histograma.setStatusTip("Aplica equalização no histograma")
        self.acao_equalizar_histograma.triggered.connect(self.aplicar_equalizacao_histograma)

        # Adiciona a ação "Equalizar Histograma" ao menu "Histograma"
        menu_histograma.addAction(self.acao_equalizar_histograma)
        self.registrar_acao_com_imagem(self.acao_equalizar_histograma)

        # Ação "Redimensionar (Vizinho mais próximo)"
        self.acao_redimensionar_vizinho = QAction("Redimensionar (Vizinho mais próximo)", self)
        self.acao_redimensionar_vizinho.setStatusTip("Redimensiona pela técnica do vizinho mais próximo")
        self.acao_redimensionar_vizinho.triggered.connect(self.redimensionar_vizinho)

        # Adiciona a ação "Redimensionar (Vizinho mais próximo)" ao menu "Reamostragem"
        menu_reamostragem.addAction(self.acao_redimensionar_vizinho)
        self.registrar_acao_com_imagem(self.acao_redimensionar_vizinho)

        # Ação "Redimensionar (Bilinear)"
        self.acao_redimensionar_bilinear = QAction("Redimensionar (Bilinear)", self)
        self.acao_redimensionar_bilinear.setStatusTip("Redimensiona com interpolação bilinear")
        self.acao_redimensionar_bilinear.triggered.connect(self.redimensionar_bilinear)

        # Adiciona a ação "Redimensionar (Bilinear)" ao menu "Reamostragem"
        menu_reamostragem.addAction(self.acao_redimensionar_bilinear)
        self.registrar_acao_com_imagem(self.acao_redimensionar_bilinear)

        # Menu "Filtros"
        menu_filtros = barra_menu.addMenu("Filtros")

        # Submenu "Aguçamento"
        menu_agucamento = menu_filtros.addMenu("Aguçamento")

        # Ação "Aguçamento Laplaciano"
        self.acao_agucamento_laplaciano = QAction("Aguçamento Laplaciano", self)
        self.acao_agucamento_laplaciano.setStatusTip("Realça detalhes com aguçamento laplaciano")
        self.acao_agucamento_laplaciano.triggered.connect(self.aplicar_agucamento_laplaciano)

        # Adiciona a ação "Aguçamento Laplaciano" ao submenu "Aguçamento"
        menu_agucamento.addAction(self.acao_agucamento_laplaciano)
        self.registrar_acao_com_imagem(self.acao_agucamento_laplaciano)

        # Ação "Filtro Sobel"
        self.acao_filtro_sobel = QAction("Filtro Sobel", self)
        self.acao_filtro_sobel.setStatusTip("Aplica detecção de bordas com Sobel")
        self.acao_filtro_sobel.triggered.connect(self.aplicar_sobel)

        # Adiciona a ação "Filtro Sobel" ao menu "Filtros"
        menu_filtros.addAction(self.acao_filtro_sobel)
        self.registrar_acao_com_imagem(self.acao_filtro_sobel)

        # Ação "Filtro Laplaciano"
        self.acao_filtro_laplaciano = QAction("Filtro Laplaciano", self)
        self.acao_filtro_laplaciano.setStatusTip("Aplica detecção de bordas com Laplaciano")
        self.acao_filtro_laplaciano.triggered.connect(self.aplicar_laplaciano)

        # Adiciona a ação "Filtro Laplaciano" ao menu "Filtros"
        menu_filtros.addAction(self.acao_filtro_laplaciano)
        self.registrar_acao_com_imagem(self.acao_filtro_laplaciano)


        #-------------------------------------------

        # Ação "Filtro Gaussiano"
        self.acao_gaussiano = QAction("Filtro Gaussiano", self)
        self.acao_gaussiano.setStatusTip("Aplica suavização gaussiana")
        self.acao_gaussiano.triggered.connect(self.aplicar_gaussiano)

        # Adiciona a ação "Filtro Gaussiano " ao menu "Filtros"
        menu_filtros.addAction(self.acao_gaussiano)
        self.registrar_acao_com_imagem(self.acao_gaussiano)

        # Ação "Filtro Box "
        self.acao_box = QAction("Filtro Box", self)
        self.acao_box.setStatusTip("Aplica suavização por média")
        self.acao_box.triggered.connect(self.aplicar_box)

        # Adiciona a ação "Filtro Box " ao menu "Filtros"
        menu_filtros.addAction(self.acao_box)
        self.registrar_acao_com_imagem(self.acao_box)

        # Ação "Filtro Mediana"
        self.acao_filtro_mediana = QAction("Filtro Mediana", self)
        self.acao_filtro_mediana.setStatusTip("Aplica redução de ruído com mediana")
        self.acao_filtro_mediana.triggered.connect(self.aplicar_mediana)

        # Adiciona a ação "Filtro Mediana" ao menu "Filtros"
        menu_filtros.addAction(self.acao_filtro_mediana)
        self.registrar_acao_com_imagem(self.acao_filtro_mediana)

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

        # Atualiza informação persistente na barra inferior
        self.atualizar_status_imagem(
            f"Padding alterado para: {tipo}"
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

            try:

                # Carrega a imagem usando o gerenciador de imagens
                self.gerenciador_imagem.carregar_imagem(caminho_imagem)

            except ValueError as erro:

                QMessageBox.warning(
                    self,
                    "Erro ao abrir imagem",
                    str(erro)
                )

                return

            # Atualiza o estado geral da interface
            self.atualizar_estado_interface()

            # Exibe a imagem na interface
            self.exibir_imagem()

            # Refaz a primeira renderização após a área ficar visível
            QTimer.singleShot(0, self.exibir_imagem)

            # Informa o sucesso da operação na barra inferior
            self.atualizar_status_imagem(
                "Imagem carregada com sucesso."
            )

    def exibir_imagem(self):
        """
        Exibe a imagem atual na interface.
        """

        # Obtém a imagem atual do gerenciador
        imagem = self.gerenciador_imagem.obter_imagem_atual()

        # cria objeto de imagem do Qt a partir do caminho da imagem carregada
        pixmap = cv2_to_qt(imagem)

        # Obtém a área disponível para exibir a imagem com boa proporção
        largura_area = max(self.area_imagem.viewport().width() - 24, 1)
        altura_area = max(self.area_imagem.viewport().height() - 24, 1)

        # Ajusta o tamanho da imagem para caber na área de exibição
        pixmap = pixmap.scaled(largura_area, altura_area, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Exibe a imagem no QLabel
        self.label_imagem.setPixmap(pixmap)

        # Mantém os indicadores da interface sincronizados
        self.atualizar_estado_interface()

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

            # Atualiza feedback visual da operação concluída
            self.atualizar_status_imagem(
                "Imagem salva com sucesso."
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

        # Atualiza o resumo da operação na interface
        self.atualizar_status_imagem(
            "Imagem restaurada para a versão original."
        )

    def resizeEvent(self, event):
        """
        Reexibe a imagem ao redimensionar a janela.
        """

        super().resizeEvent(event)

        # Redesenha a imagem para aproveitar a nova área disponível
        if self.gerenciador_imagem.imagem_atual is not None:
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
        self.salvar_estado_antes_edicao()
        imagem_negativa = aplicar_negativo(imagem)

        # Atualiza a imagem atual no gerenciador
        self.gerenciador_imagem.imagem_atual = imagem_negativa

        # Exibe a imagem modificada na interface
        self.exibir_imagem()

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            "Efeito negativo aplicado."
        )

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

        # Salva estado anterior antes de alterar os offsets acumulados
        self.salvar_estado_antes_edicao()
        
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

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            f"Brilho ajustado em {self.gerenciador_imagem.offset_brilho}."
        )

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

        # Salva estado anterior antes de alterar os offsets acumulados
        self.salvar_estado_antes_edicao()
        
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

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            f"Contraste acumulado em {self.gerenciador_imagem.offset_contraste}."
        )

    def aplicar_expansao_contraste(self):
        """
        Aplica expansão linear de contraste.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        self.salvar_estado_antes_edicao()

        imagem_transformada = expansao_contraste(
            imagem
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            "Expansão de contraste aplicada."
        )

    def aplicar_transformacao_logaritmica(self):
        """
        Aplica transformação logarítmica.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        self.salvar_estado_antes_edicao()

        imagem_transformada = (
            transformacao_logaritmica(imagem)
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            "Transformação logarítmica aplicada."
        )

    def aplicar_transformacao_exponencial(self):
        """
        Aplica transformação exponencial.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        self.salvar_estado_antes_edicao()

        imagem_transformada = (
            transformacao_exponencial(imagem)
        )

        self.gerenciador_imagem.imagem_atual = (
            imagem_transformada
        )

        self.exibir_imagem()

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            "Transformação exponencial aplicada."
        )

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

        # Atualiza mensagem de operação concluída
        self.atualizar_status_imagem(
            "Histograma exibido."
        )

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

            self.salvar_estado_antes_edicao()

            imagem_equalizada = (
                equalizar_histograma(imagem)
            )

            self.gerenciador_imagem.imagem_atual = (
                imagem_equalizada
            )

            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                "Equalização de histograma aplicada."
            )

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

            # Salva estado anterior antes do redimensionamento
            self.salvar_estado_antes_edicao()

            # Redimensiona imagem
            imagem_redimensionada = (redimensionar_vizinho_mais_proximo(imagem,nova_largura,nova_altura))

            # Atualiza imagem atual
            self.gerenciador_imagem.imagem_atual = (imagem_redimensionada)

            # Atualiza interface
            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                f"Imagem redimensionada para {nova_largura} x {nova_altura} com vizinho mais próximo."
            )

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

            # Salva estado anterior antes do redimensionamento
            self.salvar_estado_antes_edicao()

            # Redimensiona imagem
            imagem_redimensionada = (redimensionar_bilinear(imagem,nova_largura,nova_altura))

            # Atualiza imagem atual
            self.gerenciador_imagem.imagem_atual = (imagem_redimensionada)

            # Atualiza interface
            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                f"Imagem redimensionada para {nova_largura} x {nova_altura} com interpolação bilinear."
            )

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

            self.salvar_estado_antes_edicao()

            imagem_filtrada = aplicar_sobel(imagem)

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                "Filtro Sobel aplicado."
            )

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

            self.salvar_estado_antes_edicao()

            imagem_filtrada = aplicar_laplaciano(imagem)

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                "Filtro Laplaciano aplicado."
            )

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

                self.salvar_estado_antes_edicao()

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

                # Atualiza mensagem de operação concluída
                self.atualizar_status_imagem(
                    f"Filtro Box aplicado com kernel {tamanho}."
                )

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

            self.salvar_estado_antes_edicao()

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

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                f"Filtro Gaussiano aplicado com kernel {tamanho} e sigma {sigma}."
            )

    def aplicar_mediana(self):
        """
        Aplica filtro de mediana com tamanho de kernel definido pelo usuário.
        """

        imagem = self.gerenciador_imagem.obter_imagem_atual()

        if imagem is None:
            return

        dialog = DialogMediana()

        if not dialog.exec_():
            return

        tamanho_kernel = dialog.obter_parametros()

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

            self.salvar_estado_antes_edicao()

            imagem_filtrada = aplicar_mediana(
                imagem,
                tamanho_kernel=tamanho_kernel,
                padding=self.tipo_padding
            )

            self.gerenciador_imagem.imagem_atual = (imagem_filtrada)

            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                f"Filtro Mediana aplicado com kernel {tamanho_kernel}."
            )

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

        # Mostra cursor de espera durante o processamento
        QApplication.setOverrideCursor(
            Qt.WaitCursor
        )

        try:

            self.salvar_estado_antes_edicao()

            resultado = aplicar_agucamento_laplaciano(
                imagem
            )

            self.gerenciador_imagem.imagem_atual = (
                resultado
            )

            self.exibir_imagem()

            # Atualiza mensagem de operação concluída
            self.atualizar_status_imagem(
                "Aguçamento laplaciano aplicado."
            )

        finally:

            QApplication.restoreOverrideCursor()
