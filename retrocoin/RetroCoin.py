import random
import time

import requests

class RetroCoinUser:
    def __init__(self, user, password, master_server: str = 'http://localhost:8080'):

        """
        
            # RetroCoin to users

            :param user: Your own username.
            :param password: Your password account.

            :param master_server: Master server address.

        
        """

        self.user = user
        self.password = password
        self.server = master_server



    def GetServerDifficulty(self):

        """
        
            # It makes a call to the server to be able to get what difficulty you are facing.
        
        """

        r = requests.get(self.server + '/API/GET/difficulty')

        return r.text


    def GetServerBlocks(self):

        """
        
            # It makes a call to the server to be able to get what blocks you are facing.
        
        """

        r = requests.get(self.server + '/API/GET/blocks')

        return r.text


    def GetServerKeys(self):
        
        """

            # Get message to desencrypted.
        
        """

        r = requests.get(self.server + '/API/GET/encryptedkey')

        return r.json()


    def Mine(self):



        cib = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'], 
                ['n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]


        nib = [['0', '1', '2', '3', '4'],
                ['5', '6', '7', '8', '9']]


        difficult = int(self.GetServerDifficulty())
        blocks = int(self.GetServerBlocks())
        keys = self.GetServerKeys()

        seed = 0

        while True:
            naturalcib = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'], 
                    ['n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]


            naturalnib = [['0', '1', '2', '3', '4'],
                    ['5', '6', '7', '8', '9']]
            

            seed = random.randrange(0, int(10 * blocks * difficult))
            print(f'Intentando con la semilla {seed}...')
            # time.sleep(1) # Antibug.

            random.seed(seed)

            random.shuffle(cib[0])
            random.shuffle(cib[1])
            random.shuffle(nib[0])
            random.shuffle(nib[1])

            

            key = keys['start'] # La llave principal.
            encrypted_message = ''

            for char in key.lower():
                char = char.lower()

                if char in cib[0]:
                    encrypted_message += cib[1][cib[0].index(char)]

                elif char in cib[1]:
                    encrypted_message += cib[0][cib[1].index(char)]

                elif char in nib[0]:
                    encrypted_message += nib[1][nib[0].index(char)]

                elif char in nib[1]:
                    encrypted_message += nib[0][nib[1].index(char)]

                else:
                    encrypted_message += char


            myEncrypted = encrypted_message

            
            if myEncrypted == keys['stop']:
                print(f'¡MINADO TERMINADO! \n\nSemilla: {seed}\nCon dificultad: {difficult}\nValido para el bloque: {blocks}\n\n\n')

                r = requests.get(self.server + f'/API/validate/ElHaban3ro/to/{seed}')
                # break
                print(r.text)
                return r.text

            else:
                cib = naturalcib
                nib = naturalnib
                print(f'No ha funcionado la semilla {seed}. Intentaremos con una nueva.')


            cib[0] = naturalcib[0]
            cib[1] = naturalcib[1]
            nib[0] = naturalnib[0]
            nib[1] = naturalnib[1]

            print(f'seed: {seed}')

            seed = 0
            random.seed(None)

            print(f'seed: {seed}')