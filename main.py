import arcade

import Game


SEED = 239

""" Amount of plates into which we divide the map. """
TECTONIC_PLATES = 200

N = 20
""" You can change this constant. It determines an amount of cells on your map (3N cells on one side).
    Remember that quantity is proportional to the square of edge length.
    Huge values can cause lags and Memory Error (N>80) """


def main():
    game = Game.Game(n=N, tectonic_plates_count=TECTONIC_PLATES, seed=SEED)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
