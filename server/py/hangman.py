# Example solution to test docker thingies


from typing import List, Optional
import string
import random
from enum import Enum
from pydantic import BaseModel, field_validator
from server.py.game import Game, Player


class GuessLetterAction(BaseModel):
    letter: str

    @field_validator("letter")
    @classmethod
    def uppercase(cls, value: str) -> str:
        return value.upper()


class GamePhase(str, Enum):
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished


class HangmanGameState(BaseModel):
    word_to_guess: str = ""
    phase: GamePhase = GamePhase.SETUP
    guesses: List[str] = []
    incorrect_guesses: List[str] = []

    @field_validator("word_to_guess")
    @classmethod
    def uppercase(cls, value: str) -> str:
        return value.upper()

    def updateincorrect_guesses(self) -> None:
        self.incorrect_guesses = [letter for letter in self.guesses if letter not in self.word_to_guess]

    def get_masked_state(self) -> "HangmanGameState":
        if self.phase == GamePhase.FINISHED:
            masked_word = self.word_to_guess
        else:
            masked_word = ''.join([letter if letter in self.guesses else '_' for letter in self.word_to_guess])
        return HangmanGameState(
            word_to_guess=masked_word,
            phase=self.phase,
            guesses=self.guesses,
            incorrect_guesses=self.incorrect_guesses
        )

    def check_if_finished(self) -> None:
        if len(set(self.word_to_guess).difference(set(self.guesses))) == 0:
            self.phase = GamePhase.FINISHED
        if len(set(self.guesses).difference(set(self.word_to_guess))) > 7:
            self.phase = GamePhase.FINISHED

    def apply_action(self, action: GuessLetterAction) -> None:
        self.guesses.append(action.letter)
        self.updateincorrect_guesses()
        self.check_if_finished()


class Hangman(Game):

    def __init__(self) -> None:
        self.state = HangmanGameState()

    def get_state(self) -> HangmanGameState:
        return self.state

    def set_state(self, state: HangmanGameState) -> None:
        self.state = state
        self.state.phase = GamePhase.RUNNING

    def print_state(self) -> None:
        state = self.state.get_masked_state()
        print('phase:', state.phase)
        print(' '.join(state.word_to_guess))
        num_wrong = len(self.state.incorrect_guesses)
        if num_wrong == 0:
            print("\n\n\n\n\n\n _")
        else:
            back = " "
            left_arm = " "
            right_arm = " "
            left_leg = " "
            right_leg = " "
            if num_wrong > 2:
                back = '|'
            if num_wrong > 3:
                left_arm = '/'
            if num_wrong > 4:
                right_arm = '\\'
            if num_wrong > 5:
                left_leg = "/"
            if num_wrong > 6:
                right_leg = "\\"
            print(" _______")
            print(" |/    |" if num_wrong > 7 else " |/")
            print(" |     O" if num_wrong > 1 else " |")
            print(f" |    {left_arm}{back}{right_arm}")
            print(f" |    {left_leg} {right_leg}")
            print(" |_")
        print(f"Incorrect guesses: {' '.join(self.state.incorrect_guesses)}")
        if self.state.phase == GamePhase.FINISHED:
            print(f"Solution: {self.state.word_to_guess}")

    def get_list_action(self) -> List[GuessLetterAction]:
        if self.state.phase == GamePhase.FINISHED:
            return []
        all_letters = string.ascii_uppercase
        return [GuessLetterAction(letter=letter) for letter in all_letters if letter not in self.state.guesses]

    def apply_action(self, action: GuessLetterAction) -> None:
        if self.state.phase == GamePhase.FINISHED:
            raise ValueError("Game is finished")
        self.state.apply_action(action)

    def get_player_view(self, idx_player: int) -> HangmanGameState:
        return self.state.get_masked_state()


# pylint: disable = too-few-public-methods
class RandomPlayer(Player):

    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> Optional[GuessLetterAction]:
        if len(actions) > 0:
            return random.choice(actions)
        return None


# pylint: disable = too-few-public-methods
class StructuredPlayer(Player):
    perfect_order = [*'ESIARNTOLCDUPMGHBYFVKWZXQJ']

    def select_action(self, state: HangmanGameState, actions: List[GuessLetterAction]) -> GuessLetterAction:
        if len(actions) == 0:
            raise ValueError("Empty action list")
        available_letters = [action.letter for action in actions]
        for letter in self.perfect_order:
            if letter in available_letters:
                return GuessLetterAction(letter=letter)
        return actions[0]


if __name__ == "__main__":

    game = Hangman()
    game_state = HangmanGameState(word_to_guess='DevOps')
    game.set_state(game_state)
    player = StructuredPlayer()
    for _ in range(26):
        if game.state.phase == GamePhase.FINISHED:
            break
        act = player.select_action(game.get_state(), game.get_list_action())
        game.apply_action(act)
        game.print_state()
        print("\n---------------------\n")

# Alternative main section where you need to input the guesses in the command line.

# if __name__ == "__main__":
#
#     # Initialize the Hangman game
#     game = Hangman()
#
#     # Set up a new game state
#     game_state = HangmanGameState(
#         word_to_guess="DevOpsp".upper(), # Word to guess
#         phase=GamePhase.RUNNING,         # Phase set to RUNNING
#         guesses=[],                      # No correct guesses yet
#         incorrect_guesses=[]             # No incorrect guesses yet
#     )
#
#     game.set_state(game_state)  # Initialize the game state
#
#     game.print_state()
#     # Start taking guesses in a loop until the game ends
#     while game.get_state().phase != GamePhase.FINISHED:
#         # Display available actions
#         actions = game.get_list_action()
#         print("\nAvailable actions:", [action.letter for action in actions])
#
#         # Take input from the player
#         guess = input("Enter your guess: ").upper()
#
#         # Find the action matching the input
#         selected_action = next((action for action in actions if action.letter == guess), None)
#
#         if selected_action:
#             game.apply_action(selected_action)
#             game.print_state()  # Update and print game state after the guess
#         else:
#             print(f"Invalid guess '{guess}'. Try again.")