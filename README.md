# Status Coronavoucher

Visualize o status atual da sua solicitação do [auxílio emergencial](https://auxilio.caixa.gov.br/#/inicio) pelo terminal.

> OBS: Este projeto não é uma implementação da Caixa e tampouco com apoio da mesma.


## ⚠ Atenção

**Este script não funciona mais.**

Nas antigas versões do sistema de registro/consulta do auxílio emergencial da Caixa, o sistema *Captcha* não tinha sido implementado corretamente, possibilitando a utilização de scripts automatizados para realizar consultas diretamente ao servidor, somente com os dados já cadastrados sendo enviados, sem nenhuma especie de bloqueio. Contudo, recentemente (junho/2020), ocorreu uma atualização corrigindo essa má implementação, assim **impossibilitando este script de funcionar corretamente.**

## 💡 Objetivo

Fiz este projeto para facilitar na consulta do status do coronavoucher e botar meus conhecimentos em prática.

A consulta é feita diretamente no servidor da caixa, assim evitando: *acessar o site, preencher captcha, problemas no site.* 

### Isto servirá para você se:

- Quer consultar o status mais rápido;
- Quer integrar em alguma aplicação que desenvolveu;
- Teve problemas consultando diretamente pelo site.

## ⚙️ Instalação

O projeto é contruído em `Python 3.x`, então é necessário ter instalado em sua maquína. [[clique aqui para baixar]](https://www.python.org/downloads/)

Após a instalação do Python, faça o download do repositório ou clone o repositório com:
```git
$ git clone https://github.com/matheusfelipeog/status-coronavoucher.git
```
Em seguida, entre no repositório com `cd ./status-coronavoucher` e instale o módulo `requests` com o pip:
```
$ pip install requests
```

## 💻 Uso

O programa possuí uma interface de linha de comando, assim facilitando ainda mais a consulta.

**Para utilização básica, use:**
```
$ python cli.py 12345678910 "Fulano de Tal Uzumaki" 1997-10-10 "Fulana Uzumaki de Tal"
```

**Para mais, veja a ajuda:**
```
$ python cli.py -h

usage: python cli.py [-h] cpf nome nasc mae desc [options]

Consulte a situação atual do auxílio emergencial.

positional arguments:
  CPF                   os 11 digitos do CPF, sem espaço ou caracteres
                        especiais.
  NOME                  O nome informado na hora do cadastro no sitema.
  NASC                  A data de nascimento no formato AA-MM-DD (Ano-Mês-
                        Dia).
  MAE                   Nome da mãe do solicitante do auxílio.

optional arguments:
  -h, --help            show this help message and exit
  -desc desc, --desconhecida desc
                        Informe se a mãe é desconhecida com True. False é o
                        padrão
  -f format, --format format
                        formato de retorno -> [simple, complete, raw]
```

### Formatos de retorno:

`simple`:
```
Nome: Fulano de Tal Uzumaki
CPF: 12345678901
Status: Aguardando
```

`complete`:
```
Nome: Fulano de Tal Uzumaki
CPF: 12345678901
Sexo: None
Banco: None
Bolsa Familia: False
Nº Situação Cadastral: 5
Data e Hora de Cadastro: 4/08/2020 21:20.192 PM
Status Atual: Aguardando
Motivo: None
Valor Benefício: None
DE Situação Crédito: None
DT Situação Crédito: None
```

`raw`:
```python
{
  'sexo': None,
  'situacao': 'Aguardando',
  'banco': None,
  'motivo': None,
  'bolsa_familia': False,
  'cpf': 12345678901,
  'noPessoa': 'Fulano de Tal Uzumaki',
  'nuSituacaoCadastro': 5,
  'dhFinalizacaoCadastro': '2020-04-08T18:21:20.192'
  'dt_situacao_credito': None,
  'de_situacao_credito': None,
  'vr_beneficio': None
 }
```

## 🤝 Contribuições

Caso tenha dicas e propostas para melhorar o projeto, abra uma issue detalhando o que você propõe.

Toda contribuição é bem vinda. 

## 📜 Licença

Este projeto está sobre a licença [MIT](https://github.com/matheusfelipeog/status-coronavoucher/blob/master/LICENSE).
