# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 15:
# 99102 Manuel Albino
# 99108 Matilde Tocha

from itertools import count
import numpy as np
from numpy import array, broadcast_to, column_stack

import sys

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

    def __init__(self, board: np.array, n: int) -> None:
        self.board = board
        self.n = n
        
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col]
            
    def get_columns(self) -> array:
        # tup = ()
        # for i in range(self.n):
        #     tupl = ()
        #     for j in range(self.n):
        #         tupl += (self.board[j, i],)
        #     tup += (tupl,)
        return np.transpose(self.board)
    
    def get_rows(self) -> array:
        # tup = ()
        # for i in range(self.n):
        #    tup += (tuple(self.board[i]),)
        # np.array([self.board[i, :] for i in range(self.n)])
        return self.board
    
    def get_avail_pos(self) -> tuple:
        return tuple((row, col) for row in range(self.n) for col in range(self.n) \
            if self.get_number(row, col) == 2)

    def put_piece(self, pos: tuple) -> array: 
        cp_board = self.board.copy()
        cp_board[pos[0], pos[1]] = pos[2]

        return cp_board
        
    def adjacent_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.board[row+1, col], self.board[row-1, col]) if row - 1 >= 0 and row + 1 < self.n \
            else ((self.board[row+1, col], None) if row - 1 < 0 else (None, self.board[row-1, col]))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row, col-1], self.board[row, col+1]) if col - 1 >= 0 and col + 1 < self.n \
            else ((None, self.board[row, col+1]) if col - 1 < 0 else (self.board[row, col-1], None)) 
    
    def __str__(self) -> str:
        string = ''
        for i in range(self.n):
            for j in range(self.n):
                string += str(self.board[i, j]) + '\t'
            if i != self.n:
                string += '\n'
        return string 

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01
        """
        n = int(sys.stdin.readline())
        
        list_board = [list(map(int, sys.stdin.readline().split("\t"))) for i in range(n)]
        list_board = np.array(list_board)
        
        return Board(list_board, n)

# board = Board.parse_instance_from_stdin()
# print("Initial:\n", board, sep = "")
# print(board.get_columns())
# print(board.get_rows())
# print(board.get_avail_pos())


# print(board.adjacent_vertical_numbers(3, 3))
# print(board.adjacent_horizontal_numbers(3, 3))

# print(board.adjacent_vertical_numbers(1, 1))
# print(board.adjacent_horizontal_numbers(1, 1))


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.state = TakuzuState(board)

    def actions(self, state: TakuzuState) -> tuple:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        avail_pos = self.board.get_avail_pos()
        
        pass
                    
        def fill_cols(self) -> np.array: # rule 1
            columns = self.board.get_columns()
            res = []
            np.array(res)
            
            for i in range(len(columns)):
                if np.count_nonzero(columns[i] == 0) == self.board.n // 2 + self.board.n % 2:
                    res += [(pos[0], pos[1], 1) for pos in self.board.get_avail_pos() if pos[1] == i]
                
                elif np.count_nonzero(columns[i] == 1) == self.board.n // 2 + self.board.n % 2:
                    res += [(pos[0], pos[1], 0) for pos in self.board.get_avail_pos() if pos[1] == i]
                    
            return res
        
        def fill_rows(self) -> np.array: # rule 1
            rows = self.board.get_rows()
            res = []
            np.array(res)
            
            for i in range(len(rows)):
                if np.count_nonzero(rows[i] == 0) == self.board.n // 2 + self.board.n % 2:
                    res += [(pos[0], pos[1], 1) for pos in self.board.get_avail_pos() if pos[0] == i]
                
                elif np.count_nonzero(rows[i] == 1) == self.board.n // 2 + self.board.n % 2:
                    res += [(pos[0], pos[1], 1) for pos in self.board.get_avail_pos() if pos[0] == i]
                    
            return res
    
        def trios(self, avail_pos: tuple): # rule 2
            res = []
            np.array(res)
            for pos in avail_pos:
                adjacents_v = self.board.adjacent_vertical_numbers(pos[0], pos[1])
                adjacents_h = self.board.adjacent_horizontal_numbers(pos[0], pos[1])

                if len(set(adjacents_v)) == 1 and (adjacents_v[0] == 0 or adjacents_v[0] == 1):
                    res += [(pos[0], pos[1], 1) if adjacents_v[0] == adjacents_v[1] == 0 else (pos[0], pos[1], 0)]

                if len(set(adjacents_h)) == 1 and (adjacents_h[0] == 0 or adjacents_h[0] == 1):
                    res += [(pos[0], pos[1], 1) if adjacents_h[0] == adjacents_h[1] == 0 else (pos[0], pos[1], 0)]
                    
            return res
    
    def equal_horizontal_adjacents(self, pos): # rule 3
        return tuple(value for value in (0,1) if value not in \
            self.board.adjacent_horizontal_numbers(pos[0], pos[1])) + pos
    
    
    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        cp_board = Board(np.copy(state.board.board),self.board.n)
        cp_board.put_piece(action)
       
        return TakuzuState(cp_board)


    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board=state.board
        
        def different_columns_lines(self, board : Board):
            return len(np.unique(board.get_rows())) == len(board.get_rows()) and \
                len(np.unique(board.get_columns())) == len(board.get_columns()) 
                
        def equal_number_1_0(self, board : Board):
            rows = board.get_rows()
            columns = board.get_columns()
            count_var = 0

            if board.n % 2 == 1:
                for i in range(len(rows)):
                    if np.count_nonzero(rows[i] == 1) != board.n // 2 + board.n % 2:
                        if np.count_nonzero(rows[i] == 0) == board.n // 2 + board.n % 2:
                            count_var += 1
                        
                    elif np.count_nonzero(rows[i] == 1) == board.n // 2 + board.n % 2:
                        if np.count_nonzero(rows[i] == 0) != board.n // 2 + board.n % 2:
                            count_var += 1
                        
                    if np.count_nonzero(columns[i] == 1) != board.n // 2 + board.n % 2:
                        if np.count_nonzero(columns[i] == 0) == board.n // 2 + board.n % 2:
                            count_var += 1
                        
                    elif np.count_nonzero(columns[i] == 1) == board.n // 2 + board.n % 2:
                        if np.count_nonzero(columns[i] == 0) != board.n // 2 + board.n % 2:
                            count_var += 1
                            
                return count_var == 2 * len(rows)
                            
            else:
                for i in range(len(rows)):
                    if np.count_nonzero(rows[i] == 1) != board.n / 2 or np.count_nonzero(rows[i] == 0) != board.n / 2:
                        return false
                    if np.count_nonzero(columns[i] == 1) != board.n / 2 or np.count_nonzero(columns[i] == 0) != board.n / 2:
                        return false
                return true
            
        def different_adj_numbers(self, board : Board):
            rows = board.get_rows()
            
            for i in range(board.n):
                for j in range(board.n):
                    if len(set(board.adjacent_horizontal_numbers(i,j)))==1 and board.get_number(i,j)==board.adjacent_horizontal_numbers(i,j)[0] or len(set(board.adjacent_vertical_numbers(i,j)))==1 and board.get_number(i,j)==board.adjacent_vertical_numbers(i,j)[0]:
                        return false
            return true     
            
    
        return different_columns_lines(board) and equal_number_1_0(board) and different_adj_numbers(board)
    
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass


board = Board.parse_instance_from_stdin()
print("Initial:\n",board,sep="")
problem = Takuzu(board)
state = TakuzuState(board)
# avail_pos = board.get_avail_pos()
# print(avail_pos)
# print(problem.trios(avail_pos))
# print(problem.different_adj_numbers(board))
# print(problem.result(state,(1,1,1)))
# print(problem.last_avail_pos(avail_pos))
# print(problem.goal_test(state))
# print(problem.equal_vertical_adjacents((0, 1)))
