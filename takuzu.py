# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 15:
# 99102 Manuel Albino
# 99108 Matilde Tocha

from itertools import count
import sys

from numpy import broadcast_to
from sqlalchemy import false, true
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board: list, n: int) -> None:
        self.board = board
        self.n = n
        
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]
            
    def get_columns(self):
        tup=()
        for i in range(self.n):
            tupl=()
            for j in range(self.n):
                tupl+=(self.board[j][i],)
            tup+=(tupl,)
        return tup
    
    def get_lines(self):
        tup=()
        for i in range(self.n):
           tup+=(tuple(self.board[i]),)
        return tup

        
    def adjacent_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.board[row+1][col], self.board[row-1][col]) if row - 1 >= 0 and row + 1 < self.n \
            else ((self.board[row+1][col], None) if row - 1 < 0 else (None, self.board[row-1][col]))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row][col-1], self.board[row][col+1]) if col - 1 >= 0 and col + 1 < self.n \
            else ((None, self.board[row][col+1]) if col - 1 < 0 else (self.board[row][col-1], None)) 
    
    def __str__(self) -> str:
        string = ''
        for i in range(self.n):
            for j in range(self.n):
                string += str(self.board[i][j]) + '\t'
            if i != self.n:
                string += '\n'
        return string 
    
    def put_piece(self, pos: tuple) -> list: 
        cp_board = self.board.copy()
        cp_board[pos[0]][pos[1]] = pos[2] 
        return cp_board
    
    def get_avail_pos(self) -> tuple:
        return tuple((row, col) for row in range(self.n) for col in range(self.n) if self.get_number(row, col) == 2)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01
        """
        n = int(sys.stdin.readline())
        return Board([list(map(int, sys.stdin.readline().split("\t"))) for i in range(n)], n)
        
        
    # TODO: outros metodos da classe

# board = Board.parse_instance_from_stdin()
# print("Initial:\n",board,sep="")
# print(board.get_columns())
# print(board.get_lines())


# print(board.adjacent_vertical_numbers(3, 3))
# print(board.adjacent_horizontal_numbers(3, 3))

# print(board.adjacent_vertical_numbers(1, 1))
# print(board.adjacent_horizontal_numbers(1, 1))


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.state = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        posicoes_livres = self.board.get_avail_pos()
        
    def equal_vertical_adjacents(self, pos): # rule 1
        return tuple(value for value in (0,1) if value not in self.board.adjacent_vertical_numbers(pos[0], pos[1])) \
            + pos
    
    def equal_horizontal_adjacents(self, pos): # rule 2
        return tuple(value for value in (0,1) if value not in self.board.adjacent_horizontal_numbers(pos[0], pos[1])) \
        + pos
    
    def different_columns_lines(self):
        lines_columns = self.board.get_lines() + self.board.get_columns()
        return len(set(lines_columns)) == len(lines_columns)
    
    def equal_number_1_0(self):
        lines_columns = self.board.get_lines() + self.board.get_columns()
        var = lines_columns[0][0]
        for i in range(len(lines_columns)):
            count_var=0
            for k in range(len(lines_columns[0])):
                if count_var > (len(lines_columns[0]))/2:
                    return false
                if lines_columns[i][k] == var:
                    count_var+=1
            if count_var != (len(lines_columns[0]))/2:
                return false
        return true
    
    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

board = Board.parse_instance_from_stdin()
problem = Takuzu(board)
print("Initial:\n",board,sep="")
print(problem.equal_number_1_0())
# print(problem.equal_vertical_adjacents((0, 1)))

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
