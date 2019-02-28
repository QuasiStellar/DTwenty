import random

import arcade

import Game


SEED = random.random()

TECTONIC_PLATES = 7
# Amount of plates into which we divide the map.

N = 3
# You can change this constant.
# It determines an amount of cells on your map (2 * 4**N + 1 cells on one side).
# Remember that quantity is proportional to the square of edge length.
# Huge values can cause lags and Memory Error (N>3)


def main():
    game = Game.Game(n=N, tectonic_plates_count=TECTONIC_PLATES, seed=SEED)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
