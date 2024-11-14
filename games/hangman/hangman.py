#imports
import random



# words 

words = ['test', 'cat', 'dog', 'lamp']

# game 
## the task 

word = words[random.randint(0,len(words))]

length = len(word)
hidden_word = '_ '*length

print(hidden_word + ' your turn: ')

## input 

letter = input()

def open_letter(letter, word): 
    pass

if letter in word:
    open_letter(letter, word)
else: 
    draw_next()

# drawing 

# end
