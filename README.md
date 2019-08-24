# Game of life

Command line to observe how [Conway's game of life](https://www.wikiwand.com/en/Conway's_Game_of_Life) works.

## Installation

[pygame](https://www.pygame.org) for a graphical representation:
`> pip install pygame`

Patterns database can be downloaded [here](www.conwaylife.com/patterns/all.zip), put all files in the [patterns](patterns/) directory.

## Usage

For a quick demo: `> python main.py`.
To see the different options: `python main.py -h`.

In graphical mode you can move around using arrow keys and zoom in and out with `+` and `-`.

There is also an ugly console display: `python main.py --console-display`.
