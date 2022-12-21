def correct_input(min_value, max_value):
    while True:
        try:
            option = int(input('Escolha uma das opções acima \n'))
            if option >= min_value and option <= max_value:
                return option
            else:
                print(f'Digite um número entre {min_value} e {max_value}')
        except:
            print('Opção inválida. Digite um número')
