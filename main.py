# -*- coding: utf-8 -*-

# @author: Matheus Felipe <github.com/matheusfelipeog>

if __name__ == '__main__':
    from status_coronavoucher import Coronavoucher

    cpf = 'CPF AQUI'  # Tudo junto, sem espaço
    sms_token = 'SMS TOKEN AQUI'  # Tudo junto, sem espaço

    with Coronavoucher(cpf, sms_token) as Cv:
        print(Cv.show_status())
