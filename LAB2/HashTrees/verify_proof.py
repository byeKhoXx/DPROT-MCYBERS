import os
import sys

public_info = input("Type the public info in the correct format: ") #Request the hash tree public info
doc_path = input("Type the path of the document to verify: ") #Request the path of the document to verify
proof = input("Type the path of the file with the proof nodes, separated by \":\" and sorted: ") #Request the path of the file with the nodes needed to verify the membership

info = public_info.rsplit(":") 
root_hash = info[-1]
layers = int(info[-2])
os.system("cat doc.pre " + doc_path + " | openssl dgst -sha1 -binary | xxd -p > aux_hash.txt") #Computes the hash of the file to verify

aux = open(proof, "r")
nodes = aux.read().rsplit(":")
aux.close()

layer = 0
next_n = 0

n = nodes[next_n]

for i in range(layers):
    os.system("cp aux_hash.txt aux_hash2.txt")

    if layer+1 == layers: #Verifies if the root hashes are the same and prints the result
        aux_root_hash = os.popen("cat aux_hash2.txt").read()
        if root_hash in aux_root_hash:
            print("***OK***")
        else:
            print("***WRONG***")


        os.system("rm aux_hash.txt")
        os.system("rm aux_hash2.txt")
        sys.exit()

    elif int(n[4]) == layer: #Computes the hash of a node if needs another node to get the upper node
        if int(n[6])%2 == 0:
            os.system("cat node.pre " + n + " aux_hash2.txt | openssl dgst -sha1 -binary | xxd -p > aux_hash.txt")
        else:
            os.system("cat node.pre aux_hash2.txt " + n + " | openssl dgst -sha1 -binary | xxd -p > aux_hash.txt")

        next_n = next_n + 1
        n = nodes[next_n]


    else: #Computes the hash of a node if no needs another node to get the upper node
        os.system("cat node.pre aux_hash2.txt | openssl dgst -sha1 -binary | xxd -p > aux_hash.txt")

    layer = layer + 1
    
    
