#!/usr/bin/python3
# -*-coding-utf8-*-

import sys
import random

SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front
myMessage = """"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human."""

def DoMain() :
    myKey = 2023
    myMode = "encrypt"

    if myMode == "encrypt" :
        translated  = EncryptMessage(myKey, myMessage)
    elif myMode == "decrypt" :
        translated = DecryptMessage(myKey, myMessage)

    print("key : %s " % (myKey))
    print("%sed text: " % (myMode.title()))
    print()
    print(translated)
    print()

    myMode = "decrypt"
    translated = DecryptMessage(myKey, translated)
    print("decrypt : ")
    print() 
    print(translated)
        
##--------------------------------------------------------------------
    
def GDC(a, b) :
    while a != 0 :
        a, b = b % a, a

    return b

def FindModInvers(a, m) :
    if GDC(a, m ) != 1 :
        return None

    (u1, u2, u3) = (1, 0, a)
    (v1, v2, v3) = (0, 1, m)

    while v3 != 0 :
        q = u3 // v3
        (v1, v2, v3, u1, u2, u3) = ((u1 - q * v1), \
            (u2 - q * v2), \
            (u3 - q * v3), \
            v1, \
            v2, \
            v3)

    return u1 % m


print(GDC(24, 32))
print(GDC(37, 41))
print(FindModInvers(7, 26))
print(FindModInvers(8953851, 26))

##--------------------------------------------------------------------

def GetKeyParts(key) :
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)

    return (keyA, keyB)

def CheckKeys(keyA, KeyB, mode) :
    if keyA == 1 and mode == "encrypt" :
        sys.exit("The affine cipher becomes incredibly week when key is to 1. Choose different key.")

    if KeyB == 0 and mode == "encrypt" :
        sys.exit("The affine cipher becomes incredibly week when key is to 0. Choose different key.")

    if GDC(keyA, len(SYMBOLS)) != 1 :
        sys.exit("Key A (%s) and simbol set size (%s) are not prime." % (keyA, len(SYMBOLS)))

def EncryptMessage(key, message) :
    (keyA, keyB) = GetKeyParts(key)
    CheckKeys(keyA, keyB, "encrypt")

    cipherText = ''
    for symbol in message :
        if symbol in SYMBOLS :
            symIndex = SYMBOLS.find(symbol)
            cipherText += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else :
            cipherText += symbol

    return cipherText

def DecryptMessage(key, message) :
    (keyA, keyB) = GetKeyParts(key)
    CheckKeys(keyA, keyB, 'decrypt')
    plainText = ''
    modInverseOfKey = FindModInvers(keyA, len(SYMBOLS))

    for symbol in message :
        if symbol in SYMBOLS :
            symIndex = SYMBOLS.find(symbol) 
            plainText += SYMBOLS[(symIndex - keyB) * modInverseOfKey % len(SYMBOLS)]
        else :
            plainText += symbol

    return plainText

def GetRandomKey() :
    while True :
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))

        if GDC(keyA, len(SYMBOLS)) == 1 :
            return keyA * len(SYMBOLS) + keyB 

if __name__ == "__main__" :
    DoMain()





