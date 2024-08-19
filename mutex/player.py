import random
import time

from colorama import Fore


class Player:
    def __init__(self, player_id, theater, imdb_list):
        self.player_id = player_id
        self.theater = theater
        self.imdb_list = imdb_list
        self.position = (theater.size - 1, random.randint(0, theater.size - 1))
        self.popcorn_count = 1

    def move(self):
        """
        Metodo principal para movimentar o jogador. O jogador se move para uma posição aleatória adjacente a sua
        posição. Os movimentos possiveis sao: cima, esquerda, direita e diagonais superiores. Além disso, são limitados
        pelo valor de MOVEMENTS
        :return: None
        """
        from absolute_cinema import MOVEMENTS

        for _ in range(MOVEMENTS):
            x, y = self.position
            move = random.choice(
                [
                    (x - 1, y - 1),  # diagonal superior esquerda
                    (x - 1, y),  # cima
                    (x - 1, y + 1),  # diagonal superior direita
                    (x, y - 1),  # esquerda
                    (x, y + 1),  # direita
                ]
            )
            new_x, new_y = move
            self.theater.move_player(
                player=self, old_x=x, old_y=y, new_x=new_x, new_y=new_y
            )
            time.sleep(0.1)

    def action(self):
        x, y = self.position
        cell = self.theater.grid[x][y]
        if cell == "M":
            from absolute_cinema import MOVIE_DURATION_RANGE

            duration = random.uniform(*MOVIE_DURATION_RANGE)
            print(
                f"{Fore.CYAN}Player {self.player_id} is watching a movie at ({x}, {y}) "
                + f"for {int(duration * 1000)} milliseconds{Fore.RESET}"
            )
            time.sleep(duration)
            self.imdb_list.write_review(self.player_id, self.popcorn_count, duration)
        elif cell == "P":
            print(
                f"{Fore.CYAN}Player {self.player_id} found a popcorn at ({x}, {y}){Fore.RESET}"
            )
            self.popcorn_count += 1
