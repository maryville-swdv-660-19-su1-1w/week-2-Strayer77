from django.test import TestCase
from game_api.models import Game

from django.core.exceptions import ValidationError

class GameModelTests( TestCase ):

    ### word field
    def test_init_should_assign_given_word(self):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.word, "TESTWORD" )
    
    def test_word_is_required( self ):
        with self.assertRaises( ValidationError ):
            game = Game()
            game.full_clean()

    def test_word_is_less_than_3_chars( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "AA")
            game.full_clean()

    def test_word_is_only_letters( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "A1B")
            game.full_clean()



    ### guesses_taken field
    def test_guesses_taken_should_not_increment_if_letter_in_word( self ):
        expectedGuessesTaken = 2
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= expectedGuessesTaken
        )

        game.handleGuess('T')
        self.assertEquals( expectedGuessesTaken, game.guesses_taken )

    def test_guesses_taken_should_increment_if_letter_not_in_word( self ):
        initialGuessesTaken = 2
        expectedGuessesTaken = initialGuessesTaken + 1
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= initialGuessesTaken
        )

        game.handleGuess('X')
        self.assertEquals( expectedGuessesTaken, game.guesses_taken )
    

    ### guessed_word_state field
    def test_guessed_word_state_is_unchanged_if_guess_not_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('X')
        self.assertEquals( initialGuessedWordState, game.guessed_word_state )

    def test_guessed_word_state_is_updated_with_guessed_letter_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        expectedGuessedWordState = ['T','','S','T','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('T')
        self.assertEquals( expectedGuessedWordState, game.guessed_word_state )


    ### available_letters field
    def test_init_should_set_letters_available_to_alphabet( self ):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.letters_available, list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    def test_available_letters_should_remove_guessed_letters_when_letter_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )
        
    def test_available_letters_should_remove_guessed_letters_when_letter_not_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )

    ### letters_guessed field
    def test_letters_guessed_should_add_guessed_letter_when_letter_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )
    
    def test_letters_guessed_should_add_guessed_letter_when_letter_not_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )

    ### is_game_over field
    # TODO: add tests
    # HINT: considering adding a fixture or other widely scoped variables if you feel ]hat will
    #  make this easier

    ######################################################################################
    
    #new tests - Week 2 HW - Strayer77

    # with the number of guesses at 3(4 once game handles guess, because X isn't in the word) 
    # out of 5, the game continues and is_game_over is False
    def test_is_game_over_is_false_if_guesses_left( self ):
        expectedState = False
        numberGuessesTaken = 3
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= numberGuessesTaken
        )
        game.handleGuess('X')
        self.assertEquals( game.is_game_over, expectedState )


    # with the guess being a letter in the word (T), and the number of guesses
    # 4 out of 5, is_game_over remains False because not all letters guessed yet
    def test_is_game_over_is_false_if_not_all_letters_guessed( self ):
        expectedState = False
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 4
        )
        game.handleGuess('T')
        self.assertEquals( game.is_game_over, expectedState )


    # with the number of guesses at 4, the guessed letter (X) isn't
    # in our word, so all guesses are used up (5 out of 5) and is_game_over is True
    def test_is_game_over_is_true_if_no_guesses_left( self ):
        expectedState = True
        numberGuessesTaken = 4
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', '', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= numberGuessesTaken
        )
        game.handleGuess('X')
        self.assertEquals( game.is_game_over, expectedState )

    
    # with 2 out of 5 guesses and only one letter remaining in guessed word state,
    # the guess 'T' will complete the game and set is_game_over to True
    def test_is_game_over_is_true_if_all_letters_guessed( self ):
        expectedState = True
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','E','S','','W','O','R','D'],
            letters_guessed = ['S', 'D', 'W', 'O', 'R','E'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )
        game.handleGuess('T')
        self.assertEquals( game.is_game_over, expectedState )