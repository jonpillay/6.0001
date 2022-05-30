from ast import Return
import random
import string
from hangman import *


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    word_split = list(secret_word)
    letters_left = len(word_split)

    for i in range(len(word_split)):
      if word_split[i] in letters_guessed:
        letters_left -= 1
    if letters_left == 0:
      return True
    else:
      return False

    """for i in word_split:
      print(i)
      if i in letters_guessed:
        dummy_split.remove(i)
        print(dummy_split)
    if len(dummy_split) == 0:
      print("True")
    else:
      print("False")"""

#is_word_guessed('strings', ['s','t','i','n', 'g', 'r'])

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    display_word_list = []
    word_split = list(secret_word)

    for i in word_split:
      if i in letters_guessed:
        display_word_list.append(i)
      else:
        display_word_list.append('_')
    return ''.join(display_word_list)

#get_guessed_word('strings', ['s'])

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    alpha_list = list(string.ascii_lowercase)
    for i in alpha_list:
      if i in letters_guessed:
        alpha_list.remove(i)
    return alpha_list

#get_available_letters(['g', 'a', 'o'])

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    def clean_word(word):
      wordList=list(word)
      for i in word:
        if i == ' ':
          wordList.remove(i)
      return wordList

    cleaned_word = clean_word(my_word)
    other_word_split = list(other_word)

    for i in range(len(cleaned_word)):
      if not len(other_word_split) == len(cleaned_word):
        return False
      else:
        for i in range(len(cleaned_word)):
          if cleaned_word[i] in string.ascii_lowercase and other_word_split[i] != cleaned_word[i]:
            return False
          elif i == len(cleaned_word)-1:
            return True

#match_with_gaps('t_ ct', 'tart')

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    """def clean_word(word):
      wordList = list(word)
      print(len(wordList))
      for i in wordList:
        print(i)
        if i == ' ':
          wordList.remove(i)
      return ''.join(wordList)

    cleaned_word = clean_word(my_word)
    possibe_matches = []

    for word in load_words():
      if len(word) == len(cleaned_word):
        for i in range(len(cleaned_word)):
          if cleaned_word[i] in string.ascii_lowercase and word[i] != cleaned_word[i]:
            break
          elif i == len(word)-1:
            possibe_matches.append(word)
    return print(possibe_matches)"""

    """ 

    After intitially handling show_possible_matches() entirely within it's own funtion 
    I used match_with_gaps() as the course asked it be coded. Although with this method
    you have to clean my_word on every loop over word_list as you call match_with_gaps.

    """

    possible_matches = []

    for word in load_words():
      if match_with_gaps(my_word, word) == True:
        possible_matches.append(word)
      else:
        pass
    return possible_matches