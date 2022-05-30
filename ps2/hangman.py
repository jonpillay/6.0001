# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
from asyncio.windows_events import NULL
import random
import string
from tracemalloc import stop

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def load_words_cleanly():
    """
    Returns a list of valid words. Words are strings of lowercase letters 
    without printing the startup 'load' message.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


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
        display_word_list.append('_ ')
    return ''.join(display_word_list)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alpha_list = list(string.ascii_lowercase)
    final_list = []
    for i in alpha_list:
      if i not in letters_guessed:
        final_list.append(i)
    return final_list
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    guesses_left = 6
    letters_guessed = []
    warnings = 3
    
    print("Welcome to the Game of Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("You have " + str(warnings) + " warnings left.")
    print("-------------")

    while is_word_guessed(secret_word, letters_guessed) == False:
      print("You have " + str(guesses_left) + " guesses left.")
      print("Available letters: " + ''.join(get_available_letters(letters_guessed)))
      guess = input("Please guess a letter: ").lower()
      if guess in letters_guessed:
        if warnings==0:
          guesses_left-=1
        else:
          warnings-=1
        print("Oops! You've already guessed that letter. You have " + str(warnings) + " warnings left")
        print("-------------")
      elif guess.isalpha() == False:
        if warnings==0:
          guesses_left-=1
        else:
          warnings-=1
        print("Oops! That is not a valid letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
        print("-------------")
      else:
        letters_guessed.append(guess)
        if guess not in secret_word:
          if guess in ['a', 'e', 'i', 'o', 'u']:
            guesses_left -= 2
          else:
            guesses_left-=1
          print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
        elif guess in secret_word:
          print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
        print("-----------")
        if guesses_left <= 0:
          print("Sorry, you ran out of guesses. The word was " + secret_word)
          break          
    if is_word_guessed(secret_word, letters_guessed) == True:
      print("That's great, you guessed the secert word ", secret_word, " in ", str(6-guesses_left), " guesses.")
    return
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



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
    cleaned_other_word = list(other_word)

    for i in range(len(cleaned_word)):
      if not len(cleaned_other_word) == len(cleaned_word):
        return False
      else:
        for i in range(len(cleaned_word)):
          if cleaned_word[i] in string.ascii_lowercase and cleaned_other_word[i] != cleaned_word[i]:
            return False
          elif i == len(cleaned_word)-1:
            return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    '''

    After intitially handling show_possible_matches() entirely within it's own funtion 
    I used match_with_gaps() as the course asked it be coded. Although with this method
    you have to clean my_word() on every loop over word_list as you call match_with_gaps.

    '''

    possible_matches = []
    wordList = load_words_cleanly()

    for word in wordList:
      if match_with_gaps(my_word, word) == True:
        possible_matches.append(word)
      else:
        pass
    return print(' '.join(possible_matches))



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_left = 6
    letters_guessed = []
    warnings = 3
    
    print("Welcome to the Game of Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("You have " + str(warnings) + " warnings left.")
    print("-------------")

    while is_word_guessed(secret_word, letters_guessed) == False:
      print("You have " + str(guesses_left) + " guesses left.")
      print("Available letters: " + ''.join(get_available_letters(letters_guessed)))
      guess = input("Please guess a letter: ").lower()
      if guess == '*':
        print("Possible word matches are: ")
        show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        print("-------------")
      else:
        if guess in letters_guessed:
          if warnings==0:
            guesses_left-=1
          else:
            warnings-=1
          print("Oops! You've already guessed that letter. You have " + str(warnings) + " warnings left")
          print("-------------")
          if guesses_left <= 0:
              print("Sorry, you ran out of guesses. The word was " + secret_word)
              break
        elif guess.isalpha() == False:
          if warnings==0:
            guesses_left-=1
          else:
            warnings-=1
          print("Oops! That is not a valid letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
          print("-------------")
        # Need to stop the '*' running to here
        if guesses_left <= 0:
              print("Sorry, you ran out of guesses. The word was " + secret_word)
              break
        else:
          letters_guessed.append(guess)
          if guess not in secret_word:
            if guess in ['a', 'e', 'i', 'o', 'u']:
              guesses_left -= 2
            else:
              guesses_left-=1
            print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
          elif guess in secret_word:
            print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
          print("-----------")
          if guesses_left <= 0:
            print("Sorry, you ran out of guesses. The word was " + secret_word)
            break          
    if is_word_guessed(secret_word, letters_guessed) == True:
      print("That's great, you guessed the secert word ", secret_word, " in ", str(6-guesses_left), " guesses.")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

#secret_word = choose_word(wordlist)
#hangman(secret_word)

if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)