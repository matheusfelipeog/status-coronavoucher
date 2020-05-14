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
    
    def __init__(
            self,
            cpf: int,
            nome: str,
            data_nasc: str,
            nome_mae: str,
            mae_desconhecida: bool=False,
            session: requests.Session=None
        ):
        """
        @cpf `int` -> Corresponde aos 11 digitos do CPF do indivíduo, no formato: 00000000000
        
        @nome `str` -> Corresponde ao nome do solicitante do coronavoucher
        
        @data_nasc `str` -> Corresponde a data de nascimento do solicitante do coronavoucher
        
        @nome_mae `str` -> Corresponde ao nome da mãe do solicitante do coronavoucher

        @mae_desconhecida `bool` -> Para informar em casos de mãe desconhecida

        @session `Session` -> Corresponde a instância de Session para manipulação HTTP
        """

        # Criação da sessão para manipular o protocolo HTTP
        if not isinstance(session, requests.Session):
            self._session = requests.Session()
        else:
            self._session = session

        self.cpf = cpf
        self.nome = str(nome)
        self.data_nasc = str(data_nasc)
        self.nome_mae = str(nome_mae)
        self.mae_desconhecida = bool(mae_desconhecida)

        self._url = 'https://auxilio.caixa.gov.br/api/cadastro/validarLogin/'

        self._payload = {
                "nome": self.nome,
                "cpf": self.cpf,
                "dataNascimento": self.data_nasc,
                "nomeMae": self.nome_mae,
                "isMaeDesconhecida": self.mae_desconhecida
            }

        # Em caso de mãe desconhecida será removida a chave-valor
        # correspondente para envio correto do payload
        if self.mae_desconhecida:
            del self._payload['nomeMae']

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
        return f'Coronavoucher( \
            cpf=<{self.cpf}>, nome=<{self.nome}>, data_nasc=<{self.data_nasc}>, \
            nome_mae=<{self.nome_mae}>, mae_desconhecida=<{self.mae_desconhecida}>, \
            session={self._session})'

    def __str__(self):
        return self.__repr__()
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._session.close()

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
        if int(cod_error) == 404:  # CPF Incorreto ou inválido
            msg_error =  f'\n[Info]: {data["data"]["mensagem"]}\n'

        elif int(cod_error) == 415:  # Dados divergentes comparados a base de dados
            msg_error =  f'\n[Info]: {data["data"]["mensagem"]}\n'

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
            template += f'\nNº Situação Cadastral: {all_data["nuSituacaoCadastro"]}'
            template += f'\nData e Hora de Cadastro: {all_data["dhFinalizacaoCadastro"]}'
            template += f'\nStatus Atual: {all_data["situacao"]}\nMotivo: {all_data["motivo"]}'
            template += f'\nValor Benefício: {all_data["vr_beneficio"]}'
            template += f'\nDE Situação Crédito: {all_data["de_situacao_credito"]}'
            template += f'\nDT Situação Crédito: {all_data["dt_situacao_credito"]}\n'

        else:
            template = self._get_msg_error(response)

        return template
