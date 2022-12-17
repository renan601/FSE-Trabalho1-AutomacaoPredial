class Display():
    def __init__(self):
        self.update_display([], False, False, False, False)

    def update_display(self, client_data, lampada1, lampada2, arCondicionado, projetor):
        if __name__=='__main__':
            for i in range(len(client_data)):
                print(f"Sistemas {client_data[i][0]}")

                print(f"Valor Lâmpada 01: {lampada1}")
                print(f"Valor Lâmpada 02: {lampada2}")
                print(f"Valor Ar Condicionado: {arCondicionado}")
                print(f"Valor Projetor: {projetor}")

if __name__=='__main__':
    Display()