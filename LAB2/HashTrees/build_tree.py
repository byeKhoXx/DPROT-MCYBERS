import os

def new_layer(layer, num_hashes):

    num = 0
    for i in range(0, num_hashes, 2):
        if i == num_hashes-1 and num_hashes%2 == 1:
            os.system("cat node.pre node" + str(layer) + "." + str(i) + " | openssl dgst -sha1 -binary | xxd -p > node" + str(layer+1) + "." + str(num))
        else:
            os.system("cat node.pre node" + str(layer) + "." + str(i) + " node" + str(layer) + "." + str(i+1) + " | openssl dgst -sha1 -binary | xxd -p > node" + str(layer+1) + "." + str(num))
        

        os.system("echo -n '" + str(layer+1) + ":" + str(num) + ":' >> temp.txt")
        os.system("cat node" + str(layer+1) + "." + str(num) + " >> temp.txt")
        num = num+1


os.system("echo -n '\x35\x35\x35\x35\x35\x35' > doc.pre") #Creates the header for a document
os.system("echo -n '\xe8\xe8\xe8\xe8\xe8\xe8' > node.pre") #Creates the header for a node
os.system("touch temp.txt")

n = input ("Type the number of files the hash tree will contain:") #Request the number of files the hash tree will contain
n = int(n)

file_path = []
for i in range(n): #Request the path of each file and computes the hash
    file_path.append(input("Type the path of the file " + str(i+1) + ":"))
    os.system("cat doc.pre " + file_path[i] + " | openssl dgst -sha1 -binary | xxd -p > node0." + str(i))
    os.system("echo -n '" + str(0) + ":" + str(i) + ":' >> temp.txt")
    os.system("cat node" + str(0) + "." + str(i) + " >> temp.txt")

layer = 0
num_hashes = n
while num_hashes > 1: #Determine if it is necessary to create another layer or the root is reached
    new_layer(layer, num_hashes)
    layer = layer + 1
    
    if num_hashes%2 == 1:

        num_hashes = int(num_hashes/2) + 1
    else:

        num_hashes = int(num_hashes/2)


root_hash = os.popen("cat node" + str(layer) + ".0").read()
public_info = "MerkleTree:sha1:353535353535:e8e8e8e8e8e8:" + str(n) + ":" + str(layer+1) + ":" + root_hash #Appends the root hash to the hash tree public info

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt") #Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")
