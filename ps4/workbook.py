import string

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

    print(shift_dict)

    return shift_dict

build_shift_dict(7)