import os
import sys

if len(sys.argv) != 2:
    print("Usage: $python3 gen_key.py <name>")
    exit()

#Reading the name of who will belongs the generated keys
name = sys.argv[1]

#Checking if the param file is generated. If it is not generated, it generates
if not os.path.isfile("param.pem"):
    os.system("openssl genpkey -genparam -algorithm dh -pkeyopt dh_rfc5114:3 -out param.pem")

#Generating the private and public key
os.system("openssl genpkey -paramfile param.pem -out " + name + "_pkey.pem")
os.system("openssl pkey -in " + name + "_pkey.pem -pubout -out " + name + "_pubkey.pem")