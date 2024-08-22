# Rastreador_cripto

Projeto de rastreamento automatizado do BitCoin e envio de e-mail com atualização do valor.


## Descrição

Este projeto é um programa com as seguintes funcionalidades:
- **Recebe um valor de referência do usuário para monitorar o preço do Bitcoin em R$**
- **Recebe um e-mail informado pelo usuário para enviar as atualizações**
- **Realiza a consulta em tempo real do Bitcoin na API https://coinlayer.com/**
- **Faz a análise dos dados e caso o valor do Bitcoin esteja abaixo do informado, envia um e-mail com a atualização**
- **Programa agendado para rodar de 10 em 10 minutos**

## Requisitos

- Python 3.7 ou superior

## Instalação

1. **Clone este repositório:**

    ```bash
    git clone https://github.com/cadumrod/rastreador_cripto
    cd rastreador_cripto
    ```

2. **Crie e ative um ambiente virtual:**

    No Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    No macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Adicione os acessos necessários:**

    - Crie uma conta gratuita para utilizar a API em https://coinlayer.com/
    - Crie um arquivo chamado "access.env" no diretório raiz
    - Adicione suas informações no "access.env" com o seguinte formato:

        API_TOKEN=seutoken
        EMAIL_ADDRESS=seuacesso
        EMAIL_PASSWORD=suasenha

## Uso

1. Para executar o aplicativo, navegue até o diretório raiz do projeto e execute o arquivo "app.py":

    No Windows:
    ```bash
    python app.py
    ```

    No macOS/Linux:
    ```bash
    python3 app.py
    ```


## Estrutura do Projeto

- `app.py`: Arquivo principal do aplicativo.
- `config.py`: Arquivo que carrega login, senha e token para conexão com a API.
- `template_html.html`: Template utilizado para enviar o e-mail com a atualização do Bitcoin.
- `README.md`: Este arquivo de documentação.
- `requirements.txt`: Arquivo de requisitos com as dependências do projeto.
- `LICENSE`: Licença MIT.


## Autor

**Carlos Rodrigues**

- [GitHub](https://github.com/cadumrod)
- [E-mail](mailto:carlosrod.dev@gmail.com)

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.