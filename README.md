# READ ME

## Implementation Links

* https://www.chessprogramming.org/Main_Page
	* [Board Representation](https://www.chessprogramming.org/Board_Representation)
	* [Search](https://www.chessprogramming.org/Search)

## Packages

* For now none but later pygame for GUI

## FEN Notation

* example of starting state fen string

    * 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

* / : indicate next rank

* numerical value 1-9 : indicates number of empty squares between pieces

* w | b : indicates turn

* - : indicates filler for notation in western chess

* second to last value is number of half moves since last capture (if reaches 60 game ends in draw)

* last value is number of full moves (full move means increments after both white and black move)

* Upper Case for White, Lower case for black
    * King/General: K/k
    * Advisor: A/a
    * Elephant: E/e
    * Rook/Chariot: R/r
    * Cannon: C/c
    * Horse/Knight: H/h
    * Pawn: P/p

## Implemenation

### Board Class

* Variables: 

	* ``state``: {1d Char Array} containing piece positions

	* ``valid_moves``: {array of Moves} contains list of valid moves of the current players turn

	* ``turn``: {char} w | b

	* ``computer_color``: {char} w | b

	* ``king_pos`` {int} integer position of the turn of current players king within state
                     (this will be needed for determining legal moves)
	* ``half_moves`` {int} number of half moves since last capture. If == 60 then game ends in draw, increments after white or black move

	* ``full_moves`` {int} number of full moves

* Functions

	* ``__init__(self, fen)``: default constructor from fen. Uses fen to initialize all board variables
	
	* ``generateValidMoves()``: analyzes state and generates ``valid_moves``

	* ``updateBoardFromMove(move: move.Move)``: updates ``state`` from ``move``

	* ``checkForCheck(move: move.Move, turn: char)``: Helper function that analyzes a move and looks a half move further to see if that move puts themselves in check. Returns bool.


## Notes

* In ``updateBoardFromMove()`` need to increment halfmove counter and full move counter

* In main game loop need to check for draw with halfmove counter










