class Central:
    def __init__(self):
        self.lampada1 = False
        self.lampada2 = False
        self.arCondicionado = False
        self.projetor = False
        
        self.menu()
    
    def menu(self):
        menu = {
            1: 'Acender Lâmpada 01',
            2: 'Acender Lâmpada 02',
            3: 'Ligar Projetor Multimidia',
            4: 'Ligar Ar-Condicionado (1º Andar)',
            5: 'Ligar Sistema de Alarme',
            6: 'Ligar Sistema de Alerta de Incêndio',
            7: 'Sair'
        }

        for key in menu.keys():
            print (key, '--', menu[key])
        
        option = ''
        
        try:
            option = int(input('Escolha uma das opções acima \n'))
        except:
            print('Opção inválida. Digite um número de 1 a 7')

        if option == 1:
            self.modify_device_status(option)
        elif option == 2:
            self.modify_device_status(option)
        elif option == 3:
            self.modify_device_status(option)
        elif option == 4:
            self.modify_device_status(option)
        elif option == 5:
            self.modify_system_alarm_status()
        elif option == 6:
            self.modify_fire_alarm_status()
        elif option == 7:
            exit()
        else:
            print('Opção inválida. Digite um número de 1 a 7')

    def modify_device_status(self, option):
        if option == 1:
            demand_content = {
                "type": "lampada",
                "tag": "Lâmpada 01"
            }
        elif option == 2:
            demand_content = {
                "type": "lampada",
                "tag": "Lâmpada 02"
            }
        elif option == 3:
            demand_content = {
                "type": "projetor",
                "tag": "Projetor Multimidia"
            }
        elif option == 4:
            demand_content = {
                "type": "ar-condicionado",
                "tag": "Ar-Condicionado (1º Andar)"
            }

    def modify_system_alarm_status(self):
        pass

    def modify_fire_alarm_status(self):
        pass


if __name__=='__main__':
    Central()