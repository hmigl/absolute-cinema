import random

from colorama import Fore

from mutex import Mutex


class Theater:
    def __init__(self, size):
        self.size = size
        self.grid = [["F" for _ in range(size)] for _ in range(size)]
        self.locks = [[Mutex() for _ in range(size)] for _ in range(size)]

    def place_items(self, movies, popcorn):
        """
        Aloca os filmes e pipocas no cinema, em posições aleatórias

        :param movies: quantidade de filmes
        :param popcorn: quantidade de pipocas
        :return: None
        """
        for _ in range(movies):
            x, y = self.random_empty_cell()
            self.grid[x][y] = "M"
        for _ in range(popcorn):
            x, y = self.random_empty_cell()
            self.grid[x][y] = "P"

    def random_empty_cell(self):
        """
        Retorna uma posição aleatória vazia no cinema
        :return:
        """
        while True:
            x, y = random.randint(0, self.size - 2), random.randint(0, self.size - 1)
            if self.grid[x][y] == "F":
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
        from absolute_cinema import NUMBER_OF_PLAYERS

        if (
            (0 <= new_x < self.size)
            and (0 <= new_y < self.size)
            and self.grid[new_x][new_y]
            not in [str(i) for i in range(NUMBER_OF_PLAYERS)]
        ):
            if not self.locks[new_x][new_y].acquire(timeout=0.2):
                print(
                    f"{Fore.RED}Player {player.player_id} could not move to ({new_x}, {new_y}){Fore.RESET}"
                )
                return
            try:
                self.move_or_consume(player, old_x, old_y, new_x, new_y)
            finally:
                self.locks[new_x][new_y].release()

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
        with self.locks[old_x][old_y]:
            self.grid[old_x][old_y] = "F"
        if self.grid[new_x][new_y] in ["P", "M"]:
            player.action()
        self.grid[new_x][new_y] = str(player.player_id)

    def place_players(self, players):
        """
        Aloca os jogadores no cinema, em posições aleatórias na última linha do cinema

        :param players: lista de jogadores a serem alocados
        :return: None
        """
        while True:
            for player in players:
                random_pos_at_bottom = (self.size - 1, random.randint(0, self.size - 1))
                x, y = random_pos_at_bottom
                self.grid[x][y] = str(player.player_id)
                player.position = random_pos_at_bottom

            from absolute_cinema import NUMBER_OF_PLAYERS

            if all(
                str(i) in [cell for row in self.grid for cell in row]
                for i in range(NUMBER_OF_PLAYERS)
            ):
                break

            from absolute_cinema import GRID_SIZE

            self.grid[GRID_SIZE - 1] = ["F" for _ in range(GRID_SIZE)]
