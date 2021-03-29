import os
import sys

doc_path = input("Type the path of the file to generate the proof:") #Request the path to the file to verify
doc_pos = input("Type the position of the file to generate the proof:") #Request the position of the file to verify in the hash tree

doc_hash = os.popen("cat doc.pre " + doc_path + " | openssl dgst -sha1 -binary | xxd -p").read() #Computes the hash of the file to verify

f = open("hash_tree.txt", "r")

public_info = f.readline() #Getting the public info of the hash tree
info = public_info.rsplit(":")
num_layers = int(info[-2])
root_hash = str(num_layers-1) + ":0:" + info[-1]
nodes = int(info[-2])
layer = 0
pos = int(doc_pos)
exists = False

for l in f: #Checks if the file to verify is in the position given in the tree
    if doc_hash in l and layer == int(l[0]) and pos == int(l[2]):
        exists = True
        break

f.close()

if exists: #If the file and the position are correct, prints the info necessary to verify its membership
    for i in range(num_layers-1):
        f = open("hash_tree.txt", "r")
        if pos%2 == 1: #linia del nodo anterior
           
            for l in f:
                if str(i) + ":" + str(pos-1) in l:
                    print(l)

        elif pos+1 != nodes:
            for l in f:
                if str(i) + ":" + str(pos+1) in l:
                    print(l)

        pos = int(pos/2)
        nodes = int(nodes/2) + nodes%2

        f.close()

    print(root_hash)

    

else: #If the file or the position are incorrect, it prints .
    print("***WRONG GIVEN INFORMATION***")
    sys.exit()