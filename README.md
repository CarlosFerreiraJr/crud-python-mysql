
# 🐍 CRUD de Produtos com Python e MySQL

Sistema de gerenciamento de produtos desenvolvido em Python,
utilizando banco de dados MySQL e interface via terminal.

## 🚀 Funcionalidades

- Cadastrar produtos (CREATE)
- Consultar produtos (READ)
- Alterar produtos (UPDATE)
- Excluir produtos (DELETE)
- Validação de dados informados pelo usuário
- Confirmação antes da exclusão
- Tratamento de exceções
- Gerenciamento de conexão com MySQL

## 🛠️ Tecnologias utilizadas

- Python
- MySQL
- MySQL Connector/Python
- Python-dotenv
- Git e GitHub
- VS Code
- WSL 2 / Ubuntu

## 📁 Estrutura do projeto

```text
conexao_bd_mysql/
├── conexao.py
├── produtos.py
├── menu.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/crud-python-mysql.git
cd crud-python-mysql
```

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` utilizando `.env.example`
como referência.

Crie no MySQL um banco de dados e a tabela `produtos`
com os campos esperados pelo projeto.

## ▶️ Executando

```bash
python menu.py
```

## 🔐 Segurança

As credenciais do banco de dados são armazenadas
em variáveis de ambiente, utilizando o arquivo `.env`,
que não é versionado no Git.

## 📚 Objetivo

Projeto desenvolvido para praticar operações CRUD,
integração Python com MySQL, organização de código,
tratamento de erros e versionamento com Git.

## 👨‍💻 Autor

Carlos Alberto Ferreira Júnior

GitHub: https://github.com/CarlosFerreiraJr
