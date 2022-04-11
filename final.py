"""
Created on 3/28/2022

@author: Matthew
"""

import random
import numpy as np

def encode(text):

    letters = []
    for i in range(97, 123):  # create a list of all lowercase letters
        letters.append(chr(i))
    cypher = letters.copy()
    random.shuffle(cypher)  # randomize the order of the encoding
    convert = {}

    for i in range(26):  # fill a dictionary with key = original letters
                         # and values = corresponding encoded letter
        convert[letters[i]] = cypher[i]

    ret = ""
    for char in text.lower():  # encode the original message
        if char in convert.keys():  # check that the character is a letter
            ret += convert[char]
        else:  # if it's not, leave it alone
            ret += char

    return ret

if __name__ == '__main__':
    print(encode("Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this."))