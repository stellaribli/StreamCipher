S=[]
P = str(input("Input P: "))
i = 0
j = 0
for idx in range (len(P)-1):
    i = (i+1)%256
    j = (j+S[i])%256
    S[i], S[j] = S[j], S[i]
    t = (S[i]+S[j])%256
    u = S[t]
    c = u^P[idx]

