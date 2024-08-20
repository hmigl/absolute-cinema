import random
import threading

from colorama import Fore
from barrier import Barrier


class Theater:
    def __init__(self, size):
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        self.locks = [[threading.Lock() for _ in range(size)] for _ in range(size)]
        self.barriers = [[None for _ in range(size)] for _ in range(size)]

    def place_items(self, movies, popcorn, obstacles=2):
        """
        Aloca os filmes e pipocas no cinema, em posições aleatórias

        :param movies: quantidade de filmes
        :param popcorn: quantidade de pipocas
        :return: None
        """
        for _ in range(movies):
            x, y = self.random_empty_cell()
            self.grid[x][y].append("M")
        for _ in range(popcorn):
            x, y = self.random_empty_cell()
            self.grid[x][y].append("P")
        for _ in range(obstacles):
            x, y = self.random_empty_cell()
            self.grid[x][y].append("O")
            self.barriers[x][y] = Barrier(2)

    def random_empty_cell(self):
        """
        Retorna uma posição aleatória vazia no cinema
        :return:
        """
        while True:
            x, y = random.randint(0, self.size - 2), random.randint(0, self.size - 1)
            if not self.grid[x][y]:
                return x, y

    def move_player(self, player, old_x, old_y, new_x, new_y):
        """
        Move o jogador para a nova posição, se possível

        :param player: jogador a ser movido
        :param old_x: antiga posição x
        :param old_y: antiga posição y
        :param new_x: nova posição x
        :param new_y: nova posição y
        :return:
        """
        if (0 <= new_x < self.size) and (0 <= new_y < self.size):
            if not self.locks[new_x][new_y].acquire(timeout=0.2):
                print(
                    f"{Fore.RED}Player {player.player_id} could not move to ({new_x}, {new_y}){Fore.RESET}"
                )
                return
            try:
                self.move_or_consume(player, old_x, old_y, new_x, new_y)
            finally:
                if self.locks[old_x][old_y].locked():
                    self.locks[old_x][old_y].release()

    def move_or_consume(self, player, old_x, old_y, new_x, new_y):
        """
        Move o jogador para a nova posição. Caso a nova posição contenha um item, o jogador o consome, realizando,
        então, a ação correspondente

        :param player: jogador a ser movido
        :param old_x: antiga posição x
        :param old_y: antiga posição y
        :param new_x: nova posição x
        :param new_y: nova posição y
        :return:
        """
        player.position = (new_x, new_y)
        print(
            f"{Fore.GREEN}Player {player.player_id} moved from ({old_x}, {old_y}) to ({new_x}, {new_y}){Fore.RESET}"
        )

        if self.grid[old_x][old_y]:
            self.grid[old_x][old_y].remove(str(player.player_id))
        self.grid[new_x][new_y].append(str(player.player_id))

        if "O" in self.grid[new_x][new_y]:
            barrier = self.barriers[new_x][new_y]
            if barrier:
                print(
                    f"{Fore.MAGENTA}Player {player.player_id} is waiting at barrier ({new_x}, {new_y}){Fore.RESET}"
                )
                barrier.wait()
        else:
            player.action()

    def place_players(self, players):
        """
        Aloca os jogadores no cinema, em posições aleatórias na última linha do cinema

        :param players: lista de jogadores a serem alocados
        :return: None
        """
        for i, player in enumerate(players):
            pos = (self.size - 1, i)
            x, y = pos
            self.grid[x][y].append(str(player.player_id))
            player.position = pos
