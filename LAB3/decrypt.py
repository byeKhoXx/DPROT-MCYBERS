import os
import sys

if len(sys.argv) != 3:
    print("Usage: $python3 decrypt.py <ciphertext> <destinatary_name>")
    exit()

if not os.path.isfile(sys.argv[2] + "_pkey.pem"):
    print("*** ERROR: missing file \"" + sys.argv[2] + "_pkey.pem\" ***")
    exit()

#Reading the ephpub, iv, ciphertext and tag
f = open(sys.argv[1], "r")
info = f.read()
f.close()

#PUBLIC KEY
pub_key_i = info.find("-----END PUBLIC KEY-----")
pub_key = info[:pub_key_i+24]
os.system("echo -n \"" + pub_key + "\" > ephpub.pem")

#IV
iv_i = info.find("-----END AES-128-CBC IV-----")
iv = info[pub_key_i+56:iv_i]
os.system("echo -n \"" + iv + "\" | openssl base64 -d -out iv.bin")

#CIPHERTEXT
cipher_i = info.find("-----END AES-128-CBC CIPHERTEXT-----")
cipher = info[iv_i+68:cipher_i]
os.system("echo -n \"" + cipher + "\" | openssl base64 -d -out ciphertext.bin")

#TAG
tag_i = info.find("-----END SHA256-HMAC TAG-----")
tag = info[cipher_i+69:tag_i]
os.system("echo -n \"" + tag + "\" | openssl base64 -d -out tag.bin")

#Generating common key
os.system("openssl pkeyutl -inkey " + sys.argv[2] + "_pkey.pem -peerkey ephpub.pem -derive -out common.bin")

#Extracting Key1 & Key2
os.system("cat common.bin | openssl dgst -sha256 -binary | head -c 16 > k1.bin")
os.system("cat common.bin | openssl dgst -sha256 -binary | tail -c 16 > k2.bin")

#Generating the tag
os.system("cat iv.bin ciphertext.bin | openssl dgst -sha256 -mac hmac -macopt hexkey:`cat k2.bin | xxd -p` -binary > deciphered_tag.bin")

#Checking the tag
if os.popen("cat tag.bin | openssl base64").read() == os.popen("cat deciphered_tag.bin | openssl base64").read():
    #Decrypting the message
    os.system("openssl enc -aes-128-cbc -d -in ciphertext.bin -iv `cat iv.bin | xxd -p` -K `cat k1.bin | xxd -p` -out deciphered.txt")
else:
    print("*** ERROR: Wrong TAG. Please specify the correct receiver. ***")
 
#Cleaning the aux files
os.system("rm iv.bin ciphertext.bin ephpub.pem tag.bin k1.bin k2.bin common.bin deciphered_tag.bin")