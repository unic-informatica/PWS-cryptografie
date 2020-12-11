ECB = 0
CBC = 1
PAD_NORMAL = 1
PAD_PKCS5 = 2
#Hier boven worden variabelen die nodig zijn voor het maken van het encryptie systeem zelf
#en de encryptie gedefinieerd.

#Hieronder wordt de basis van DES opgebouwd. Dit is nodig voor DES en triple DES encryptie.
class _Desbase(object):
#Als eerste worden regels gestelt. Namelijk dat IV (initial value) en pad geen unicode zijn. Dat pad en padmode niet allebei PAD_PKCS5 zijn.
#En dat IV en len(IV) (lengte IV) altijd 8 of een meerdere van 8 zijn.
    def __init__(self, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
        if IV:
            IV = self._NoUnicode(IV)
        if pad:
            pad = self._NoUnicode(pad)
        self.block_size = 8
        if pad and padmode == PAD_PKCS5:
            raise ValueError("Cannot use pad character with PAD_PKCS5")
        if IV and len(IV) != self.block_size:
            raise ValueError("IV must be a multiple of " + str(self.block_size) + " bytes")
        self._mode = mode
        self._iv = IV
        self._pad = pad
        self._padmode = padmode
#Hieronder worden alle conponeten die nodig zijn voor DES gedefinieerd, en hoe deze weer verkegen moeten worden.
#Dit gebeurd voor elk onderdeel, dat zijn: Key, mode, pad, padmode en IV.
#Bij de meeste onderdelen wordt eerst gecheckt of het geen unicode is behalve bij mode en padmode want die kunnen alleen de 4 variabelen zijn die als eerst worden gedefinieerd.
    def getkey(self):
        return self.__key
    
    def setkey(self, key):
        key = self._NoUnicode(key)
        self.__key = key
    
    def getmode(self):
        return self._mode
    
    def setmode(self, mode):
        self._mode = mode

    def getpad(self):
        return self._pad

    def setpad(self, pad):
        if pad is not None:
            pad = self._NoUnicode(pad)
        self._pad = pad

    def getpadmode(self):
        return self._padmode

    def setpadmode(self, mode):
        self._padmode = mode

    def getIV(self):
        return self._iv

    def setIV(self, IV):
        if not IV or len(IV) != self.block_size:
            raise ValueError("IV must be a multiple of " + str(self.block_size) + " bytes")
        IV = self._NoUnicode(IV)
        self._iv = IV
#Hieronder worden twee functies uitgelegd die zorgen dat de data de goed padding krijgt en daar weer uit kan komen.
#Veel van dit process is gewoon checken of het wel kan.  
    def _paddata(self, data, pad, padmode):
        if padmode is None:
            padmode = self.getpadmode()
        if pad and padmode == PAD_PKCS5:
            raise ValueError("Cannot use pad character with PAD_PKCS5")
        if padmode == PAD_NORMAL:
            if len(data) % self.block_size == 0:
                return data
            if not pad:
                pad = self.getpad()
            if not pad:
                raise ValueError("data must be a multiple of " + str(self.block_size) + " bytes long. Try using PAD_PKCS5 or set the pad character")
            data += (self.block_size - (len(data) % self.block_size)) * pad
        elif padmode == PAD_PKCS5:
            pad_len = 8 - (len(data) % self.block_size)
            data += bytes([pad_len] * pad_len)
        return data
    
    def _unpaddata(self, data, pad, padmode):
        if not data:
            return data
        if pad and padmode == PAD_PKCS5:
            raise ValueError("Cannot use pad character with PAD_PKCS5")
        if padmode is None:
            padmode = self.getpadmode()
        if padmode == PAD_NORMAL:
            if not pad:
                pad = self.getpad()
            if pad:
                data = data[:-self.block_size] + \
                        data[-self.block_size:].rstrip(pad)
        elif padmode == PAD_PKCS5:
            pad_len = data[-1]
            data = data[:-pad_len]
        return data
#Hieronder wordt een fuctie uitgelegd die checkt of er geen unicode wordt gebruikt.
    def _NoUnicode(self, data):
        if isinstance(data, str):
            try:
                return data.encode('ascii')
            except UnicodeEncodeError:
                pass
            raise ValueError("Cannot use unicode")
        return data

class des(_Desbase):
#Al de cijfers hieronder zijn nodig voor het verschuiven (encryptie werk zelf) van de data.
#Dit zijn dingen zoals permutaties (alles met p), sboxen (sb) en een vergrotings tabel (et).
#Ze heten de tables.
    __pc1 = [56, 48, 40, 32, 24, 16,  8,
        0, 57, 49, 41, 33, 25, 17,
        9,  1, 58, 50, 42, 34, 26,
        18, 10,  2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
        6, 61, 53, 45, 37, 29, 21,
        13,  5, 60, 52, 44, 36, 28,
        20, 12,  4, 27, 19, 11,  3
    ]

    __left = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]

    __pc2 = [
        13, 16, 10, 23,  0,  4,
        2, 27, 14,  5, 20,  9,
        22, 18, 11,  3, 25,  7,
        15,  6, 26, 19, 12,  1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    __ip = [57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8,  0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    __et = [
        31,  0,  1,  2,  3,  4,
        3,  4,  5,  6,  7,  8,
        7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]

    __sb = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]

    __p = [
        15, 6, 19, 20, 28, 11,
        27, 16, 0, 14, 22, 25,
        4, 17, 30, 9, 1, 7,
        23,13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10,
        3, 24
    ]

    __fp = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
    ]
#Deze twee variabelen zijn nodig om voor de code om te weten of hij moet en- of decrypten.
    ENCRYPT =   0x00
    DECRYPT =   0x01
#Hieronder wordt de key klaar gemaakt voor het en- en decrypten.
    def __init__(self, key, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
        if len(key) != 8:
            raise ValueError("Key size must be exactly 8 bytes long")
        _Desbase.__init__(self, mode, IV, pad, padmode)
        self.key_size = 8
        self.L = []
        self.R = []
        self.Kn = [ [0] * 48 ] * 16
        self.final = []
        self.setkey(key)
#Als er een key nodig is voor DES, gebruikt de code setkey van basis DES en nog een andere functie die later wordt uitgelegd.    
    def setkey(self, key):
        _Desbase.setkey(self, key)
        self.__create_sub_keys()
#Hier wordt de string die is gegeven (data) naar voor de code een bruikbare variant.  
    def __str_to_bitlist(self, data):
        l = len(data) * 8
        result = [0] * l
        pos = 0
#De characters van de data worden hier verschoven.
        for ch in data:
            i = 7
            while i >= 0:
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1
        return result
#Hier wordt de fuctie hierboven maar dan andersom uitgevoerd.
    def __bitlist_to_str(self, data):
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << (7 - (pos % 8))
            if (pos % 8) == 7:
                result.append(c)
                c = 0
            pos += 1
        return bytes(result)
#Hier wordt uitgelegd hoe de tables gebruikt moeten worden.
    def __permutate(self, table, block):
        return list(map(lambda x: block[x], table))
#Hier wordt uitgelegd hoe er kleinere keys gemaakt moeten worden.
#Dit wordt gedaan door de key in tweeën te splitsen en dan de linker helft te veranderen.
    def __create_sub_keys(self):
        key = self.__permutate(des.__pc1, self.__str_to_bitlist(self.getkey()))
        i = 0
        self.L = key[:28]
        self.R = key[28:]
#Hier worden 16 keys gemaakt.
        while i < 16:
            j = 0
            while j < des.__left[i]:
                self.L.append(self.L[0])
                del self.L[0]
                self.R.append(self.R[0])
                del self.R[0]
                j += 1
            self.Kn[i] = self.__permutate(des.__pc2, self.L + self.R)
            i += 1
#Hier wordt het grootste deel van de het en- en decrypten uitgelegd.    
    def __des_main(self, block, crypt_type):
        block = self.__permutate(des.__ip, block)
#Eerst wordt de sleutel in tweeën gedeeld.
        self.L = block[:32]
        self.R = block[32:]
#Dan wordt gezegd wat het moet doen als het aan het en- of decrypten is.
#Door iteration en iteration_adjustment voor allebei de types tegen over gesteld te maken
#kan de code en- en decrypten. 
        if crypt_type == des.ENCRYPT:
            iteration = 0
            iteration_adjustment = 1
        else:
            iteration = 15
            iteration_adjustment = -1
        i = 0
#De onderste code moet 16 keer worden uitgevoerd met 16 verschillende keys.
        while i < 16:
#Eerst wordt er een kopie gemaakt van de rechter helft van de sleutel gemaakt die er later weer bij komt.
            copyR = self.R[:]
#Dan wordt de rechter helft groter gemaakt en wordt er een XOR operations op uitgevoerd.
            self.R = self.__permutate(des.__et, self.R)
            self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[iteration]))
            B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]
            j = 0
            Bn = [0] * 32
            pos = 0
            while j < 8:
#Eerst worden alle stukken van B weer samengevoegd dit gebeurd deels met de hulp van de sboxen.
#Daarna wordt er een paar keer een AND operatie op v uitgevoerd.
#Dit gebeurd 8 keer.
                m = (B[j][0] << 1) + B[j][5]
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]
                v = des.__sb[j][(m << 4) + n]
                Bn[pos] = (v & 8) >> 3
                Bn[pos + 1] = (v & 4) >> 2
                Bn[pos + 2] = (v & 2) >> 1
                Bn[pos + 3] = v & 1
                pos += 4
                j += 1
#De rechter helft die nu helemaal veranderd is. 
#Krijgt een keer een permutatie and daarna een XOR operatie met linker helft.
#Dan wordt gezegd dat de nieuwe linker helft de oude rechter is .
            self.R = self.__permutate(des.__p, Bn)
            self.R = list(map(lambda x, y: x ^ y, self.R, self.L))
            self.L = copyR
#Per iteration is het net iets anders, maar met de zelfde key is elke iteration met het zelfde nummer
#ook echt het zelfde. Daarom hoeft er maar een functie geschreven te worden om het grooste deel
#van de en- en decryptie te doen.
            i += 1
            iteration += iteration_adjustment
#Hieronder wordt de final key gemaakt
        self.final = self.__permutate(des.__fp, self.R + self.L)
        return self.final
#Hieronder wordt een ander groot deel van het en- en decrypten gedaan.    
    def crypt(self, data, crypt_type):
#Eerst wordt gekeken of de data te gebruiken is.
        if not data:
            return ''
        if len(data) % self.block_size != 0:
            if crypt_type == des.DECRYPT:
                raise ValueError("Data must be a multiple of " + str(self.block_size) + " bytes long")
            if not self.getpad():
                raise ValueError("Data must be a multiple of " + str(self.block_size) + " bytes long. Try setting the pad character")
            else:
                data += (self.block_size - (len(data) % self.block_size)) * self.getpad()
#Als de mode CBC is moet er een IV worden gegeven, dus er wordt hieronder gekeken of dat is gedaan.
        if self.getmode() == CBC:
            if self.getIV():
                iv = self.__str_to_bitlist(self.getIV())
            else:
                raise ValueError("Must supply IV with CBC")

        i = 0
        result = []
        while i < len(data):
#Eerst word data in een bruikbare vorm gezet.
            block = self.__str_to_bitlist(data[i:i+8])
#Daarna wordt gekeken welke mode er wordt gebruikt.
#Als er CBC wordt gebruikt wordt er eerst gekeken of er een en- of decryptie plaats vind.
#Bij een encryptie wordt er een XOR operatie op data en IV uitgevoerd.
            if self.getmode() == CBC:
                if crypt_type == des.ENCRYPT:
                    block = list(map(lambda x, y: x ^ y, block, iv))
#Daarna wordt de data door __des_main (de functie boven deze) heen gehaald.
                processed_block = self.__des_main(block, crypt_type)
#Als het een decryptie is wordt er een XOR operatie op processed_block en IV uitgevoerd.
#En IV wordt gezet als block.
#Als het een Encryptie is wordt IV processed_block.
                if crypt_type == des.DECRYPT:
                    processed_block = list(map(lambda x, y: x ^ y, processed_block, iv))
                    iv = block
                else:
                    iv = processed_block
#Als de mode ECB is dan is processed_block gewoon block die door __dea_main wordt gehaald.
            else:
                processed_block = self.__des_main(block, crypt_type)
            result.append(self.__bitlist_to_str(processed_block))
            i += 8
#De stap hierboven wordt zo vaak gedaan tot i even groot is als len(data).
        return bytes.fromhex('').join(result)
#Hieronder wordt uitgelegd wat de code moet doen als het gaat encrypten.
#Veel van de stappen is kijken of het geen unicode is.
#Daarna wordt het in de goede padding gezet en door crypt gestuurd.
    def encrypt(self, data, pad=None, padmode=None):
        data = self._NoUnicode(data)
        if pad is not None:
            pad = self._NoUnicode(pad)
        data = self._paddata(data, pad, padmode)
        return self.crypt(data, des.ENCRYPT)
#Hieronder wordt beschreven hoe de code moet decrypten.
#Het is net zoals encrypten eerst checken of er geen unicode wordt gebruikt.
#Daarna wordt er het tegenovergestelde gedaan van encrypten.    
    def decrypt(self, data, pad=None, padmode=None):
        data = self._NoUnicode(data)
        if pad is not None:
            pad = self._NoUnicode(pad)
        data = self.crypt(data, des.DECRYPT)
        return self._unpaddata(data, pad, padmode)
#Hieronder wordt triple DES beschreven.    
class tripledes(_Desbase):
    def __init__(self, key, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
        _Desbase.__init__(self, mode, IV, pad, padmode)
        self.setkey(key)
#Hieronder wordt beschrevn hoe een key van triple DES in elkaar zit.
#De key bestaat uit 3 keys van 8 bytes.
#De key kan 16 of 24 bytes lang bij 16 gebruikt hij het eerste deel van de key als key 1 en key 3.
    def setkey(self, key):
        self.key_size = 24
        if len(key) != self.key_size:
            if len(key) == 16:
                self.key_size = 16
            else:
                raise ValueError("Key must be 16 or 24 bytes long for triple DES")
#Als er CBC wordt gebruikt dan wordt er gekeken of er een IV is gegeven.
#Als dat niet is wordt IV de key.
        if self.getmode() == CBC:
            if not self.getIV():
                self._iv = key[:self.block_size]
            if len(self.getIV()) != self.block_size:
                raise ValueError("IV must be 8 bytes long")
#Hier worden de eerste twee keys gemaakt
        self.__key1 = des(key[:8], self._mode, self._iv, self._pad, self._padmode)
        self.__key2 = des(key[8:16], self._mode, self._iv, self._pad, self._padmode)
#Als key orginele key 16 bytes was wordt key 1 weer gebruikt als key 3 anders wordt key 3 net zoals key 1 en 2 beschrven.
        if self.key_size == 16:
            self.__key3 = self.__key1
        else:
            self.__key3 = des(key[16:], self._mode, self._iv, self._pad, self._padmode)
        _Desbase.setkey(self, key)
#Hieronder worden alle set dingen weer uitgelegd ze zijn niet echt anders dan de normale set dingen.    
    def setmode(self, mode):
        _Desbase.setmode(self, mode)
        for key in (self.__key1, self.__key2, self.__key3):
            key.setmode(mode)
    
    def setpad(self, pad):
        _Desbase.setpad(self, pad)
        for key in (self.__key1, self.__key2, self.__key3):
            key.setpad(pad)
    
    def setpadmode(self, mode):
        _Desbase.setpadmode(self, mode)
        for key in (self.__key1, self.__key2, self.__key3):
            key.setpadmode(mode)
    
    def setIV(self, IV):
        _Desbase.setIV(self, IV)
        for key in (self.__key1, self.__key2, self.__key3):
            key.setIV(IV)
#Hieronder wordt uitgelegd hoe encrypten werkt.
#Eerst wordt gezegd dat ENCRYPT en DECRYPT die uit normale DES zijn.
#Daarna wordt nog gekeken of data en pad geen unicode zijn.    
    def encrypt(self, data, pad=None, padmode=None):
        ENCRYPT = des.ENCRYPT
        DECRYPT = des.DECRYPT
        data = self._NoUnicode(data)
        if pad is not None:
            pad = self._NoUnicode(pad)
        data = self._paddata(data, pad, padmode)
#Als de mode CBC is, dan wordt eerst IV per sleutel gezet.
#Dan wordt per blok van 8 de data geencrypt. Dat gebeurd totdat alle data encrypted is.
        if self.getmode() == CBC:
            self.__key1.setIV(self.getIV())
            self.__key2.setIV(self.getIV())
            self.__key3.setIV(self.getIV())
            i = 0
            result = []
            while i < len(data):
                block = self.__key1.crypt(data[i:i+8], ENCRYPT)
                block = self.__key2.crypt(block, DECRYPT)
                block = self.__key3.crypt(block, ENCRYPT)
                self.__key1.setIV(block)
                self.__key2.setIV(block)
                self.__key3.setIV(block)
                result.append(block)
                i += 8
            return bytes.fromhex('').join(result)
#ALs de mode ECB is dan wordt de data gelijk geencrypt.
        else:
            data = self.__key1.crypt(data, ENCRYPT)
            data = self.__key2.crypt(data, DECRYPT)
            return self.__key3.crypt(data, ENCRYPT)
#Decrypten is hetzelfde als encrypten maar dan andersom    
    def decrypt(self, data, pad=None, padmode=None):
        ENCRYPT = des.ENCRYPT
        DECRYPT = des.DECRYPT
        data = self._NoUnicode(data)
        if pad is not None:
            pad = self._NoUnicode(pad)
        if self.getmode() == CBC:
            self.__key1.setIV(self.getIV())
            self.__key2.setIV(self.getIV())
            self.__key3.setIV(self.getIV())
            i = 0
            result = []
            while i < len(data):
                iv = data[i:i+8]
                block = self.__key3.crypt(iv, DECRYPT)
                block = self.__key2.crypt(block, ENCRYPT)
                block = self.__key1.crypt(block, DECRYPT)
                self.__key1.setIV(iv)
                self.__key2.setIV(iv)
                self.__key3.setIV(iv)
                result.append(block)
                i += 8
            data = bytes.fromhex('').join(result)
        else:
            data = self.__key3.crypt(data, DECRYPT)
            data = self.__key2.crypt(data, ENCRYPT)
            data = self.__key1.crypt(data, DECRYPT)
        return self._unpaddata(data, pad, padmode)
