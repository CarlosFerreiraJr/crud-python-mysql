import os
import subprocess
import sys
import termios
import tty
from produtos import consultar_produtos, cadastrar_produto, alterar_produto, excluir_produto

#============================================================
# Descrição:
#     Interrompe temporariamente a execução do programa
#     até que o usuário pressione uma tecla.

#     No ambiente Linux/WSL, utiliza os módulos termios
#     e tty para capturar a tecla sem exigir ENTER.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def pausar_tela():
    print("\nPressione qualquer tecla para continuar...", end="", flush=True)

    fd = sys.stdin.fileno()
    configuracao_original = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, configuracao_original)

#============================================================
# Descrição:
#     Limpa o conteúdo exibido no terminal, utilizando
#     sequências de escape ANSI.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def limpar_tela():
    if os.name == "nt":
        comando = "cls"
    else:
        comando = "clear"

    subprocess.run(comando, shell=True, check=False)


#============================================================
# Descrição:
#     Exibe o menu principal do sistema de gerenciamento
#     de produtos, apresentando as operações disponíveis.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def exibir_menu():
    print("\n===== GERENCIAMENTO DE PRODUTOS =====")
    print("1 - Cadastrar produto")
    print("2 - Consultar produtos")
    print("3 - Alterar produto")
    print("4 - Excluir produto")
    print("0 - Sair")
    print("====================================")


#============================================================
# Descrição:
#     Controla o fluxo principal da aplicação.

#     Exibe o menu, recebe a opção escolhida pelo usuário
#     e executa a operação correspondente.

#     Mantém o programa em execução até que o usuário
#     selecione a opção de sair.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def main():
    while True:
        limpar_tela()
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()
            pausar_tela()
        elif opcao == "2":
            consultar_produtos()
            pausar_tela()
        elif opcao == "3":
            alterar_produto()
            pausar_tela()
        elif opcao == "4":
            excluir_produto()
            pausar_tela()
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")



if __name__ == "__main__":
    main()
