#!/usr/bin/env python3
'''
Este proyecto realiza una implementación del algoritmo AES con Python puro sin necesidad
de hacer uso de librerias o modulos externos.

La encriptación proporciona una formam segura de enviar y recibir mensajes.
'''

from .utils import *


class AES:
    """
    Clase para encriptación AES-128 con modo CBC y PKCS#7.
    Esto es una implementación pura de AES utilizando el modo de operaciones CBC
    """

    # AES-128 tamaño del bloque
    block_size = 16
    # AES-128 encripta los mensajes usando 10 rondas
    _rounds = 10


    # Inicializamos el objeto AES
    def __init__(self, key):
        """
        Inicializamos el objeto dandole una llave.
        """
        # Nos aseguramos que la llave tenga la longitud correcta, es decir, correspondiente al tamaño del bloque AES
        assert len(key) == AES.block_size

        self._round_keys = self._expand_key(key)


    def _expand_key(self, master_key):
        """
        Expande y devuelve una lista de matrices clave para la llave maestra dada.
        """

        # Inicializar la ronda de llaves con el material de la llave sin procesar.
        key_columns = bytes2matrix(master_key)
        iteration_size = len(master_key) // 4

        # Cada iteración tiene exactamente tantas columnas como el material de la llave.
        i = 1
        while len(key_columns) < (self._rounds + 1) * 4:
            # Copia la palabra previa.
            word = list(key_columns[-1])

            # Realiza "schedule_core" una vez por fila.
            if len(key_columns) % iteration_size == 0:
                # Cambio circular.
                word.append(word.pop(0))
                # Realiza un mapeo con el S-BOX.
                word = [s_box[b] for b in word]
                # XOR con el primer byte del R-CON, cuando los otros bytes del R-CON son 0.
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                # Recorre la palabra a través del S-box en la cuarta iteración usa una llave
                # de 256-bit.
                word = [s_box[b] for b in word]

            # XOR con la palabra equivalente de la iteración previa.
            word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
            key_columns.append(word)

        # Grupo de palabras claves en una matriz de bytes de 4x4.
        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]


    # Cifra un bloque simple de datos usando AES
    def _encrypt_block(self, plaintext):
        """
        Cifra un bloque simple de texto de 16 bytes de longitud.
        """
        # Longitud de un bloque simple
        assert len(plaintext) == AES.block_size

        # Lo transforma a una matriz
        state = bytes2matrix(plaintext)

        # Agrega la ronda de llaves
        add_round_key(state, self._round_keys[0])

        # 9 rondas principales
        for i in range(1, self._rounds):
            # SubBytes - Sustitución de bytes
            sub_bytes(state)
            # ShiftRows - Cambio de filas
            shift_rows(state)
            # MixCols - Combinación de columnas
            mix_columns(state)
            # AddRoundKey - Agrega la ronda de llaves
            add_round_key(state, self._round_keys[i])

        # Última ronda, con el paso de agregar la ronda de llaves
        sub_bytes(state)
        shift_rows(state)
        add_round_key(state, self._round_keys[-1])

        # Devuelve la matriz encriptada como bytes
        return matrix2bytes(state)


    # Descifra un bloque simple de datos usando AES
    def _decrypt_block(self, ciphertext):
        """
        Descifra un bloque simple de texto de 16 bytes de longitud.
        """
        # Longitud de un bloque simple
        assert len(ciphertext) == AES.block_size

        # Lo transforma a una matriz
        state = bytes2matrix(ciphertext)

        # En orden de reversa, la última ronda es la primera
        add_round_key(state, self._round_keys[-1])
        inv_shift_rows(state)
        inv_sub_bytes(state)

        for i in range(self._rounds - 1, 0, -1):
            # 9 rondas
            add_round_key(state, self._round_keys[i])
            inv_mix_columns(state)
            inv_shift_rows(state)
            inv_sub_bytes(state)

        # Inicia la fase de agregar la ronda de llaves
        add_round_key(state, self._round_keys[0])

        # devuelve los bytes
        return matrix2bytes(state)


    # Cifrará la totalidad de los datos
    def encrypt(self, plaintext, iv):
        """
        Cifra `texto plano` utilizando el modo CBC y el relleno PKCS#7,
        con el vector de inicialización dado (iv).
        """
        # La longitud del vector de inicialización (iv) debe tener la misma longitud que el tamaño del bloque AES
        assert len(iv) == AES.block_size

        # Rellena el texto plano
        plaintext = pad(plaintext)

        ciphertext_blocks = []

        previous = iv
        for plaintext_block in split_blocks(plaintext):
            # En el modo CBC, cada bloque aplica XOR con el bloque anterior
            xorred = xor_bytes(plaintext_block, previous)

            # Cifra el bloque actual
            block = self._encrypt_block(xorred)
            previous = block

            # Añade el texto cifrado
            ciphertext_blocks.append(block)

        # Devuelve los datos como bytes
        return b''.join(ciphertext_blocks)


    # Descifrará la totalidad de los datos
    def decrypt(self, ciphertext, iv):
        """
        Descifra `texto plano` utilizando el modo CBC y el relleno PKCS#7,
        con el vector de inicialización dado (iv).
        """
        # La longitud del vector de inicialización (iv) debe tener la misma longitud que el tamaño del bloque AES
        assert len(iv) == AES.block_size

        plaintext_blocks = []

        previous = iv
        for ciphertext_block in split_blocks(ciphertext):
            # En el modo CBC, cada bloque aplica XOR con el bloque anterior
            xorred = xor_bytes(previous, self._decrypt_block(ciphertext_block))

            # Añade el texto plano
            plaintext_blocks.append(xorred)
            previous = ciphertext_block

        # Devuelve un arreglo de bytes sin el relleno PKCS#7
        return unpad(b''.join(plaintext_blocks))


def cifrar(clave, texto):
    # Importamos los módulos y las clases requeridas para las pruebas
    import os
    class bcolors:
        OK = '\033[92m' #Verde
        WARNING = '\033[93m' #Amarillo
        FAIL = '\033[91m' #Rojo
        RESET = '\033[0m' #Color de reinicio

    # Genera una clave secreta e imprimir detalles
   
    key = os.urandom(AES.block_size)
    _aes = AES(clave)
    print(f"Algoritmo: AES-CBC-{AES.block_size*8}")
    print(f"Clave secreta: {clave.hex()}")
    print()

    # Prueba una frase de longitud arbitraria
    # iv = os.urandom(AES.block_size)
    
    iv = clave
    text = bytes(texto, 'utf-8')
    print("Prueba para cifrar cualquier texto")
    print("----------------------")
    print(f"iv: {iv.hex()}")
    print(f"texto plano : '{text.decode()}'")
    ciphertext = _aes.encrypt(text, iv)
    plaintext = _aes.decrypt(ciphertext, iv)
    print(f"Texto cifrado : {ciphertext.hex()}")
    print(f"texto plano: {plaintext.decode()}")
    assert text == plaintext
    print(bcolors.OK + "El cifrado se realizó con éxito" + bcolors.RESET)
    print()
    return ciphertext.hex()


def descifrar(key2, texto):
    # Importamos los módulos y las clases requeridas para las pruebas
    import os
    class bcolors:
        OK = '\033[92m' #Verde
        WARNING = '\033[93m' #Amarillo
        FAIL = '\033[91m' #Rojo
        RESET = '\033[0m' #Color de reinicio

    # Genera una clave secreta e imprimir detalles
   
    key = os.urandom(AES.block_size)
    _aes = AES(key2)
    print(f"Algoritmo: AES-CBC-{AES.block_size*8}")
    print(f"Clave secreta: {key2.hex()}")
    print()

    # Prueba una frase de longitud arbitraria
    iv = os.urandom(AES.block_size)

    text = bytes(texto, 'utf-8')
    print("Prueba para cifrar cualquier texto")
    print("----------------------")
    print(f"iv: {iv.hex()}")
    print(f"texto plano : '{text.decode()}'")
    ciphertext = _aes.encrypt(text, iv)
    plaintext = _aes.decrypt(ciphertext, iv)
    print(f"Texto cifrado : {ciphertext.hex()}")
    print(f"texto plano: {plaintext.decode()}")
    assert text == plaintext
    print(bcolors.OK + "El cifrado se realizó con éxito" + bcolors.RESET)
    print()
    return ciphertext.hex()




if __name__ == "__main__":
    # Prueba la clase AES
    test()    
