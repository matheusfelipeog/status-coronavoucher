# -*- coding: utf-8 -*-

# @author: Matheus Felipe <github.com/matheusfelipeog>

import sys

if len(sys.argv) != 3:
    print('Uso: python main.py cpf sms_token')
    print('Exp: python main.py 12345678901 445566')
    sys.exit(0)

if __name__ == '__main__':
    from status_coronavoucher import Coronavoucher

    cpf = sys.argv[1]  
    sms_token = sys.argv[2]

    with Coronavoucher(cpf, sms_token) as Cv:
        print(Cv.show_status())
