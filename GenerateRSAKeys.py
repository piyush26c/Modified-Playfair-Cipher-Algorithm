# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:23:44 2021

@author: Piyush
"""
# Step 1: To be run by receiver.
from Crypto import Random
from Crypto.PublicKey import RSA

def generate_keys():
   # key length must be a multiple of 256 and >= 1024
   modulus_length = 256*4
   key = RSA.generate(1024)
   publickey = key.publickey()
   return publickey.exportKey('PEM')


publickey = generate_keys()
f = open('pkey.pem', 'wb')
f.write(publickey)
# print(type(publickey))
print(publickey)
pobj = RSA.importKey(publickey)
print(pobj.encrypt("Hello", 12))



"""
Public Key : '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC7P8EZKubkA2vrfmoEtEMDWgXY\nlQIovjRl8MR43dNZ4y3gE6t7RX5y/xNBLYMtGThmZ0jnOXiBTS1hA+fGylW/9O3F\n1HWDcfgl2PG/mORsnqwK+nZczGofWIY+oEROlf0cYihWNv+a0n/tDgaIhCDHtdrR\ndz4lhjBwMaHJT7zjKQIDAQAB\n-----END PUBLIC KEY-----'
"""