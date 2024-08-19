import time
from concurrent.futures import ThreadPoolExecutor

from colorama import Fore

from imdb_list import IMDbList
from player import Player
from theater import Theater

GRID_SIZE = 10
MOVEMENTS = 25
MOVIE_DURATION_RANGE = (0.1, 1)
NUMBER_OF_PLAYERS = 10


def winner(imdb_list):
    """
    Determina o vencedor do jogo.
    O calculo e feito multiplicando a quantidade de pipoca pelo tempo total de filmes assistidos.
    """
    print(imdb_list.list)
    print(f"{Fore.MAGENTA}The game is over!{Fore.RESET}")
    print(f"{Fore.MAGENTA}The winner is...{Fore.RESET}")
    scores = {}
    for i, popcorn, duration in imdb_list.list:
        scores[i] = popcorn * duration
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    time.sleep(2)
    print(f"{Fore.MAGENTA}Player {sorted_scores[0][0]}{Fore.RESET}")


def print_grid(grid):
    """
    Funcao auxiliar para imprimir a grade do cinema.
    """
    for row in grid:
        print(["".join(cell) if cell else "F" for cell in row])
    print()
    print("- " * 20)


def main():
    theater = Theater(GRID_SIZE, cell_capacity=3)
    theater.place_items(movies=20, popcorn=30)

    print_grid(theater.grid)

    imdb_list = IMDbList(size=NUMBER_OF_PLAYERS)
    players = [Player(i, theater, imdb_list) for i in range(NUMBER_OF_PLAYERS)]
    theater.place_players(players)

    print_grid(theater.grid)

    with ThreadPoolExecutor(max_workers=NUMBER_OF_PLAYERS) as executor:
        futures = [executor.submit(player.move) for player in players]
        for future in futures:
            future.result()
    winner(imdb_list)

    print_grid(theater.grid)


if __name__ == "__main__":
    main()
