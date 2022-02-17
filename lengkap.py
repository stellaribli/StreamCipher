
import codecs


def shortenKey(key): #memendekkan panjang key menjadi 256 bit
    temp_key = list(key)
    new_key = []
    for i in range(32):
        new_key.append(temp_key[i])
    return new_key

def ksa_lsfr(key):
    key_length = len(key)

    if(len(key)<=32):  #mengulang key jika panjang key kurang dari 256 bit
        key = list(key)
        for i in range(len(key)):
            key[i] = ord(key[i])
        for i in range(32 - len(key)): 
            key.append(key[i % len(key)])
    else: #memendekkan panjang key menjadi 256 bit
        shortenKey(key)

    #LSFR    
    lsfr = []
    biner = ''.join(format(i, '08b') for i in key)
    l = len(biner)
    for i in range(l):
        lsfr.append(biner[l-1])
        biner = str( int(biner[l-1]) ^ int(biner[0])) + biner[0:l-1]

    #KSA
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + int(lsfr[i]) + int((key[i % key_length]))) % 256
        S[i], S[j] = S[j], S[i] 

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i+1)%256
        j = (j+S[i])%256
        S[i], S[j] = S[j], S[i]
        t = (S[i]+S[j])%256
        u = S[t] #keystream
        yield u
        # c = u^P[idx]

def convert(key, teks): # Encrypt & decrypt
    input = list()
    for c in teks :
        input.append(ord(c))
    keystream = PRGA(ksa_lsfr(key))

    result = []
    for i in input:
        r = ("%02X" % (i ^ next(keystream)))    
        result.append(r)
    output = ''.join(result)
    return (codecs.decode(output, 'hex_codec').decode('latin-1'))

