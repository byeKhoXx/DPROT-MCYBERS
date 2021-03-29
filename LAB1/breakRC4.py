import os

key = os.popen("openssl rand -hex 13").read() #Generating a 13-bytes-length number for the key

print ("The key is " + key) #Printing the used key
print ("The message ciphered is \"A\"\n")

rep = {}
deduced_key = []

for i in range(256): #Generating all X value
    if i < 16: #IV + KEY
        aux_key = "01ff0"+ hex(i)[2:] + key
    else:
        aux_key = "01ff"+ hex(i)[2:] + key

    cipher = os.popen("echo -n 'A' | openssl enc -K '" + aux_key[:32] + "' -nosalt -rc4 | xxd ").read() #Ciphering in RC4 using IV + key

    first_Cbyte = "0x" + cipher[10] + cipher[11] #Extracting the first byte of the cipher text
    
    for j in range(256): #Generating all M[0] values
        
        res = hex(int(first_Cbyte, base=16) ^ int(hex(j), base=16)) #C[0] XOR M[0]
        
        if res == hex(i+2): #Checking if C[0] XOR M[0] == X+2
           
            if str(j) in rep:
                rep[str(j)] = rep[str(j)] + 1
            else:
                rep[str(j)] = 1


sorted_M = sorted(rep.items(), key=lambda x: x[1], reverse=True) #Sorting all the values which checks C[0] XOR M[0] == X+2 and sorting by most repetitions

print ("M[0] VALUE IS " + chr(int(sorted_M[0][0])) + " ***OK***") #Printing the M[0] guessed value

num = 3
checker = 0
for k in range(3,16): #Guessing all the key
    num = num + k
    rep = {}

    for i in range(256): #Generating all X values to guess k[k-3]

        if i < 16: #IV + KEY
            aux_key = "0" + hex(k)[2:] +"ff0"+ hex(i)[2:] + key
        else:
            aux_key = "0" + hex(k)[2:] + "ff"+ hex(i)[2:] + key

        cipher = os.popen("echo -n 'A' | openssl enc -K '" + aux_key[:32] + "' -nosalt -rc4 | xxd ").read()#Ciphering in RC4 using IV + key

        first_Cbyte = cipher[10] + cipher[11]#Extracting the first byte of the cipher text

        res = hex(int(first_Cbyte, base=16) ^ 65) # C[0] XOR M[0]
        res = int(res, base=16) - i - num #Calculating the value that has the breaking point

        for val in deduced_key:#Calculating the value that has the breaking point
            res = res - int(val, base=16)
       
        while res < 0: #Making positive the value
            res = res + 256

        if len(str(hex(res))) < 4: #Adding the value to the list
            res = "0x0" + str(hex(res))[2]
            if res in rep:
                rep[res] = rep[res] + 1
            else:
                rep[res] = 1

        else:

            if str(hex(res)) in rep:
                rep[str(hex(res))] = rep[str(hex(res))] + 1
            else:
                rep[str(hex(res))] = 1

    sorted_K = sorted(rep.items(), key=lambda y: y[1], reverse=True)#Sorting all the values as guessed keys by most repetitions

    if len(str(sorted_K[0][0])[2:]) < 2: #Adapting the guessed value
        sorted_K[0][0] = "0x0" + str(sorted_K[0][0])[2:]

    if str(sorted_K[0][0])[2:] == key[checker:checker + 2]: #Printing if the guessed value is correct or not

        print ("K[" + str(k-3) + "] VALUE IS " + str(sorted_K[0][0]) + " ***OK***")
        deduced_key.append(sorted_K[0][0])
    else:
        print ("K[" + str(k-3) + "] VALUE IS " + str(sorted_K[0][0]) + " ***WRONG***")

    checker = checker + 2
