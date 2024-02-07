# Projeto CRUD Bancário

Este projeto é uma aplicação web simples que realiza operações de CRUD (Create, Read, Update, Delete) em um banco de dados de usuários.

## Tecnologias Utilizadas

- Flask
- Marshmallow
- SQLite

## Funcionalidades

1. **Adicionar Usuário**: Cria um novo usuário com nome completo, CPF, email e saldo. A rota é `/user/add` e o método é POST.
2. **Obter Usuários**: Retorna todos os usuários registrados. A rota é `/user/request` e o método é GET.
3. **Obter Usuário por ID**: Retorna um usuário específico com base no ID fornecido. A rota é `/user/request/<id>` e o método é GET.
4. **Atualizar Usuário**: Atualiza os detalhes de um usuário existente. A rota é `/user/update` e o método é PUT.
5. **Deletar Usuário**: Deleta um usuário específico com base no ID fornecido. A rota é `/user/delete/<id>` e o método é DELETE.
6. **Criar Transação**: Cria uma transação entre dois usuários. A rota é `/transaction` e o método é POST.

## Como Executar

1. Clone este repositório.
2. Execute o arquivo principal com `python app.py`.
3. Acesse a aplicação em `localhost:5000`.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
