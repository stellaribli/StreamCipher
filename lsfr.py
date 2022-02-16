def ksa_lsfr(key):
    key_length = len(key)

    lsfr = []
    biner = ''.join(format(i, '08b') for i in key)
    l = len(biner)
    for i in range(l):
        lsfr.append(biner[l-1])
        biner = str(int(biner[0]) ^ int(biner[l-1])) + biner[0:l-1]

    ksa = list()
    for c in key :
        ksa.append(ord(c))
    # panjang_key = len(ksa)

    # S = list(range(256))
    # j = 0
    # for i in range(256):
    #     j = (j + S[i] + ksa[i % panjang_key]) % 256
    #     S[i], S[j] = S[j], S[i]  # swap


    panjang_ksa = len(ksa)

    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + ksa[i % panjang_ksa] + int(ord(key[i % key_length])) + int(lsfr[i])) % 256
        S[i], S[j] = S[j], S[i]

    return S

