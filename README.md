# Sistema de Comunicação Cliente-Servidor

## Visão Geral do Sistema
Este sistema é uma aplicação cliente-servidor que permite a comunicação entre clientes, incluindo o envio de mensagens e a criação de grupos. Ele suporta o registro de clientes, a troca de mensagens, o armazenamento de mensagens pendentes e a criação de grupos.

## Arquitetura do Sistema
O sistema é dividido em dois componentes principais:

- **Cliente:** Responsável por registrar os usuários, enviar e receber mensagens, e interagir com o servidor.
- **Servidor:** Responsável por gerenciar as conexões dos clientes, distribuir mensagens, gerenciar grupos e armazenar mensagens pendentes.

## Componentes do Cliente

### client.py
- `register_client()`: Registra um novo cliente no servidor.
- `connect_client()`: Conecta um cliente existente ao servidor e permite enviar/receber mensagens.
- `send_message(client_socket, src_id, dst_id, data)`: Envia uma mensagem para outro cliente.
- `receive_messages(client_socket, client_id)`: Recebe mensagens do servidor.
- `confirm_read(client_id, timestamp)`: Envia uma confirmação de leitura de mensagem ao servidor.
- `add_contact(client_id)`: Adiciona um novo contato à lista de contatos do cliente.
- `create_group(client_id)`: Cria um novo grupo com outros clientes.

### config.py
Contém as configurações do servidor, como `SERVER_HOST` e `SERVER_PORT`.

### storage.py
- `load_client_data()`: Carrega os dados do cliente armazenados localmente.
- `save_client_data(data)`: Salva os dados do cliente localmente.
- `save_client_id(client_id)`: Salva o ID do cliente localmente após o registro.
- `save_client_contacts(client_id, new_contact)`: Adiciona um novo contato à lista de contatos do cliente.
- `save_client_groups(client_id, new_group)`: Adiciona um novo grupo à lista de grupos do cliente.
- `save_message_to_history(client_id, message)`: Salva o histórico de mensagens do cliente.

## Componentes do Servidor

### server.py
- `handle_registration(client_socket)`: Registra um novo cliente no sistema.
- `send_pending_messages(client_id, client_socket)`: Envia mensagens pendentes para o cliente após a conexão.
- `handle_group_creation(data)`: Lida com a criação de novos grupos.
- `handle_client(client_socket)`: Garante a comunicação contínua com o cliente, recebendo e processando dados.
- `main()`: Função principal que inicia o servidor e aguarda conexões de clientes.

### config.py
Contém as configurações do servidor, como `HOST` e `PORT`.

### storage.py
- `generate_unique_id()`: Gera um ID único para novos clientes e grupos.
- `save_client_id(client_id)`: Armazena o ID do cliente no servidor.
- `save_group(group_data)`: Armazena os dados de um grupo criado.
- `client_exists(client_id)`: Verifica se um cliente existe.
- `save_pending_message(src_id, dst_id, timestamp, message)`: Salva uma mensagem pendente para um cliente.
- `get_pending_messages(client_id)`: Obtém as mensagens pendentes de um cliente.

## Fluxo de Funcionamento

1. **Registro:** Um cliente novo se registra enviando uma solicitação ao servidor, que gera e retorna um ID único.
2. **Conexão:** O cliente se conecta ao servidor utilizando seu ID, o que permite enviar e receber mensagens.
3. **Envio de Mensagens:** Um cliente pode enviar mensagens para outros clientes ou grupos. Se o destinatário não estiver online, a mensagem é armazenada como pendente.
4. **Recebimento de Mensagens:** As mensagens são recebidas pelo cliente e armazenadas em seu histórico local. Se aplicável, é enviada uma confirmação de leitura ao servidor.
5. **Criação de Grupos:** Um cliente pode criar grupos adicionando outros clientes como membros.

## Como Executar o Sistema

### Servidor:
- Inicie o servidor executando o script principal do servidor.
- O servidor ficará aguardando conexões dos clientes.

### Cliente:
- Execute o script principal do cliente.
- Escolha a opção de registrar ou conectar um cliente.
- Uma vez conectado, o cliente pode enviar mensagens, adicionar contatos ou criar grupos.
