"""
Janela de diálogo para redimensionamento.
"""

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)


class DialogRedimensionar(QDialog):
    """
    Janela de diálogo para solicitar
    largura e altura da imagem.
    """

    def __init__(self, largura_inicial, altura_inicial):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Redimensionar Imagem")

        # Campos de largura e altura
        self.input_largura = QLineEdit(str(largura_inicial))
        self.input_altura = QLineEdit(str(altura_inicial))

        # Labels
        label_largura = QLabel("Largura:")
        label_altura = QLabel("Altura:")

        # Botão confirmar
        botao_ok = QPushButton("OK")
        botao_ok.clicked.connect(self.accept)

        # Layout largura
        layout_largura = QHBoxLayout()
        layout_largura.addWidget(label_largura)
        layout_largura.addWidget(self.input_largura)

        # Layout altura
        layout_altura = QHBoxLayout()
        layout_altura.addWidget(label_altura)
        layout_altura.addWidget(self.input_altura)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_largura)
        layout_principal.addLayout(layout_altura)
        layout_principal.addWidget(botao_ok)

        self.setLayout(layout_principal)

    def obter_dimensoes(self):
        """
        Retorna largura e altura digitadas.
        """

        largura = int(self.input_largura.text())
        altura = int(self.input_altura.text())

        return largura, altura