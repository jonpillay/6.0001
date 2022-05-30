# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

from cgi import test
import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    score = SCRABBLE_LETTER_VALUES
    clean_word = word.lower()
    score_list = []
    multiplier = (7*len(word)) - 3*(n-len(word))

    for i in range(len(clean_word)):
        if clean_word[i] == '*':
            pass
        else:
            score_list.append(score[clean_word[i]])
    if multiplier >= 1:
        score = sum(score_list) * multiplier
    else:
        score = sum(score_list)
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels + 1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*']=1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()
    clean_word = word.lower()

    for i in range(len(word)):
        if clean_word[i] in hand:
            if hand[clean_word[i]] == 0:
                pass
            else:
                new_hand[clean_word[i]] = new_hand[clean_word[i]] -1
                if new_hand[clean_word[i]] == 0:
                    del new_hand[clean_word[i]]
    return new_hand

#update_hand({'a': 1, 'q': 1, 'l': 2, 'm': 1, 'u': 1, 'i': 1}, 'evil')
#update_hand('Evil', {'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2})

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    clean_word = word.lower()
    test_hand = hand.copy()
    
    # need to make check for the word in word list with the *


    """if '*' in clean_word:
        for other_word in word_list:
            if len(other_word) == len(clean_word):
                for i in range(len(clean_word)):
                    if clean_word[i] in string.ascii_lowercase and clean_word[i] != other_word[i]:
                        break
                    elif i == len(clean_word)-1:
                        return True
            else:
                pass
        return False
    else:
        if clean_word in word_list:
            for i in range(len(clean_word)):
                if clean_word[i] in test_hand:
                    test_hand = update_hand(test_hand, clean_word[i])
                    if i == len(clean_word)-1:
                        return True
                else:
                    return False
        else:
            return False"""

    # Sure I can rewrite this to cut out the '*' check layer and half the length of the code.
    # The * loop should be able to check if is * and pass onto next element if it is.

    if '*' in clean_word:
        for other_word in word_list:
            if len(other_word) == len(clean_word):
                for i in range(len(clean_word)):
                    if clean_word[i] in hand:
                        if clean_word[i] in string.ascii_lowercase and clean_word[i] != other_word[i]:
                            break
                        elif i == len(clean_word)-1:
                            return True
                    else:
                        break
            else:
                pass
        return False
    else:
        if clean_word in word_list:
            for i in range(len(clean_word)):
                if clean_word[i] in test_hand:
                    test_hand = update_hand(test_hand, clean_word[i])
                    if i == len(clean_word)-1:
                        return True
                else:
                    return False
        else:
            return False

# test_ps3.py is returning that is_word_valid with wildcards should respond with False for is_word_valid('e*m', {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '*': 1}, word_list)
# However elm is in word_list
# Code below shows this

"""word_list = load_words()
if 'elm' in word_list:
    print("it is there")
else:
    print("It is not there")"""


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return len(hand)
    

def play_hand(hand, word_list):
    player_score = 0
    while calculate_handlen(hand) > 0:
        print("")
        print("Current hand: ", end="")
        display_hand(hand)
        played_word = input("Please enter a word or '!!' to indicate you are done: ")
        if played_word == '!!':
            return False
        else:
            if is_valid_word(played_word, hand, word_list):
                score = get_word_score(played_word, HAND_SIZE)
                print("You scored: " + str(score))
                player_score += score
                hand = update_hand(hand, played_word)
            else:
                print(played_word + " is not a valid word. Please try again!")
                hand = update_hand(hand, played_word)
    return player_score
            
                
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

#play_hand(deal_hand(HAND_SIZE), load_words())

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    subs = hand.get(letter)
    while True:
        if letter in VOWELS:
            x = random.choice(VOWELS)
        else:
            x = random.choice(CONSONANTS)
        if x in hand:
            pass
        else:
            del hand[letter]
            hand[x]=subs
            return hand



def play_game(word_list, hand=None, hands=None, pre_score=None, loop=False):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    game_score = 0

    if loop == False:
        hands = int(input("Enter total number of hands: "))
        hand = deal_hand(HAND_SIZE)
        hand_copy = hand.copy()
        hands_copy = hands
        replays = 1
    print("Current hand: ", end="")
    display_hand(hand)

    if loop == False:
        decision = input("Would you like to the substitute a letter? ")
        if decision == 'yes':
            letter = input("What letter would you like to replace: ")
            if letter in hand:
                hand = substitute_hand(hand, letter)
                hand_copy = hand
    while hands > 0 and calculate_handlen(hand) > 0:
        x = play_hand(hand, word_list)
        hands-=1
        if x == False:
            hands = 0
        else:
            game_score += x
    if pre_score and pre_score > game_score:
        game_score=pre_score
    if calculate_handlen(hand) == 0:
        print("You ran out of letters")
    print("Total score for this hand: " + str(game_score))
    print("----------")
    if replays > 0:
        replays -= 1
        replay = input("Would you like to replay hand? ")
        if replay == 'yes':
            print("We are here somehow")
            play_game(word_list, hand_copy, hands_copy, game_score, loop=True)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)