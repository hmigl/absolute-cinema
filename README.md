# Absolute Cinema

Conteúdo
=========

- [Visão Geral](#visão-geral)
- [Começando](#começando)
    - [Requisitos](#requisitos)
    - [Instalação](#instalação)
    - [Como Rodar o Jogo](#como-rodar-o-jogo)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## Visão Geral

**Absolute Cinema** é um jogo de simulação multithreaded que explora conceitos de condições de corrida e mecanismos de
sincronização. No jogo, os jogadores são personagens que se movem por um cinema, interagindo com itens como filmes e
pipocas. Esses itens têm regras específicas para consumo, que dependem da presença de outros jogadores no mesmo espaço,
simulando barreiras de sincronização.

### Condições de Corrida e Resolução

Uma condição de corrida ocorre quando duas ou mais threads (ou jogadores) acessam uma seção crítica de código
simultaneamente, podendo resultar em comportamento inesperado ou incorreto. No **Absolute Cinema**, utiliza-se diversos
mecanismos de sincronização para resolver essas condições:

- **Mutex (Mutual Exclusion)**: Controla o acesso exclusivo a seções críticas para garantir que apenas um jogador acesse
  o recurso de cada vez.
- **Semáforo**: Limita o número de jogadores que podem entrar em uma determinada célula do cinema ao mesmo tempo.
- **Barreiras**: Sincronizam os jogadores em determinadas células, fazendo com que esperem até que todos estejam
  presentes para realizar ações conjuntas.

### O Jogo

O jogo simula um cinema de tamanho `10x10` onde os jogadores se movem e interagem com os itens. Eles começam na parte
inferior do cinema e tentam assistir a filmes e coletar pipocas. O objetivo é maximizar o número de pipocas consumidas
em relação à duração dos filmes assistidos.

### Conceitos Principais

- **Theater (Cinema)**: Representa o ambiente onde os jogadores (10, mas customizável) se movem e interagem. Ele é composto por uma matriz de
  células que podem conter itens como filmes ('M') e pipocas ('P').
- **Player (Jogador)**: Representa os personagens controlados por threads, que se movem pelo teatro e interagem com os
  itens.
- **IMDbList**: Uma lista compartilhada onde os jogadores escrevem suas críticas de filmes, que são usadas para
  determinar o vencedor ao final do jogo.

### O Vencedor

O vencedor do jogo é determinado com base em uma combinação de fatores: o número de pipocas coletadas e a duração dos
filmes assistidos. A pontuação final é calculada como a multiplicação do número de pipocas pelo tempo de duração dos
filmes.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## Começando

### Requisitos

- Python 3.12 ou superior
- Git instalado na sua máquina

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/hmigl/absolute-cinema.git
   cd absolute-cinema
   ```

2. Escolha um módulo de sincronização para rodar o jogo:

    ```bash
   # Mutex
   cd mutex
    ```

    ```bash
    # Semáforo
    cd semaphore
    ```

    ```bash
    # Barreira
    cd barrier
    ```

3. Rode o jogo:

    ```bash
    python3 absolute_cinema.py
    ```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
# Observações
Para personalizar o tamanho do cinema, o número de jogadores, ou outros parâmetros, é possível editar as variáveis no arquivo absolute_cinema.py.
O jogo foi projetado para rodar no terminal, então certifique-se de que seu terminal suporte as cores usadas no jogo (via a biblioteca colorama).