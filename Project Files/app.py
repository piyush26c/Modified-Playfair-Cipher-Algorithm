# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from stegano import lsb
from ModifiedPlayfair import ModifiedPlayfair
import chardet

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA



app = Flask(__name__)

UPLOAD_FOLDER = 'UploadedImages/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


################# Utility Functions #######################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_keys():
   # key length must be a multiple of 256 and >= 1024
   key = RSA.generate(1024)
   publickey = key.publickey()
   return key.exportKey(), publickey.exportKey() #returns privetkey and public key

@app.route('/senderurl')
def sender():
    return render_template('sender.html')

@app.route('/receiverurl')
def receiver():
    return render_template('receiver.html')

###########################################################
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/accept_sender_data', methods = ['GET', 'POST'])
def accept_sender_data():
    if request.method == 'POST':
        print('line 44')
        ############## SENDER SIDE CODE ###############

        f = request.files['uploaded_image']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        else:
            return 'File format not supported!!'
        ####### Photo uploded ######
        print('line 55')
        plaintext = request.form['plaintext']
        print('Plaintext : ',plaintext)

        playfairkey = str(request.form['playfairkey'])
        print('Playfairkey : ',playfairkey)

        receiver_publickey = request.form['receiver_publickey']
        #print('Receiver publickey : ',receiver_publickey)
        ### All data collected from front end ########
        print('line 68')
        objModifiedPlayfair = ModifiedPlayfair() #creating obj of modified playfair class

        objModifiedPlayfair.getKey(playfairkey) # passing playfair key to that class

        objModifiedPlayfair.getPlainText(plaintext) # passing plaintext to that class

        objModifiedPlayfair.preparePairs()

        objModifiedPlayfair.generateKeyTable()

        objModifiedPlayfair.encrypt()

        cipher_from_playfair = objModifiedPlayfair.getCipherText()    ####### 1 (string)
        ######### Playfiar completed ############
        print('line 83')
        ########## RSA Started ################
        # encrypt() : Requires plaintecxt in bytes form only.

        receiver_publickey1 = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCd/6VYB0E3uazCZr4nuL2A6mqc\nyFFgeTjlH7QeDn1EFIEUFrogViH0+8AZaKVIvo0HJztdpaEA3Yl8iiVhQPFqm6JE\nYczZ7K+nD0/rMWIcF2k9TR9Y6MmP9zfL2WYM4soCM05L9zHlLLtaNMyraCgp/v3f\npPWI2oJ75cv+ouGpTQIDAQAB\n-----END PUBLIC KEY-----'


        print(type(receiver_publickey))
        print(receiver_publickey.encode('utf-8').replace(b'\\n', b'\n'))
        print(receiver_publickey.encode('utf-8').replace(b'\\n', b'\n') == receiver_publickey1.encode('utf-8'))


        pobj = RSA.importKey(receiver_publickey.encode('utf-8').replace(b'\\n', b'\n'))
        pobj = PKCS1_OAEP.new(pobj)
        print('RSA Cipher of playfairkey : ',pobj.encrypt(playfairkey.encode('utf-8')))  #print bytes in string form
        rsacipher_for_playfairKey = pobj.encrypt(playfairkey.encode('utf-8'))  #### 2 (rsacipher_for_playfairKey -> unique type che bytes)
        ########## RSA completed ############
        print("RSA Cipher: ", rsacipher_for_playfairKey)
        print("\nRSA Cipher Length: ", len(rsacipher_for_playfairKey))
        print('line 103')
        ########## R transposition Started ####
        playfair_rsa_combined_cipher = cipher_from_playfair + "||||" + str(rsacipher_for_playfairKey) # bytes to string
        
        ptl = list(playfair_rsa_combined_cipher)
        fl = []
        bl = []
        # print("Length : ", len(ptl))
        for i in range(0,len(ptl)):
            if i%2 == 0:
                # print("i: ", i)
                fl.append(playfair_rsa_combined_cipher[i])
            else:
                # print("i: ", i)
                bl.insert(0,playfair_rsa_combined_cipher[i])

        templist = fl + bl
        ciphertext = ''.join(templist)
        ciphertext =  ciphertext[::-1]
        print('Combined (RSA + Playfair) Cipher Text:', ciphertext)
        ########## R transposition completed ###########
        print('line 124')
        ########### stegnography Encryption ###############
        imgname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        secret = lsb.hide( imgname, ciphertext)
        
        imgextension = filename.split('.')[1]
        secret.save('EncryptedImg'+'.'+imgextension)
        
        # Downloading final encrypted image
        print('line 125')
        uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory= "", filename='EncryptedImg'+'.'+imgextension)

        #print('Encrypted image successfully downloaded at sender end!')
        #return render_template('index.html')

@app.route('/generate_receiver_keys')
def generate_receiver_keys():
    ######### RSA started #############
        privatekey, publickey = generate_keys()
        print("Public Key: ", publickey)
        print("\n\nPrivate Key: ", privatekey)
        return render_template('display_recvr_keys.html', privatekey=privatekey, publickey=publickey)

@app.route('/receiverside_decrypt')
def receiver_decrypt():
    return render_template('receiver_decrypt.html')

if __name__ == '__main__':
   app.run(debug = True)