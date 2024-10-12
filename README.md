# Explicações do Código

## 1. Configuração do Banco de Dados

O código se conecta a um banco de dados PostgreSQL. As credenciais (usuário e senha) devem ser ajustadas de acordo com a configuração local. As chaves secretas são necessárias para o gerenciamento de sessões e autenticação JWT.

## 2. Modelo de Usuário

O modelo `Usuario` representa a tabela de usuários no banco de dados, contendo os campos `id`, `nome`, `email` e `senha`.

## 3. Funcionalidades Atendidas

### CRUD de Usuário:

- **Criar**: Adiciona um novo usuário ao banco de dados.
- **Ler**: Retorna todos os usuários ou um usuário específico pelo ID.
- **Atualizar**: Permite a atualização dos dados de um usuário existente.
- **Deletar**: Remove um usuário do banco de dados.

### Login:

Implementa autenticação com JWT. Após validação do usuário e senha, um token de acesso é gerado, permitindo ao usuário acessar áreas protegidas do aplicativo.

## Por que Python e Flask são adequados para o projeto SupGuard?

- **Facilidade de Desenvolvimento**: Python é uma linguagem acessível e popular, ideal para desenvolvimento ágil.
- **Segurança**: A utilização de hashing de senhas e JWT para autenticação fornece uma camada extra de segurança aos dados do usuário.
- **Escalabilidade**: A estrutura modular do Flask permite que o sistema evolua com o tempo, podendo ser expandido para incluir novas funcionalidades.
