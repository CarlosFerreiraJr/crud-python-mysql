from decimal import Decimal, InvalidOperation
from mysql.connector import Error
from conexao import conectar, desconectar

#============================================================
# Descrição:
#     Consulta todos os produtos cadastrados na tabela
#     produtos do banco de dados MySQL.

#     Exibe as informações de cada produto no terminal.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def consultar_produtos():
    conexao = conectar()

    if conexao is None:
        return

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        if not produtos:
            print("\nNenhum produto encontrado.")
            return

        print("\n===== LISTA DE PRODUTOS =====")

        for produto in produtos:
            print(f"ID: {produto['id_produto']}")
            print(f"Nome: {produto['nome_produto']}")
            print(f"QR Code: {produto['id_qrcode']}")
            print(f"Descrição Técnica: {produto['descricao_tecnica']}")
            print(f"Status: {produto['status_produto']}")
            print(f"Imagem: {produto['nome_imagem']}")
            print(f"Tipo de Produto: {produto['tipo_produto']}")
            print(f"Local de Instalação: {produto['local_instalacao']}")
            print(f"Tipo de Gás: {produto['tipo_gas']}")
            print(f"Situação: {produto['situacao_produto']}")
            print("-" * 50)

    except Exception as erro:
        print(f"\nErro ao consultar produtos: {erro}")

    finally:
        if cursor is not None:
            cursor.close()

        desconectar(conexao)


#============================================================
# Descrição:
#     Solicita os dados de um novo produto ao usuário
#     e realiza o cadastro na tabela produtos do MySQL.

#     Valida os campos obrigatórios e os valores
#     permitidos para status e tipo de produto.

# Parâmetros:
#     Nenhum.

# Retorno:
#     Nenhum.
#============================================================
def cadastrar_produto():
    print("\n===== CADASTRO DE PRODUTOS =====")

    nome = input("Nome do produto: ").strip()
    qrcode = input("Identificação QR Code: ").strip()
    descricao = input("Descrição técnica: ").strip()
    imagem = input("Nome da imagem: ").strip()
    local = input("Local de instalação: ").strip()
    gas = input("Tipo de gás: ").strip()
    situacao = input("Situação do produto: ").strip()

    if not nome or not qrcode:
        print("\nNome e QR Code são obrigatórios!")
        return

    status = input("Status [ATIVO/INATIVO] (padrão ATIVO): ").strip().upper()
    tipo = input("Tipo [VENDA/CONSULTA] (padrão VENDA): ").strip().upper()

    status = status or "ATIVO"
    tipo = tipo or "VENDA"

    if status not in ("ATIVO", "INATIVO"):
        print("\nStatus inválido!")
        return

    if tipo not in ("VENDA", "CONSULTA"):
        print("\nTipo de produto inválido!")
        return

    conexao = conectar()

    if conexao is None:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        sql = """
            INSERT INTO produtos (
                nome_produto,
                id_qrcode,
                descricao_tecnica,
                status_produto,
                nome_imagem,
                tipo_produto,
                local_instalacao,
                tipo_gas,
                situacao_produto
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome,
            qrcode,
            descricao or None,
            status,
            imagem or None,
            tipo,
            local or None,
            gas or None,
            situacao or None
        )

        cursor.execute(sql, valores)
        conexao.commit()

        print("\nProduto cadastrado com sucesso!")
        print(f"ID do produto: {cursor.lastrowid}")

    except Error as erro:
        conexao.rollback()
        print(f"\nErro ao cadastrar produto: {erro}")

    finally:
        if cursor is not None:
            cursor.close()

        desconectar(conexao)


#===========================================================
# Função: alterar_produto()
#
# Descrição:
#     Permite alterar os dados de um produto cadastrado
#     no banco de dados MySQL.
#     Os campos não informados permanecem inalterados.
#
# Parâmetros:
#     Nenhum.
#
# Retorno:
#     Nenhum.
#===========================================================
def alterar_produto():

    print("\n===== ALTERAÇÃO DE PRODUTOS =====")

    # Solicita o ID do produto
    try:
        id_produto = int(input("Informe o ID do produto: "))

        if id_produto <= 0:
            print("\nID inválido!")
            return

    except ValueError:
        print("\nO ID deve ser um número inteiro!")
        return

    # Estabelece a conexão com o MySQL
    conexao = conectar()

    if conexao is None:
        return

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        # Consulta o produto pelo ID informado
        sql = "SELECT * FROM produtos WHERE id_produto = %s"
        cursor.execute(sql, (id_produto,))

        produto = cursor.fetchone()

        # Verifica se o produto existe
        if produto is None:
            print("\nProduto não encontrado!")
            return

        print(f"\nProduto encontrado: {produto['nome_produto']}")
        print("\nInforme os novos valores.")
        print("Pressione ENTER para manter o valor atual.\n")

        # Campos que podem ser alterados
        campos = {
            "nome_produto": "Nome",
            "id_qrcode": "QR Code",
            "descricao_tecnica": "Descrição técnica",
            "status_produto": "Status",
            "nome_imagem": "Imagem",
            "tipo_produto": "Tipo de produto",
            "local_instalacao": "Local de instalação",
            "tipo_gas": "Tipo de gás",
            "situacao_produto": "Situação"
        }

        alteracoes = {}

        # Solicita os novos valores dos campos
        for campo, descricao in campos.items():

            valor_atual = produto[campo]

            novo_valor = input(
                f"{descricao} [{valor_atual or 'Não informado'}]: "
            ).strip()

            # ENTER mantém o valor atual
            if not novo_valor:
                continue

            # Valida os campos ENUM
            if campo in ("status_produto", "tipo_produto"):
                novo_valor = novo_valor.upper()

                opcoes = (
                    ("ATIVO", "INATIVO")
                    if campo == "status_produto"
                    else ("VENDA", "CONSULTA")
                )

                if novo_valor not in opcoes:
                    print(f"\nValor inválido para {descricao}!")
                    return

            # Armazena apenas os campos alterados
            if novo_valor != valor_atual:
                alteracoes[campo] = novo_valor

        # Verifica se houve alguma alteração
        if not alteracoes:
            print("\nNenhuma alteração realizada.")
            return

        # Monta o comando UPDATE dinamicamente
        colunas = ", ".join(
            f"{campo} = %s" for campo in alteracoes
        )

        sql = f"""
            UPDATE produtos
            SET {colunas}
            WHERE id_produto = %s
        """

        # Organiza os parâmetros da consulta
        valores = tuple(alteracoes.values()) + (id_produto,)

        # Executa o UPDATE
        cursor.execute(sql, valores)

        # Confirma as alterações
        conexao.commit()

        print("\nProduto alterado com sucesso!")

    except Error as erro:
        # Desfaz a transação em caso de erro
        conexao.rollback()
        print(f"\nErro ao alterar produto: {erro}")

    finally:
        # Encerra o cursor
        if cursor is not None:
            cursor.close()

        # Encerra a conexão
        desconectar(conexao)


#===========================================================
# Função: excluir_produto()
#
# Descrição:
#     Exclui um produto cadastrado no banco de dados MySQL,
#     utilizando o ID informado pelo usuário.
#     Antes da exclusão, apresenta os dados do produto
#     e solicita uma confirmação.
#
# Parâmetros:
#     Nenhum.
#
# Retorno:
#     Nenhum.
#===========================================================
def excluir_produto():

    print("\n===== EXCLUSÃO DE PRODUTOS =====")

    # Solicita o ID do produto
    try:
        id_produto = int(input("Informe o ID do produto: "))

        if id_produto <= 0:
            print("\nID inválido!")
            return

    except ValueError:
        print("\nO ID deve ser um número inteiro!")
        return

    # Estabelece a conexão com o MySQL
    conexao = conectar()

    if conexao is None:
        return

    cursor = None

    try:
        # Cria o cursor retornando dicionários
        cursor = conexao.cursor(dictionary=True)

        # Consulta o produto antes de excluir
        sql = """
            SELECT *
            FROM produtos
            WHERE id_produto = %s
        """

        cursor.execute(sql, (id_produto,))

        # Recupera o produto encontrado
        produto = cursor.fetchone()

        # Verifica se o produto existe
        if produto is None:
            print("\nProduto não encontrado!")
            return

        # Exibe os dados para conferência
        print("\n===== PRODUTO ENCONTRADO =====")
        print(f"ID: {produto['id_produto']}")
        print(f"Nome: {produto['nome_produto']}")
        print(f"QR Code: {produto['id_qrcode']}")
        print(f"Status: {produto['status_produto']}")
        print(f"Tipo: {produto['tipo_produto']}")
        print(f"Local: {produto['local_instalacao']}")
        print("-" * 40)

        # Solicita confirmação antes da exclusão
        confirmacao = input(
            "\nDeseja realmente excluir este produto? "
            "[S/N]: "
        ).strip().upper()

        # Cancela a exclusão caso não seja confirmada
        if confirmacao != "S":
            print("\nExclusão cancelada pelo usuário.")
            return

        # Executa o comando DELETE
        sql = """
            DELETE FROM produtos
            WHERE id_produto = %s
        """

        cursor.execute(sql, (id_produto,))

        # Verifica se algum registro foi excluído
        if cursor.rowcount == 0:
            print("\nNenhum produto foi excluído.")
            conexao.rollback()
            return

        # Confirma a exclusão no banco
        conexao.commit()

        print("\nProduto excluído com sucesso!")

    except Error as erro:
        # Desfaz a transação em caso de erro
        conexao.rollback()

        print(f"\nErro ao excluir produto: {erro}")

    finally:
        # Fecha o cursor
        if cursor is not None:
            cursor.close()

        # Encerra a conexão com o MySQL
        desconectar(conexao)
