from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QHBoxLayout,
    QFrame
)


class DialogGaussiano(QDialog):

    def __init__(self):
        super().__init__()

        # Configurações gerais da janela
        self.setWindowTitle(
            "Gaussiano Personalizado"
        )
        self.setModal(True)
        self.setMinimumWidth(380)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Painel visual com título e descrição do filtro
        painel = QFrame()
        painel.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #d1d5db;"
            "border-radius: 12px;"
        )

        layout_painel = QVBoxLayout()
        layout_painel.setContentsMargins(16, 16, 16, 16)
        layout_painel.setSpacing(10)

        titulo = QLabel("Configurar Filtro Gaussiano")
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #111827;"
        )

        descricao = QLabel(
            "Defina o tamanho do kernel e a intensidade do desfoque gaussiano."
        )
        descricao.setWordWrap(True)
        descricao.setStyleSheet(
            "font-size: 12px; color: #6b7280;"
        )

        # Kernel
        label_kernel = QLabel("Tamanho do Kernel:")

        self.spin_kernel = QSpinBox()

        self.spin_kernel.setRange(3, 99)
        self.spin_kernel.setSingleStep(2)
        self.spin_kernel.setValue(5)
        self.spin_kernel.setSuffix(" px")

        # Sigma
        label_sigma = QLabel("Sigma (σ):")

        self.spin_sigma = QDoubleSpinBox()

        self.spin_sigma.setRange(
            0.1,
            100
        )

        self.spin_sigma.setValue(
            1.0
        )

        self.spin_sigma.setSingleStep(
            0.1
        )
        self.spin_sigma.setDecimals(1)

        layout_painel.addWidget(titulo)
        layout_painel.addWidget(descricao)
        layout_painel.addWidget(label_kernel)
        layout_painel.addWidget(self.spin_kernel)
        layout_painel.addWidget(label_sigma)
        layout_painel.addWidget(self.spin_sigma)
        painel.setLayout(layout_painel)

        layout.addWidget(painel)

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

        return (
            self.spin_kernel.value(),
            self.spin_sigma.value()
        )
