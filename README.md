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