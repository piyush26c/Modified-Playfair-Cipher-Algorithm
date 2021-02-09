# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 18:54:55 2021

@author: Piyush
"""
#Step 2: Get Public Key of Receiver for encrypting the plain text. (To be run by sender)
    
        
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def encrypt_message(a_message , publickey):
   encrypted_msg = publickey.encrypt(a_message, 32)[0]
   encoded_encrypted_msg = base64.b64encode(encrypted_msg)
   return encoded_encrypted_msg



a_message = "This Mayuresh!".encode("utf-8")


importedpk = RSA.importKey('-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC7P8EZKubkA2vrfmoEtEMDWgXY\nlQIovjRl8MR43dNZ4y3gE6t7RX5y/xNBLYMtGThmZ0jnOXiBTS1hA+fGylW/9O3F\n1HWDcfgl2PG/mORsnqwK+nZczGofWIY+oEROlf0cYihWNv+a0n/tDgaIhCDHtdrR\ndz4lhjBwMaHJT7zjKQIDAQAB\n-----END PUBLIC KEY-----')
importedpk.encrypt("Hello", 12)

# print(pk.encrypt("Hello", 12) == importedpk.encrypt("Hello", 12))


