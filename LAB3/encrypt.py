import os
import sys

if len(sys.argv) != 3:
    print("Usage: $python3 decrypt.py <receiver_name> <message>")
    exit()

if not os.path.isfile("param.pem"):
    print("*** ERROR: missing file \"param.pem\" ***")
    exit()

if not os.path.isfile(sys.argv[1] + "_pubkey.pem"):
    print("*** ERROR: missing file \"" + sys.argv[1] + "_pubkey.pem\" ***")
    exit()

message = sys.argv[2]

#ephkeys gen
os.system("openssl genpkey -paramfile param.pem -out eph_pkey.pem")
os.system("openssl pkey -in eph_pkey.pem -pubout -out  eph_pubkey.pem")

#common.bin gen
os.system("openssl pkeyutl -inkey eph_pkey.pem -peerkey " + sys.argv[1] + "_pubkey.pem -derive -out common.bin")

#keys gen
os.system("cat common.bin | openssl dgst -sha256 -binary | head -c 16 > k1.bin")
os.system("cat common.bin | openssl dgst -sha256 -binary | tail -c 16 > k2.bin")

#generating the iv
os.system("openssl rand 16 > iv.bin")

#Encrypting
os.system("echo -n \"" + sys.argv[2] +"\" | openssl enc -aes-128-cbc -K `cat k1.bin | xxd -p` -iv `cat iv.bin | xxd -p` > ciphertext.bin")

#Generating TAG
os.system("cat iv.bin ciphertext.bin | openssl dgst -sha256 -mac hmac -macopt hexkey:`cat k2.bin | xxd -p` -binary > tag.bin")

#Generating the ciphertext.pem file, with the ephimeral public key, the iv, the ciphertext and the tag
os.system("cat eph_pubkey.pem > ciphertext.pem")
os.system("echo \"-----BEGIN AES-128-CBC IV-----\" >> ciphertext.pem")
os.system("cat iv.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END AES-128-CBC IV-----\" >> ciphertext.pem")
os.system("echo \"-----BEGIN AES-128-CBC CIPHERTEXT-----\" >> ciphertext.pem")
os.system("cat ciphertext.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END AES-128-CBC CIPHERTEXT-----\" >> ciphertext.pem")
os.system("echo \"-----BEGIN SHA256-HMAC TAG-----\" >> ciphertext.pem")
os.system("cat tag.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END SHA256-HMAC TAG-----\" >> ciphertext.pem")

#Cleaning the aux files
os.system("rm iv.bin eph_* ciphertext.bin tag.bin k1.bin k2.bin common.bin")