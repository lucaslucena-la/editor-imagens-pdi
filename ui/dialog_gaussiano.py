from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QHBoxLayout
)


class DialogGaussiano(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Gaussiano Personalizado"
        )

        layout = QVBoxLayout()

        # Kernel
        layout.addWidget(
            QLabel("Tamanho do Kernel:")
        )

        self.spin_kernel = QSpinBox()

        self.spin_kernel.setRange(3, 99)
        self.spin_kernel.setSingleStep(2)
        self.spin_kernel.setValue(5)

        layout.addWidget(
            self.spin_kernel
        )

        # Sigma
        layout.addWidget(
            QLabel("Sigma (σ):")
        )

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

        layout.addWidget(
            self.spin_sigma
        )

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

        return (
            self.spin_kernel.value(),
            self.spin_sigma.value()
        )