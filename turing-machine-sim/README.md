Pardon my mess, the pokemon stuff I did in a rush, so the naming convention is ugly

`pkmntype.py` runs the Turing Machine, taking in as command lines the
arguments for the Turing Machine

`pkmntypes.yml` is the generated Turing Machine source code

`pkmn-typechart-tmgen.py` generates the Turing Machine source code for Pokemon types

`evz.*` are files regarding the evenzeros machine

`even-zeros.yml` (sic) is the Turing Machine source code for computing if there
are an even number of zeros

Here is a visual explanation of how the Turing Machine computes type:

(For Fire attacking Grass/Bug)

|State|0   |1   |2   |
|-----|----|----|----|
|>>qReadMove<<|Fire|Grass|Bug|
|qFire|>>{empty}<<|Grass|Bug|
|qFire|{empty}|>>2<<|Bug|
|qFire|{empty}|2|>>2<<|
|qComputeStart|{empty}|>>2<<|2|
|qCompute2|>>{empty}<<|2|2|
|qAccept|>>{empty}<<|4|2|

