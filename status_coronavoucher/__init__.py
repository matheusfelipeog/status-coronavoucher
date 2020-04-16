# -*- coding: utf-8 -*-

# @author: Matheus Felipe <github.com/matheusfelipeog>

import requests
import json


class Coronavoucher(object):
    """Classe para obter o status da situação atual do auxílio emergencial."""
    
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

    def get_status(self) -> dict:
        """Pega o status do coronavoucher.
        
        @return `dict` -> Retorna um dicionário com todas as informações.
        """

        response = self._session.put(
                self._url,
                data=json.dumps(self._payload),
                headers=self._headers,
                verify=True
            )
        return response.json()

    def show_status(self) -> str:
        """Mostrar Nome, CPF e Situação do coronavoucher.
        
        @return `str`-> Retorna um template simples para ser printado com as informações.
        """
        status = self.get_status()

        template = f'\nNome: {status["noPessoa"]}\nCPF: {status["cpf"]}\nStatus: {status["situacao"]}\n'

        return template

    def show_all_infos(self) -> str:
        """Mostrar todas as informações do coronavoucher.
        
        @return `str` -> Retorna um template para ser printado com as informações. 
        """
        all_info = self.get_status()

        template = f'\nNome: {all_info["noPessoa"]}\nCPF: {all_info["cpf"]}\nSexo: {all_info["sexo"]}'
        template += f'\nBanco: {all_info["banco"]}\nBolsa Familia: {all_info["bolsa_familia"]}'
        template += f'\nMotivo: {all_info["motivo"]}\nNº Situação Cadastral: {all_info["nuSituacaoCadastro"]}'
        template += f'\nData e Hora de Cadastro: {all_info["dhFinalizacaoCadastro"]}'
        template += f'\nStatus Atual: {all_info["situacao"]}\n'

        return template
