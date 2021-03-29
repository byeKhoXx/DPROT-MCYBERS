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



doc_path = input("Type the path of the file to add:") #Request the path of the new file

f = open("hash_tree.txt", "r")
public_info = f.readline()
info = public_info.rsplit(":") #Getting public info of the hash tree to modify
nodes = int(info[-2]) #Getting the number of nodes of the hash tree


info_nodes = ""
for i in range (nodes): #Reads the private info of the hash tree
    info_nodes = info_nodes + f.readline()
f.close()
os.system("cat doc.pre " + doc_path + " | openssl dgst -sha1 -binary | xxd -p > node0." + str(nodes)) #Computes the hash of the new node

f = open("temp.txt", "a")
f.write(info_nodes)
f.close()
os.system("echo -n '" + str(0) + ":" + str(nodes) + ":' >> temp.txt") #Adding the new node to the private part of the hash tree
os.system("cat node" + str(0) + "." + str(nodes) + " >> temp.txt")
nodes = nodes + 1
old_nodes = nodes

layer = 0
while nodes > 1: #Determine if it is necessary to create another layer or the root is reached
    new_layer(layer, nodes)
    layer = layer + 1
    
    if nodes%2 == 1:

        nodes = int(nodes/2) + 1
    else:

        nodes = int(nodes/2)


root_hash = os.popen("cat node" + str(layer) + ".0").read()
public_info = "MerkleTree:sha1:353535353535:e8e8e8e8e8e8:" + str(old_nodes) + ":" + str(layer+1) + ":" + root_hash #Recomputing the public info of the hash tree

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt") #Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")
