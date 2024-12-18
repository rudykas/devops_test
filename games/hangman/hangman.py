# #imports
# import random
# import numpy as np


# # words 

# words = ['test', 'cat', 'dogt', 'lampt']

# # game 
# ## the task 

# word = words[random.randint(0,len(words)-1)]

# length = len(word)
# hidden_word = '_'*length
# shown_word = hidden_word

# print('Hi! here is what you need to guess: ' + hidden_word + ' \nyour turn: ')

# ## input 

# letter = input('Guess letter: ')

# def open_letter(letter, word, shown_word): 
#     # indices = np.where(array > 5)[0] = 
#     word = np.array(list(word))
#     if letter in word: 
#         indices = np.where(word == letter)
#         shown_word = np.array(list(shown_word))
#         shown_word[indices] = letter
#         shown_word = ''.join(shown_word)
#     print(shown_word)
#     return shown_word

#     pass

# state = 0
# while state < 8: 
#     if letter in word:
#         shown_word = open_letter(letter, word, shown_word)
#         if '_' not in shown_word: print('Congrats! You won, word is', shown_word)
#     else: 
#         state += 1
#         print('nope, you made ' + str(state) + ' errors')
#     letter = input('Ok. Guess next letter: ')
#     #todo add 

# print('Congrats! You lost')
# # drawing 


# # end
