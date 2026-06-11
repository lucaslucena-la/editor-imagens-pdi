"""
Arquivo principal da aplicação.

Responsável por iniciar o sistema,
criar a aplicação PyQt5 e abrir
a janela principal.
"""

import sys

from PyQt5.QtWidgets import QApplication

from ui.janela_principal import JanelaPrincipal


# Estilo visual global da aplicação
ESTILO_APLICACAO = """
QMainWindow {
    background-color: #ffffff;
}

QMenuBar {
    background-color: #ffffff;
    color: #1f2937;
    border-bottom: 1px solid #d1d5db;
}

QMenuBar::item {
    spacing: 8px;
    padding: 8px 12px;
    background: transparent;
}

QMenuBar::item:selected {
    background: #f3f4f6;
    border-radius: 6px;
}

QMenu {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    padding: 6px;
}

QMenu::item {
    padding: 8px 24px 8px 12px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: #e5e7eb;
}

QToolBar {
    background-color: #ffffff;
    border: none;
    border-bottom: 1px solid #d1d5db;
    spacing: 6px;
    padding: 8px;
}

QToolButton {
    background-color: #f9fafb;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px 12px;
}

QToolButton:hover {
    background-color: #f3f4f6;
}

QToolButton:pressed {
    background-color: #e5e7eb;
}

QToolButton:disabled {
    color: #9ca3af;
    background-color: #f3f4f6;
    border-color: #e5e7eb;
}

QStatusBar {
    background-color: #ffffff;
    color: #4b5563;
    border-top: 1px solid #d1d5db;
}

QLabel {
    color: #1f2937;
}

QScrollArea {
    border: none;
}

QPushButton {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #f3f4f6;
}

QPushButton:pressed {
    background-color: #e5e7eb;
}

QPushButton:disabled {
    background-color: #f3f4f6;
    color: #9ca3af;
    border-color: #e5e7eb;
}

QLineEdit,
QSpinBox,
QDoubleSpinBox {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px 10px;
}

QLineEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {
    border: 1px solid #9ca3af;
}

QDialog {
    background-color: #ffffff;
}

QMessageBox {
    background-color: #ffffff;
}
"""

def main():
    """
    Função principal da aplicação.
    """

    # Cria a aplicação PyQt5
    app = QApplication(sys.argv)

    # Aplica identidade visual global
    app.setStyleSheet(ESTILO_APLICACAO)

    # Cria a janela principal
    janela = JanelaPrincipal()

    # Exibe a janela principal
    janela.show()

    # Inicia o loop de eventos da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
