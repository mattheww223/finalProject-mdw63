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


"""
Function to look at letter frequencies/transitions in War and Peace

OUTPUT:
transitions: a 27x27 numpy a array where the row is a letter (or space) and 
column is a letter or space. transitions[row][column] is the probability
of row being followed by column. 
"""
def processWP():
    transitions = np.zeros(shape=(27, 27))
    letters = [chr(x) for x in range(97, 123)]  # create a list of all lowercase
                                                # characters
    letters.append(" ")
    lettercount = [0 for x in letters]
    noCurrent = True

    with open("WarAndPeace.txt", 'r') as file:  # go through War And Peace
        for line in file:
            for char in line.lower():
                if char == "'":
                    noCurrent = True
                    continue

                if char not in letters:  # ignore non-letters
                    char = " "

                if noCurrent:  # avoid an error if there is no character
                    current = letters.index(char)
                    lettercount[current] += 1
                    noCurrent = False
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

def decode(text):
    letters = [chr(x) for x in range(97, 123)]
    trueTransitions = processWP()  # find expected transition matrix
    currTransitions = getTransitions(text, letters)  # find transition matrix
                                                     # for input
    errors = [100 for x in range(30)]
    errors[0] = calcError(trueTransitions, currTransitions)
    lettertracker = []
    counter = 0

    for iteration in range(90001):
        swap1 = random.randint(0, 25)  # randomly choose two letters to swap
        swap2 = random.randint(0, 25)

        while swap1 == swap2:
            swap2 = random.randint(0, 25)

        newTransitions = currTransitions.copy()  # make a new matrix with the
                                                 # rows/columns swapped
        newTransitions[[swap1, swap2]] = newTransitions[[swap2, swap1]]
        newTransitions[:, [swap1, swap2]] = newTransitions[:, [swap2, swap1]]

        # if the transition matrix is better with letters swapped, update order
        if calcError(trueTransitions, newTransitions) < errors[counter]:
            errors[counter] = calcError(trueTransitions, newTransitions)
            newLetters = letters.copy()
            temp = letters[swap1]
            newLetters[swap1] = newLetters[swap2]
            newLetters[swap2] = temp
            letters = newLetters[:26]
            currTransitions = newTransitions

        if iteration % 1000 == 0:
            print(errors[counter])


        if iteration % 3000 == 0:  # every 3000 iterations, store best letters
                                   # found and minimum error, then restart
            if iteration == 0:
                continue
            counter = iteration//3000
            letters = letters[:26]
            print(f"{letters} at iteration: {iteration}")
            lettertracker.append(letters.copy())
            random.shuffle(letters)
            currTransitions = getTransitions(text, letters)

    index = errors.index(min(errors))
    bestLetters = lettertracker[index]
    ret = buildWord(text, bestLetters)  # use the best key found to decode

    return ret

"""
getTransitions is a function that, given a text and a list letters, returns
the frequencies of transitions between letters

INPUTS:
text: text that we're wanting to find transitions for
letters: list of letters (can be unsorted) to find transition probabilities when
letters have been swapped

OUTPUTS:
textTransitions: 27x27 numpy array with entries corresponding to transition 
probabilities
"""
def getTransitions(text, letters):
    textTransitions = np.zeros(shape=(27, 27))
    letters.append(" ")
    lettercount = [0 for x in letters]
    noCurrent = True

    for char in text.lower():

        if char not in letters:  # ignore non-letters
            noCurrent = True
            continue

        if noCurrent:  # avoid an error if there is no current character
            current = letters.index(char)
            lettercount[current] += 1
            noCurrent = False
            continue

        nextletter = letters.index(char)
        lettercount[nextletter] += 1  # keep track of how many times
                                      # each letter appears
        textTransitions[current, nextletter] += 1  # keep track of how many
                                                   # times each letter is
                                                   # followed by any other
                                                   # letter
        current = nextletter

    for row in range(27):  # divide the values in transitions by number of
                           # occurences to convert from raw number to frequency
        for column in range(27):
            if lettercount[row] == 0:
                textTransitions[row][column] = 0
            else:
                textTransitions[row][column] /= lettercount[row]

    return textTransitions


"""
calcError looks for the sum of the squared errors for each entry of the
War and Peace transition matrix and the text transition matrix

INPUTS:
trueTransitions: 27x27 numpy array that is based on letter transitions in War
and Peace
textTransitions: 27x27 numpy array that is based on getTransitions

OUTPUT:
error: float sum of squared errors for each entry
"""
def calcError(trueTransitions, textTransitions):
    error = 0
    for i in range(27):
        for j in range(27):
            error += (trueTransitions[i][j] - textTransitions[i][j]) ** 2
    return error


"""
buildWord is a helper function that uses a given cypher to decode text

INPUTS:
text: a string of text
cypher: a list of letters, where the order corresponds to what the code is
(first letter will be swapped with a, second with b, etc.)

OUTPUT:
ret: a string corresponding to text with letters swapped based on cypher
"""
def buildWord(text, cypher):
    letters = [chr(x) for x in range(97, 123)]
    ret = ""
    for char in text.lower():
        if char in letters:  # check that the character is a letter
            ret += letters[cypher.index(char)]
        else:  # if it's not, leave it alone
            ret += char
    return ret


if __name__ == '__main__':
    #print(decode(encode("Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate—we can not consecrate—we can not hallow—this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us—that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion—that we here highly resolve that these dead shall not have died in vain—that this nation, under God, shall have a new birth of freedom—and that government of the people, by the people, for the people, shall not perish from the earth.")))
    #print(decode(encode("But tonight, I want to go easy on the traditional list of proposals for the year ahead. Don’t worry, I’ve got plenty, from helping students learn to write computer code to personalizing medical treatments for patients. And I will keep pushing for progress on the work that I believe still needs to be done. Fixing a broken immigration system. (Applause.) Protecting our kids from gun violence. (Applause.) Equal pay for equal work. (Applause.) Paid leave. (Applause.) Raising the minimum wage. (Applause.) All these things still matter to hardworking families. They’re still the right thing to do. And I won't let up until they get done. But for my final address to this chamber, I don’t want to just talk about next year. I want to focus on the next five years, the next 10 years, and beyond. I want to focus on our future. We live in a time of extraordinary change -- change that’s reshaping the way we live, the way we work, our planet, our place in the world. It’s change that promises amazing medical breakthroughs, but also economic disruptions that strain working families. It promises education for girls in the most remote villages, but also connects terrorists plotting an ocean away. It’s change that can broaden opportunity, or widen inequality. And whether we like it or not, the pace of this change will only accelerate. America has been through big changes before -- wars and depression, the influx of new immigrants, workers fighting for a fair deal, movements to expand civil rights. Each time, there have been those who told us to fear the future; who claimed we could slam the brakes on change; who promised to restore past glory if we just got some group or idea that was threatening America under control. And each time, we overcame those fears. We did not, in the words of Lincoln, adhere to the “dogmas of the quiet past.” Instead we thought anew, and acted anew. We made change work for us, always extending America’s promise outward, to the next frontier, to more people. And because we did -- because we saw opportunity where others saw only peril -- we emerged stronger and better than before. What was true then can be true now. Our unique strengths as a nation -- our optimism and work ethic, our spirit of discovery, our diversity, our commitment to rule of law -- these things give us everything we need to ensure prosperity and security for generations to come.")))
    print(decode(encode("Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity. But 100 years later, the Negro still is not free. One hundred years later, the life of the Negro is still sadly crippled by the manacles of segregation and the chains of discrimination. One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity. One hundred years later the Negro is still languished in the corners of American society and finds himself in exile in his own land. And so we've come here today to dramatize a shameful condition. In a sense we've come to our nation's capital to cash a check. When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir. This note was a promise that all men — yes, Black men as well as white men — would be guaranteed the unalienable rights of life, liberty and the pursuit of happiness. It is obvious today that America has defaulted on this promissory note insofar as her citizens of color are concerned. Instead of honoring this sacred obligation, America has given the Negro people a bad check, a check which has come back marked insufficient funds. But we refuse to believe that the bank of justice is bankrupt. We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation. And so we've come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice. We have also come to his hallowed spot to remind America of the fierce urgency of now. This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism. Now is the time to make real the promises of democracy. Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice. Now is the time to lift our nation from the quick sands of racial injustice to the solid rock of brotherhood. Now is the time to make justice a reality for all of God's children. It would be fatal for the nation to overlook the urgency of the moment. This sweltering summer of the Negro's legitimate discontent will not pass until there is an invigorating autumn of freedom and equality. 1963 is not an end, but a beginning. Those who hope that the Negro needed to blow off steam and will now be content will have a rude awakening if the nation returns to business as usual.")))
    pass
