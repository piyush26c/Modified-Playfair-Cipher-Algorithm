# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:19:25 2021

@author: Piyush
"""
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

#Step 3: Decrypt cipher text using own private key. (To be run by receiver)



def decrypt_message(encoded_encrypted_msg, privatekey):
   decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
   decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
   return decoded_decrypted_msg



decrypted_msg = decrypt_message(encrypted_msg, privatekey)


print ("Decrypted message: %s - (%d)\n\n" % (decrypted_msg, len(decrypted_msg)))