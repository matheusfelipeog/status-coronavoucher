# -*- coding: utf-8 -*-

# @author: Matheus Felipe <github.com/matheusfelipeog>

if __name__ == '__main__':

    # Builtins
    import argparse

    # My Module
    from status_coronavoucher import Coronavoucher

    parser = argparse.ArgumentParser(
            prog='cli.py',
            usage='python %(prog)s [-h] cpf token [options]',
            description='Consulte a situação atual do auxílio emergencial.',
        )

    # Parâmetro CPF, que corresponde aos digitos do CPF da pessoa que irá consultar o status
    parser.add_argument(
        'cpf',
        action='store',
        type=int,
        help='os 11 digitos do CPF, sem espaço ou caracteres especiais.',
        metavar='CPF',
    )

    # Parâmetro token, que corresponde aos digitos enviados via SMS para o smartphone.
    parser.add_argument(
        'token',
        action='store',
        type=int,
        help='os 6 digitos do token SMS que é enviado.',
        metavar='TOKEN',
    )

    # Configuração do parâmetro que determina o formato da saída para visualização dos dados
    parser.add_argument(
        '-f', '--format',
        action='store',
        type=str,
        help='formato de retorno -> [simple, complete, raw]',
        metavar='format',
        default='simple',
        choices=['simple', 'complete', 'raw']
    )

    # Aglomera todos os argumentos passados em um objeto,
    # assim podendo ser acessados como atributos.
    args = parser.parse_args()

    cpf = args.cpf 
    sms_token = args.token

    with Coronavoucher(cpf, sms_token) as Cv:

        if args.format == 'simple':
            print(Cv.show_data())

        elif args.format == 'complete':
            print(Cv.show_all_data())

        elif args.format == 'raw':
            print(Cv.get_data())
