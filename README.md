# Status Coronavoucher

Visualize o status atual da sua solicitação do auxílio emergencial pelo terminal durante o dia

> Este projeto não é uma implementação da Caixa e tampouco com apoio da mesma

## Objetivo

O projeto foi criado com objetivo de estudar o módulo requests e facilitar a consulta do status atual do coronavoucher. 

## Instalação

O projeto é contruído em `Python 3.x`, então é necessário ter instalado em sua maquína. [Clique aqui para baixar](https://www.python.org/downloads/)

Após a instalação do Python, clone o repositório com:
```git
git clone https://github.com/matheusfelipeog/status-coronavoucher.git
```
Em seguida, entre no repositório e instale o módulo `requests`:
```
cd ./status-coronavoucher/
pip install requests
```

## Execução

Para executar o projeto, informe seus dados no arquivo `main.py`

```python
if __name__ == '__main__':
    from status_coronavoucher import Coronavoucher

    cpf = 'CPF AQUI'  # Tudo junto, sem espaço
    sms_token = 'SMS TOKEN AQUI'  # Tudo junto, sem espaço

    with Coronavoucher(cpf, sms_token) as Cv:
        print(Cv.show_status())

```
Execute o script com:
```
python main.py
```

## Contribuições

Caso tenha dicas e propostas para melhorar o projeto, abra uma issue detalhando o que você propõe.

Toda contribuição é bem vinda. 

## Licença

[MIT](https://github.com/matheusfelipeog/status-coronavoucher/blob/master/LICENSE)
