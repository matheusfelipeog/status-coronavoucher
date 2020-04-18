# -*- coding: utf-8 -*-

# @author: Matheus Felipe <github.com/matheusfelipeog>

import requests
import json


class Coronavoucher(object):
    """Classe para obter o status da situação atual do auxílio emergencial.

    Metódos públicos:

    >>> show_data(...)  # Mostre os dados parcial.

    >>> show_all_data(...)  # Mostre os dados completos.

    >>> get_data(...)  # Obtenha os dados puros.

    Metódos internos:

    >>>  _request_a_new_sms_token(...)  # Solicite um novo código sms.

    >>>  _data_verification(...)  # Verifique se os dados estão válidos

    >>>  _get_msg_error(...)  # Pegue a mensagem de erro com base nos dados.
    """
    
    def __init__(self, cpf: str, sms_token: str, session: requests.Session=None):
        """
        @cpf `str` -> Corresponde aos 11 digitos do CPF do indivíduo, no formato: 00000000000

        @sms_token `str` -> Corresponde aos 6 digitos do token que é enviado para seu celular via sms
        
        @session `Session` -> Corresponde a instância de Session para manipulação HTTP
        """

        # Criação da sessão para manipular o protocolo HTTP
        if not isinstance(session, requests.Session):
            self._session = requests.Session()
        else:
            self._session = session

        self.cpf = str(cpf)
        self.sms_token = str(sms_token)

        self._url = 'https://auxilio.caixa.gov.br/api/cadastro/validarLogin/{}'.format(self.cpf)

        self._payload = {
            "token": self.sms_token
            }
        self._headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
            "authority": "auxilio.caixa.gov.br",
            "method": "PUT",
            "path": "/api/cadastro/validarLogin/",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-length": "18",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://auxilio.caixa.gov.br",
            "referer": "https://auxilio.caixa.gov.br/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

    def __repr__(self):
        return f'Coronavoucher(cpf=<{self.cpf}>, sms_token=<{self.sms_token}>, session={self._session})'

    def __str__(self):
        return self.__repr__()
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._session.close()

    def _request_a_new_sms_token(self) -> dict:
        """Solicitar um novo token sms para validação."""
        temp_url = 'https://auxilio.caixa.gov.br/api/sms/validarLogin'

        temp_payload = {"cpf": int(self.cpf)}

        # Cópia temporária do headers, alterando o path e o method
        temp_headers = self._headers.copy()
        temp_headers["path"] = '/api/sms/validarLogin'
        temp_headers["method"] = 'POST'

        response = self._session.post(
                temp_url,
                data=json.dumps(temp_payload),
                headers=temp_headers,
                verify=True
            )

        return response.json()

    def _data_verification(self, data: dict) -> dict:
        """Verifica se existiu um erro retornado pelo server.
        
        @data `dict` -> Dados do coronavoucher em formato dict.

        @return `str` ->  Nova estrutura com http code.
        """

        http_code = data.get('codigo', 200)  # Se não existe a chave "codigo" retorna 200

        if http_code == 200:
            # Dados válidos, contendo todas as informações do coronavoucher
            return {"http_code": http_code, "data": data}

        else:  # Erro retornado pelo server
            return {"http_code": data.get('codigo'), "data": data}

    def _get_msg_error(self, data: dict) -> str:
        """Cria uma mensagem de erro para ser exibida.
        
        @data `dict` -> Dados do coronavoucher em formato dict.

        @return `str` ->  Mensagem de erro com base no http code.
        """

        cod_error = data['http_code']

        msg_error = ''
        if int(cod_error) == 401:  # Token SMS inválido ou expirado
            msg_error =  f'\n[Erro]: {data["data"]["mensagem"]}\n'

        elif int(cod_error) == 404:  # CPF Incorreto ou inválido
            msg_error =  f'\n[Erro]: {data["data"]["mensagem"]}\n'

        else:
            msg_error = '\nOcorreu um erro, tente novamente...\n'

        return msg_error
        
    def get_data(self) -> dict:
        """Pega os dados do coronavoucher.
        
        @return `dict` -> Retorna um dicionário com todas as informações.
        """

        response = self._session.put(
                self._url,
                data=json.dumps(self._payload),
                headers=self._headers,
                verify=True
            )
        return response.json()

    def show_data(self) -> str:
        """Mostrar Nome, CPF e Situação do coronavoucher.
        
        @return `str` -> Retorna um template simples para ser printado com as informações.
        """
        response = self._data_verification(self.get_data())

        template = ''
        if response.get('http_code') == 200:

            status = response.get('data')

            template = f'\nNome: {status["noPessoa"]}\nCPF: {status["cpf"]}\nStatus: {status["situacao"]}\n'

        else:
            template = self._get_msg_error(response)

            if response.get('http_code') == 401:
                template += '[Erro]: Solicitando um novo código, aguarde...\n'
                new_sms_token = self._request_a_new_sms_token()
                template += f'[Erro]: {new_sms_token["mensagem"]}.\n'

        return template

    def show_all_data(self) -> str:
        """Mostrar todas os dados do status do coronavoucher.
        
        @return `str` -> Retorna um template para ser printado com as informações. 
        """
        response = self._data_verification(self.get_data())

        template = ''
        if response.get('http_code') == 200:

            all_data = response.get('data')

            template = f'\nNome: {all_data["noPessoa"]}\nCPF: {all_data["cpf"]}\nSexo: {all_data["sexo"]}'
            template += f'\nBanco: {all_data["banco"]}\nBolsa Familia: {all_data["bolsa_familia"]}'
            template += f'\nMotivo: {all_data["motivo"]}\nNº Situação Cadastral: {all_data["nuSituacaoCadastro"]}'
            template += f'\nData e Hora de Cadastro: {all_data["dhFinalizacaoCadastro"]}'
            template += f'\nStatus Atual: {all_data["situacao"]}\n'

        else:
            template = self._get_msg_error(response)

            if response.get('http_code') == 401:
                template += '[Erro]: Solicitando um novo código, aguarde...\n'
                new_sms_token = self._request_a_new_sms_token()
                template += f'[Erro]: {new_sms_token["mensagem"]}.\n'

        return template
