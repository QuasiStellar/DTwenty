import random

import arcade

import Game


SEED = random.random()

TECTONIC_PLATES = 20
""" Amount of plates into which we divide the map. """

N = 2
""" You can change this constant. It determines an amount of cells on your map (2 * 4**N + 1 cells on one side). """


def main():
    game = Game.Game(n=N, tectonic_plates_count=TECTONIC_PLATES, seed=SEED)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
