from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QHBoxLayout,
    QFrame
)


class DialogBox(QDialog):
    """
    Janela de diálogo para solicitar
    o tamanho do kernel Box.
    """

    def __init__(self):
        super().__init__()

        # Configurações gerais da janela
        self.setWindowTitle(
            "Box Personalizado"
        )
        self.setModal(True)
        self.setMinimumWidth(360)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Bloco visual de orientação do diálogo
        painel = QFrame()
        painel.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 12px;"
        )

        layout_painel = QVBoxLayout()
        layout_painel.setContentsMargins(16, 16, 16, 16)
        layout_painel.setSpacing(10)

        titulo = QLabel("Configurar Filtro Box")
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #111827;"
        )

        descricao = QLabel(
            "Escolha um tamanho ímpar para o kernel de suavização."
        )
        descricao.setWordWrap(True)
        descricao.setStyleSheet(
            "font-size: 12px; color: #6b7280;"
        )

        # Campo de tamanho do kernel
        label_kernel = QLabel("Tamanho do Kernel:")

        self.spin_kernel = QSpinBox()

        # O kernel deve ser ímpar para manter um centro definido
        self.spin_kernel.setRange(3, 99)
        self.spin_kernel.setSingleStep(2)
        self.spin_kernel.setValue(5)
        self.spin_kernel.setSuffix(" px")

        layout_painel.addWidget(titulo)
        layout_painel.addWidget(descricao)
        layout_painel.addWidget(label_kernel)
        layout_painel.addWidget(self.spin_kernel)
        painel.setLayout(layout_painel)

        layout.addWidget(painel)

        # Botões de confirmação e cancelamento
        botoes = QHBoxLayout()
        botoes.setSpacing(10)

        btn_ok = QPushButton("OK")
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet(
            "background-color: #ffffff;"
            "color: #1f2937;"
            "border: 1px solid #d1d5db;"
        )

        btn_ok.clicked.connect(
            self.accept
        )

        btn_cancelar.clicked.connect(
            self.reject
        )

        botoes.addWidget(btn_ok)
        botoes.addWidget(btn_cancelar)

        layout.addLayout(botoes)

        self.setLayout(layout)

    def obter_parametros(self):
        """
        Retorna o tamanho do kernel escolhido.
        """

        return self.spin_kernel.value()
