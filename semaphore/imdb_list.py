from colorama import Fore


class IMDbList:
    def __init__(self, size):
        self.list = [(i, 1, 0) for i in range(size)]

    def write_review(self, player_id, popcorn_count, movie_duration):
        """
        Escreve uma review de um filme assistido por um jogador.

        :param player_id: id do jogador
        :param popcorn_count: quantidade de pipocas consumidas
        :param movie_duration: duração do filme
        :return:
        """
        print(f"{Fore.YELLOW}Player {player_id} wrote a review{Fore.RESET}")
        self.list[player_id] = (player_id, popcorn_count, int(movie_duration * 100))
