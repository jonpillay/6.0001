# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from typing import Sequence


def get_permutations(sequence, index=0, perm_list=[]):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if index == len(sequence):
        perm_list.append("".join(sequence))
    for f in range(index, len(sequence)):
        perm = [x for x in sequence]
        perm[index], perm[f] = perm[f], perm[index]
        get_permutations(perm, index+1, perm_list)
    return perm_list

print(get_permutations('abc'))

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

