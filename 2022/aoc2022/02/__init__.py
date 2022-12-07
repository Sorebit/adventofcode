from enum import Enum, auto
from os import getenv
from pathlib import Path


class Reader:
    """_summary_
    """
    def lines(p: Path, strip: bool = True):
        """Yields lines from file :param p: for processing them with or without storage. Opt-out withespace strip"""
        with open(p, 'r') as file:
            for line in file.readlines():
                if strip:
                    yield line.strip()
                else:
                    yield line


VERBOSE = getenv('VERBOSE')


# Opponent choice ranges from A to C and always means their move choice
# Player choice ranges from X to Z. This can be
# - Part 1: Player's move
# - Part 2: Predicated outcome for the round

class Move(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3
    
    @classmethod
    def from_opponent_choice(cls, choice: str) -> 'Move':
        opponent_choices = {
            'A': Move.Rock,
            'B': Move.Paper,
            'C': Move.Scissors,
        }
        return opponent_choices[choice]
        
    @classmethod
    def from_player_choice(cls, choice: str) -> 'Move':
        player_choices = {
            'X': Move.Rock,
            'Y': Move.Paper,
            'Z': Move.Scissors,
        }
        return player_choices[choice]


class Outcome(Enum):
    Lost = 0
    Draw = 3
    Won = 6

    @classmethod
    def from_player_choice(cls, ch: str) -> 'Outcome':
        player_choices = {
            'X': Outcome.Lost,
            'Y': Outcome.Draw,
            'Z': Outcome.Won,
        }
        return player_choices[ch]


class Game:
    # This could be a 2D table, but it's easier for me to read this way
    outcome_lookup = {
        Move.Rock: {
            # lookup[Move.Rock] -> Outcome of the game depending on player's move, when the opp played Rock.
            Move.Rock: Outcome.Draw,
            Move.Paper: Outcome.Won,
            Move.Scissors: Outcome.Lost,
        },
        Move.Paper: {
            Move.Rock: Outcome.Lost,
            Move.Paper: Outcome.Draw,
            Move.Scissors: Outcome.Won,
        },
        Move.Scissors: {
            Move.Rock: Outcome.Won,
            Move.Paper: Outcome.Lost,
            Move.Scissors: Outcome.Draw,
        },
    }
    
    @classmethod
    def player_move_from_predicate(cls, opponent_move: Move, predicate) -> 'Outcome':
        # Find player move for predicated outcome.
        player_choices = cls.outcome_lookup[opponent_move]
        # Find first player choice, that when paired with opponent move, gives predicated outcome.
        solution = next(
            ch 
            for ch in player_choices
            if player_choices[ch] == predicate
        )
        return solution
    
    @classmethod
    def score(cls, opponent_move: Move, player_move: Move | None = None, predicate = None):
        """Find final score based on opponent move and either player move or outcome predicate.
        
        - opponent_move is required and always known.
        - When player_move is unknown (None), an outcome predicate is required. The necessary player_move will
          be found and used to calculate final score.
        - When player_move is known, the outcome will be looked up and used to calculate final_score.
        
        
        Final score is the sum of player's selected shape (Move.value) & outcome (Outcome.value)
        """
        if player_move is not None:
            # Find outcome based on opponent move and player move.
            outcome = cls.outcome_lookup[opponent_move][player_move]
        
        if predicate is not None:
            outcome = predicate
            player_move = cls.player_move_from_predicate(opponent_move, predicate)
            
        return player_move.value + outcome.value

def run(in_file: Path):
    final_score = 0
    final_score_2 = 0
    
    for line in Reader.lines(in_file):
        left, right = line.split()  # A X
        opponent_move = Move.from_opponent_choice(left)
        player_move = Move.from_player_choice(right)
        predicate = Outcome.from_player_choice(right)
        
        score = Game.score(opponent_move, player_move, None)
        score_2 = Game.score(opponent_move, None, predicate)
        final_score += score
        final_score_2 += score_2
    
    return final_score, final_score_2


def test_02():
    part_1, part_2 = run(Path('/home/boczek/Documents/aoc22/aoc2022/02/in/input'))
    assert part_1 == 10310, f'{part_1} != 10310'
    assert part_2 == 14859, f'{part_2} != 14859'
    
test_02()
