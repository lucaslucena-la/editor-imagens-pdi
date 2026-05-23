"""
Arquivo principal da aplicação.

Responsável por iniciar o sistema,
criar a aplicação PyQt5 e abrir
a janela principal.
"""

import sys

from PyQt5.QtWidgets import QApplication

from ui.janela_principal import JanelaPrincipal

def main():
    """
    Função principal da aplicação.
    """

    # Cria a aplicação PyQt5
    app = QApplication(sys.argv)

    # Cria a janela principal
    janela = JanelaPrincipal()

    # Exibe a janela principal
    janela.show()

    # Inicia o loop de eventos da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()