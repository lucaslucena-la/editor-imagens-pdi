"""
Janela de diálogo para redimensionamento.
"""

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QCheckBox,
    QFrame
)


class DialogRedimensionar(QDialog):
    """
    Janela de diálogo para solicitar
    largura e altura da imagem.
    """

    def __init__(self, largura_inicial, altura_inicial):
        super().__init__()

        # Armazena proporção original para redimensionamento opcional
        self.largura_inicial = largura_inicial
        self.altura_inicial = altura_inicial
        self.atualizando_campos = False

        # Configurações da janela
        self.setWindowTitle("Redimensionar Imagem")
        self.setModal(True)
        self.setMinimumWidth(380)

        # Campos de largura e altura
        self.input_largura = QSpinBox()
        self.input_largura.setRange(1, 10000)
        self.input_largura.setValue(largura_inicial)
        self.input_largura.setSuffix(" px")

        self.input_altura = QSpinBox()
        self.input_altura.setRange(1, 10000)
        self.input_altura.setValue(altura_inicial)
        self.input_altura.setSuffix(" px")

        # Labels
        label_largura = QLabel("Largura:")
        label_altura = QLabel("Altura:")

        # Controle para preservar proporção da imagem
        self.checkbox_proporcao = QCheckBox("Manter proporção original")
        self.checkbox_proporcao.setChecked(True)

        # Botões de confirmação e cancelamento
        botao_ok = QPushButton("OK")
        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setStyleSheet(
            "background-color: #ffffff;"
            "color: #1f2937;"
            "border: 1px solid #d1d5db;"
        )

        botao_ok.clicked.connect(self.accept)
        botao_cancelar.clicked.connect(self.reject)

        # Mantém os campos sincronizados ao preservar proporção
        self.input_largura.valueChanged.connect(self.atualizar_altura_proporcional)
        self.input_altura.valueChanged.connect(self.atualizar_largura_proporcional)

        # Painel visual com instruções do redimensionamento
        painel = QFrame()
        painel.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 12px;"
        )

        layout_painel = QVBoxLayout()
        layout_painel.setContentsMargins(16, 16, 16, 16)
        layout_painel.setSpacing(10)

        titulo = QLabel("Definir novas dimensões")
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #111827;"
        )

        descricao = QLabel(
            "Informe largura e altura desejadas para gerar uma nova versão da imagem."
        )
        descricao.setWordWrap(True)
        descricao.setStyleSheet(
            "font-size: 12px; color: #6b7280;"
        )

        # Layout largura
        layout_largura = QHBoxLayout()
        layout_largura.setSpacing(10)
        layout_largura.addWidget(label_largura)
        layout_largura.addWidget(self.input_largura)

        # Layout altura
        layout_altura = QHBoxLayout()
        layout_altura.setSpacing(10)
        layout_altura.addWidget(label_altura)
        layout_altura.addWidget(self.input_altura)

        layout_painel.addWidget(titulo)
        layout_painel.addWidget(descricao)
        layout_painel.addLayout(layout_largura)
        layout_painel.addLayout(layout_altura)
        layout_painel.addWidget(self.checkbox_proporcao)
        painel.setLayout(layout_painel)

        # Layout dos botões de ação
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(10)
        layout_botoes.addWidget(botao_ok)
        layout_botoes.addWidget(botao_cancelar)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(14)
        layout_principal.addWidget(painel)
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)

    def atualizar_altura_proporcional(self, largura):
        """
        Ajusta a altura automaticamente
        conforme a largura informada.
        """

        if not self.checkbox_proporcao.isChecked() or self.atualizando_campos:
            return

        self.atualizando_campos = True

        nova_altura = max(
            1,
            round((largura * self.altura_inicial) / self.largura_inicial)
        )

        self.input_altura.setValue(nova_altura)
        self.atualizando_campos = False

    def atualizar_largura_proporcional(self, altura):
        """
        Ajusta a largura automaticamente
        conforme a altura informada.
        """

        if not self.checkbox_proporcao.isChecked() or self.atualizando_campos:
            return

        self.atualizando_campos = True

        nova_largura = max(
            1,
            round((altura * self.largura_inicial) / self.altura_inicial)
        )

        self.input_largura.setValue(nova_largura)
        self.atualizando_campos = False

    def obter_dimensoes(self):
        """
        Retorna largura e altura digitadas.
        """

        largura = self.input_largura.value()
        altura = self.input_altura.value()

        return largura, altura
