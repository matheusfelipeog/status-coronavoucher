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

    # Parâmetro nome, que corresponde ao nome informado na hora do cadastro no sistema do auxílio.
    parser.add_argument(
        'nome',
        action='store',
        type=str,
        help='O nome informado na hora do cadastro no sitema.',
        metavar='NOME',
    )

    # Parâmetro nasc, que corresponde a data de nascimento no formato Ano-Mês-Dia
    parser.add_argument(
        'nasc',
        action='store',
        type=str,
        help='A data de nascimento no formato AA-MM-DD (Ano-Mês-Dia).',
        metavar='NASC',
    )

    # Parâmetro mae, que corresponde ao nome da mãe do solicitante do auxílio.
    parser.add_argument(
        'mae',
        action='store',
        type=str,
        help='Nome da mãe do solicitante do auxílio.',
        metavar='MAE',
    )

    # Parâmetro desc/desconhecida, caso a mãe do solicitante não seja conhecida.
    parser.add_argument(
        '-desc', '--desconhecida',
        action='store',
        type=bool,
        help='Informe se a mãe é desconhecida com True. False é o padrão',
        metavar='desc',
        default=False,
        choices=[True, False]
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
    nome = args.nome
    nasc = args.nasc
    mae = args.mae
    desc = args.desconhecida

    with Coronavoucher(cpf, nome, nasc, mae, desc) as Cv:

        if args.format == 'simple':
            print(Cv.show_data())

        elif args.format == 'complete':
            print(Cv.show_all_data())

        elif args.format == 'raw':
            print(Cv.get_data())
