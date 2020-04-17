# Status Coronavoucher

Visualize o status atual da sua solicitação do [auxílio emergencial](https://auxilio.caixa.gov.br/#/inicio) pelo terminal.

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

**Execute o script diretamente na linha de comando com:**
```
python main.py 12345678901 445566
```

**Retorno resumido:**
```
Nome: Fulano de Tal Uzumaki
CPF: 12345678901
Status: Aguardando
```

**Retorno completo:**
```
Nome: Fulano de Tal Uzumaki
CPF: 12345678901
Sexo: None
Banco: None
Bolsa Familia: False
Motivo: None
Nº Situação Cadastral: 5
Data e Hora de Cadastro: 2020-04-08T18:21:20.192
Status Atual: Aguardando
```

## Contribuições

Caso tenha dicas e propostas para melhorar o projeto, abra uma issue detalhando o que você propõe.

Toda contribuição é bem vinda. 

## Licença

[MIT](https://github.com/matheusfelipeog/status-coronavoucher/blob/master/LICENSE)
