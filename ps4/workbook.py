import string
from ps4a import *
import random

"""def multi_recur(a, b):
    if b == 1:
        return a
    else:
        return a + multi_recur(a, b-1)

print(multi_recur(4, 300))"""

def build_shift_dict(shift):
    '''
    Creates a dictionary that can be used to apply a cipher to a letter.
    The dictionary maps every uppercase and lowercase letter to a
    character shifted down the alphabet by the input shift. The dictionary
    should have 52 keys of all the uppercase letters and all the lowercase
    letters only.        
    
    shift (integer): the amount by which to shift every letter of the 
    alphabet. 0 <= shift < 26

    Returns: a dictionary mapping a letter (string) to 
                another letter (string). 
    '''
    lower_list = list(string.ascii_lowercase)
    upper_list = list(string.ascii_uppercase)
    loop_point = 26-shift

    lower_shift = {lower_list[i]:(lower_list[i+shift] if i < loop_point else lower_list[i-loop_point]) for i in range(len(lower_list))}
    upper_shift = {upper_list[i]:(upper_list[i+shift] if i < loop_point else upper_list[i-loop_point]) for i in range(len(upper_list))}

    shift_dict = {**lower_shift, **upper_shift}

    return shift_dict

#build_shift_dict(7)

def apply_shift(shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_text = 'hello how are you?'
        shift_dict = build_shift_dict(shift)

        shifted_text = [(shift_dict[n] if n in shift_dict else n) for n in shift_text]

        return "".join(shifted_text)

#print(apply_shift(24))

def build_transpose_dict(vowels_permutation):
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
        
        shuffled_vowels = random.choice(get_permutations(vowels_permutation))

        lower_map = {vow_low[i]:shuffled_vowels[i] for i in range(len(vow_low))}

        upper_map = {vow_up[i]:shuffled_vowels[i].upper() for i in range (len(vow_up))}

        map_dict = {**lower_map, **upper_map, **{cons_low[i]:cons_low[i] for i in range(len(cons_low))}, **{cons_up[i]:cons_up[i] for i in range(len(cons_up))}}

        return map_dict

print(build_transpose_dict('aeiou'))