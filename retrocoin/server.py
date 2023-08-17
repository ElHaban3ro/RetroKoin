from flask import Flask
from markupsafe import escape
import random
import time
import json



app = Flask('RETROCOIN')


blocks = 1

@app.route('/ping')
def Ping():
    return 'pong'


@app.route('/API/GET/random-text-key')
def GetEncryptBase():
    """

        # Return a random key (text).
    
    """
    return 'MYPRIVATEKEYHERE'  #TODO: Obtener una palabra aleatoria del diccionario.


@app.route('/API/GET/encryptedkey')
def GenerateTargetEncrypted():
    """

        # Gives the user an encrypted message that can be used to decrypt and validate a block.
    
    """


    cib = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'], 
            ['n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]


    nib = [['0', '1', '2', '3', '4'],
            ['5', '6', '7', '8', '9']]


    difficult = int(GetDificulty())

    seed = random.randrange(0, int(10 * blocks * difficult))
    random.seed(seed)


    random.shuffle(cib[0])
    random.shuffle(cib[1])
    random.shuffle(nib[0])
    random.shuffle(nib[1])

    json_content = {}
    with open('./credentials_base.json', 'r+') as f:
        json_content = json.load(f)
        f.close()

    if json_content['start'] == 'zero' and json_content['stop'] == 'zero':

        encrypted_message = ''
        key = NewKey()


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


        with open('./credentials_base.json', 'w') as g:
            json.dump({'start': key, 'stop': encrypted_message, 'difficult': difficult}, g)
            g.close()

            print(seed)

            return {'start': key, 'stop': encrypted_message}

    else:
        return {'start': json_content['start'], 'stop': json_content['stop']}
            




@app.route('/API/validate/<user>/to/<seed>')
def validate_block(seed, user):

    """
    
        # Validates if a key was decrypted correctly.
        
        :param desencrypted_key: The key decrypted by the user and intended to be validated.
        param user: The user of the person who decrypted the message.
    
    """



    cib = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'], 
            ['n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]


    nib = [['0', '1', '2', '3', '4'],
            ['5', '6', '7', '8', '9']]



    difficult = int(GetDificulty())

    random.seed(int(seed))
    random.shuffle(cib[0])
    random.shuffle(cib[1])
    random.shuffle(nib[0])
    random.shuffle(nib[1])
    encrypted_message = ''

    json_content = {}
    key = ''
    with open('./credentials_base.json', 'r+') as f:
        json_content = json.load(f)
        key = json_content['start']
        f.close()


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


    if encrypted_message == json_content['stop']:            

        with open('./credentials_base.json', 'w') as g:
            json.dump({'start': 'zero', 'stop': 'zero', 'difficult': difficult}, g)
            g.close()

        GenerateTargetEncrypted()

        # TODO: dar lo que le pertenece al usuario.

        return 'Bloque minado, por ello, se te recompensará con 5 RetroCoins.'
    else:
        
        return 'La semilla es incorrecta.'


@app.route('/API/GET/difficulty')
def GetDificulty():
    with open('./credentials_base.json') as f:
        payload = json.load(f)


        f.close()

        return str(payload['difficult'])



@app.route('/API/GET/blocks')
def GetBlocks():
    return str(blocks)





#! ESTO NO ENTRA EN LA API.
def NewKey():
    
    """
    
        # Generate a random key to decrypt.
    
    """

    key = GetEncryptBase()

    difficulty = 40
    blocks = 666

    target_message = str(((blocks * (difficulty * 30) * random.randrange(0, 10)) * time.time()) / 25) + key + str((((difficulty * blocks * difficulty * random.randrange(blocks, (difficulty * 30))) / 2) * time.time()) / 450)

    return target_message


    

key = NewKey()
app.run()