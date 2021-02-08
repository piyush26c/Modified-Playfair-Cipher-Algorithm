

plaintext = input('Enter the plain text :')
ptl = list(plaintext)
fl = []
bl = []

for i in range(0,len(ptl)):
    if i%2 == 0:
        fl.append(plaintext[i])
    else:
        bl.insert(0,plaintext[i])

templist = fl + bl
ciphertext = ''.join(templist)
ciphertext =  ciphertext[::-1]
print('Cipher Text:',ciphertext)