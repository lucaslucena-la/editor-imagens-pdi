from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QHBoxLayout
)


class DialogBox(QDialog):
    """
    Janela de diálogo para solicitar
    o tamanho do kernel Box.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Box Personalizado"
        )

        layout = QVBoxLayout()

        # Campo de tamanho do kernel
        layout.addWidget(
            QLabel("Tamanho do Kernel:")
        )

        self.spin_kernel = QSpinBox()

        # O kernel deve ser ímpar para manter um centro definido
        self.spin_kernel.setRange(3, 99)
        self.spin_kernel.setSingleStep(2)
        self.spin_kernel.setValue(5)

        layout.addWidget(
            self.spin_kernel
        )

        # Botões de confirmação e cancelamento
        botoes = QHBoxLayout()

        btn_ok = QPushButton("OK")
        btn_cancelar = QPushButton("Cancelar")

        btn_ok.clicked.connect(
            self.accept
        )

        btn_cancelar.clicked.connect(
            self.reject
        )

        botoes.addWidget(btn_ok)
        botoes.addWidget(btn_cancelar)

        layout.addLayout(
            botoes
        )

        self.setLayout(layout)

    def obter_parametros(self):
        """
        Retorna o tamanho do kernel escolhido.
        """

        return self.spin_kernel.value()
