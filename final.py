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


def processWP():
    transitions = np.zeros(shape=(27, 27))
    letters = [chr(x) for x in range(97, 123)]  # create a list of all lowercase
                                                # characters
    letters.append(" ")
    lettercount = [0 for x in letters]
    firstIteration = True

    with open("WarAndPeace.txt", 'r') as file:  # go through War And Peace
        for line in file:
            for char in line.lower():

                if char not in letters:  # ignore non-letters
                    continue

                if firstIteration:  # avoid an error since there is no character
                                    # before the first iteration
                    current = letters.index(char)
                    firstIteration = False
                    continue

                nextletter = letters.index(char)
                lettercount[nextletter] += 1  # keep track of how many times
                                              # each letter appears
                transitions[current, nextletter] += 1  # keep track of how many
                                                       # times each letter is
                                                       # followed by any other
                                                       # letter
                current = nextletter

    for row in range(27):  # divide the values in transitions by number of
                           # occurences to convert from raw number to frequency
        for column in range(27):
            transitions[row][column] /= lettercount[row]

    return transitions

if __name__ == '__main__':
    print(encode("Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this."))