
# coding: utf-8

# In[52]:

from random import randint

HangmanLexicon = {
    0: 'OCTOPUS',
    1: 'BUOY',
    2: 'COMPUTER',
    3: 'FUZZY',
    4: 'ECSTATIC',
    5: 'ELECTRICITY',
    6: 'UNSTABLE',
    7: 'REUSABLE',
    8: 'BOTTLE',
    9: 'RECESSION',
    10: 'MAGNITUDE',
    
}

def PlayHangman(guesses, Lexicon):
    word = Lexicon[randint(0,10)]
    hidden_word = list('_ ' * len(word))
    guessed_letters = []
    
    print("Let's play Hangman!")
    print(''.join(hidden_word))
    
    while True:
        letter = input('Guess a letter: ')
        
        if len(letter) > 1 or letter.upper() not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or letter == '':
            print(letter, ' is not a letter. You must guess a letter.')
        
        else:
            
            if letter.upper() in guessed_letters:
                print('You have already guessed this letter!')

            else:
                guessed_letters.append(letter.upper())

                if letter.upper() in word:
                    print('CORRECT! ', letter.upper(), ' is in the word.')
                    for i in range(len(word)):
                        if word[i] == letter.upper():
                            hidden_word[i*2] = letter.upper()
                        if '_' not in hidden_word:
                            return print('CONGRATULATIONS! You win! \nThe answer was ' + word)

                elif str(letter).upper() not in word:
                    print('INCORRECT. ', letter, ' is not in the word.')
                    guesses -= 1
                    if guesses < 0:
                        return print('Game Over! You have been hanged :( \nThe correct answer was ' + word)

                print('The word now looks like: ' + ''.join(hidden_word))
                print('You have ' + str(guesses) + ' guesses left.')
    


# In[53]:

PlayHangman(7, HangmanLexicon)


# In[ ]:



