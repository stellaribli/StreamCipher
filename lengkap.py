import sys
import random
import codecs

def ksa_lsfr(key):
    key_length = len(key)
    key = list(key)
    for i in range(len(key)):
        key[i] = ord(key[i])
    lsfr = []
    biner = ''.join(format(i, '08b') for i in key)
    l = len(biner)
    for i in range(l):
        lsfr.append(biner[l-1])
        biner = str(int(biner[0]) ^ int(biner[l-1])) + biner[0:l-1]

    # ksa = list()
    # for c in key :
    #     ksa.append(ord(c))
    # panjang_key = len(ksa)

    # S = list(range(256))
    # j = 0
    # for i in range(256):
    #     j = (j + S[i] + ksa[i % panjang_key]) % 256
    #     S[i], S[j] = S[j], S[i]  # swap


    # panjang_ksa = len(key)

    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length] + int(ord(key[i % key_length])) + int(lsfr[i])) % 256
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(plainteks,S):
    i = 0
    j = 0
    for i in range (len(plainteks)-1):
        i = (i+1)%256
        j = (j+S[i])%256
        S[i], S[j] = S[j], S[i]
        t = (S[i]+S[j])%256
        u = S[t] #keystream
    return u
        # c = u^P[idx]

def encrypt(plainteks, key):
    # key = [ord(c) for c in key]
    S = ksa_lsfr(key)
    kstream = PRGA(S)
    output = []
    for char in plainteks:
        output.append("%02X" % (ord(char)^next(kstream)))
    hexd = ''.join(output)
    hexdata = hexd.encode('ascii').strip()
    return hexdata

def dec(cipherteks,key):
    key = [ord(c) for c in key]
    S = ksa_lsfr(key)
    kstream = PRGA(S)
    output = []
    for char in cipherteks:
        output.append("%02X" % (ord(char)^next(kstream)))
    hexd = ''.join(output)
    hexd = hexd.encode('ascii')
    decode_hex = codecs.getdecoder('ascii')
    hexd = decode_hex(hexd)[0]
    hexdata = hexd.strip()
    return hexdata

# print(encrypt('senin','selasa'))
