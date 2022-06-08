# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from ps4a import get_permutations
from ps4b import *
import random
import time

start_time = time.time()

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(Message):
    def __init__(self, text, *args, **kwargs):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text, *args, **kwargs)

    def __str__(self):
        return str(self.text)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words_copy = self.valid_words.copy()

        return valid_words_copy
                
    def build_transpose_dict(self, vowels_permutation):
            '''
            vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
            
            Creates a dictionary that can be used to apply a cipher to a letter.
            The dictionary maps every uppercase and lowercase letter to an
            uppercase and lowercase letter, respectively. Vowels are shuffled 
            according to vowels_permutation. The first letter in vowels_permutation 
            corresponds to a, the second to e, and so on in the order a, e, i, o, u.
            The consonants remain the same. The dictionary should have 52 
            keys of all the uppercase letters and all the lowercase letters.

            Example: When input "eaiuo":
            Mapping is a->e, e->a, i->i, o->u, u->o
            and "Hello World!" maps to "Hallu Wurld!"

            Returns: a dictionary mapping a letter (string) to 
                    another letter (string).
            '''

            VOWELS_LOWER = 'aeiou'
            VOWELS_UPPER = 'AEIOU'
            CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
            CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

            vow_low = VOWELS_LOWER
            vow_up = VOWELS_UPPER
            cons_low = CONSONANTS_LOWER
            cons_up = CONSONANTS_UPPER
            

            lower_map = {vow_low[i]:vowels_permutation[i] for i in range(len(vow_low))}

            upper_map = {vow_up[i]:vowels_permutation[i].upper() for i in range (len(vow_up))}

            trans_dict = {**lower_map, **upper_map, **{cons_low[i]:cons_low[i] for i in range(len(cons_low))}, **{cons_up[i]:cons_up[i] for i in range(len(cons_up))}}

            return trans_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        trans_list = list(self.text)
        encrypted_text = [(transpose_dict[n] if n in transpose_dict else n) for n in trans_list]

        return "".join(encrypted_text)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text, *args, **kwargs):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text, *args, **kwargs)

    def __str__(self):
        return str(self.text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        #perm_list = get_permutations('aeiou')
        best_list = []

        for i in get_permutations('aeiou'):
            test_list = EncryptedSubMessage(self.apply_transpose(self.build_transpose_dict(i)).split())
            current_list = test_list.get_valid_words()
            if len(current_list) > len(best_list):
                best_list = current_list
        return " ".join(best_list)
    

if __name__ == '__main__':

    # Example test case (SubMessage)
    print("")
    print("Example test case (SubMessage) 1 \n")
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message(), "\n")

    # Example test case (SubMessage) 
    print("Example test case (SubMessage) 2 \n")
    message = SubMessage("This is a test!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "This is e tast!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message(), "\n")

    """
    Test cases work perfectly when permutations is set to static "eaiou".
    However randomising permutation with random.choice(get_permutations(VOWELS))
    gives differing results as possible numerous 'best cases' are found.
    Should be shown below repeating "This is a test!" with random permutation.

    Repeating could/should (see random.choice documentation) return both 
    "This is a test!" AND "Thus us a test!" for decrypted message.

    """

    # Example test case (SubMessage)
    print("3 Example test cases (SubMessage) repeat with random permutations. \n")
    print("Random test case 1. \n")
    message = SubMessage("This is a test!")
    permutation = random.choice(get_permutations('aeiou'))
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "?")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message(), "\n")

    # Example test case (SubMessage)
    print("Random test case 2. \n")
    message = SubMessage("This is a test!")
    permutation = random.choice(get_permutations('aeiou'))
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "?")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message(), "\n")

    # Example test case (SubMessage)
    print("Random test case 3. \n")
    message = SubMessage("This is a test!")
    permutation = random.choice(get_permutations('aeiou'))
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "?")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message(), "\n")

    #Example test case (EncryptedSubMessage)
    print("Example test case (EncryptedSubMessage) \n")
    message = SubMessage("This should test decrypt")
    enc_message = EncryptedSubMessage(message.apply_transpose(message.build_transpose_dict('eaiuo')))
    print("Original message:", message.get_message_text())
    print("Encrypted message:", enc_message.get_message_text())
    print("Decryted message:", enc_message.decrypt_message(), "\n")

    #Example test case (EncryptedSubMessage)
    print("Example test case with random permutation (EncryptedSubMessage)  \n")
    message = SubMessage("This should random test decrypt")
    enc_message = EncryptedSubMessage(message.apply_transpose(message.build_transpose_dict(random.choice(get_permutations('aeiou')))))
    print("Original message:", message.get_message_text())
    print("Encrypted message:", enc_message.get_message_text())
    print("Decryted message:", enc_message.decrypt_message())

print("--- %s seconds ---" % (time.time() - start_time))