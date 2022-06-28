# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 15:
# 99102 Manuel Albino
# 99108 Matilde Tocha

from email.header import Header
import numpy as np
from numpy import array

import sys

from search import (
    InstrumentedProblem,
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    compare_searchers,
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

class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board: np.array, n: int) -> None:
        self.board = board
        self.n = n
        self.certains=0
        
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col]
            
    def get_columns(self) -> array:
        return np.transpose(self.board)
    
    def get_rows(self) -> array:
        return self.board
    
    def get_avail_pos(self) -> tuple:
        return tuple((row, col) for row in range(self.n) for col in range(self.n) \
            if self.get_number(row, col) == 2)

    def put_piece(self, pos: tuple): 
        self.board[pos[0], pos[1]] = int(str(pos[2]))
        
        return self.board
    
    def out_of_bounds(self, row, col) -> bool:
        return row < 0 or row >= self.n or col < 0 or col >= self.n
        
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
                if j == self.n - 1:
                    string += str(self.board[i, j]) + '\n'
                else:
                    string += str(self.board[i, j]) +  '\t'
            
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
    
class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState) -> tuple:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = Board(state.board.board, self.board.n)
        avail_pos = board.get_avail_pos()
                    
        def fill_cols() -> np.array: # rule 1.1
            columns = board.get_columns()
            res = []
            np.array(res)
            
            for i in range(len(columns)):
                if np.count_nonzero(columns[i] == 0) == board.n // 2 + board.n % 2:
                    res += [(pos[0], pos[1], 1) for pos in avail_pos if pos[1] == i]
                
                elif np.count_nonzero(columns[i] == 1) == board.n // 2 + board.n % 2:
                    res += [(pos[0], pos[1], 0) for pos in avail_pos if pos[1] == i]
                    
            return res
        
        def fill_rows() -> np.array: # rule 1.2
            rows = board.get_rows()
            res = []
            np.array(res)
            
            for i in range(len(rows)):
                if np.count_nonzero(rows[i] == 0) == board.n // 2 + board.n % 2:
                    res += [(pos[0], pos[1], 1) for pos in avail_pos if pos[0] == i]
                
                elif np.count_nonzero(rows[i] == 1) == board.n // 2 + board.n % 2:
                    res += [(pos[0], pos[1], 0) for pos in avail_pos if pos[0] == i]
                    
            return res
    
        def trios(): # rule 2
            res = []
            np.array(res)
            for pos in avail_pos:
                adjacents_v = board.adjacent_vertical_numbers(pos[0], pos[1])
                adjacents_h = board.adjacent_horizontal_numbers(pos[0], pos[1])

                if len(set(adjacents_v)) == 1 and (adjacents_v[0] == 0 or adjacents_v[0] == 1):
                    res += [(pos[0], pos[1], 1) if adjacents_v[0] == adjacents_v[1] == 0 else (pos[0], pos[1], 0)]

                if len(set(adjacents_h)) == 1 and (adjacents_h[0] == 0 or adjacents_h[0] == 1):
                    res += [(pos[0], pos[1], 1) if adjacents_h[0] == adjacents_h[1] == 0 else (pos[0], pos[1], 0)]
                    
            return res
    
        def pairs(): # rule 3
            res = []
            
            for pos in avail_pos:
                row = pos[0]
                col = pos[1]
                
                adjacents_h = board.adjacent_horizontal_numbers(row, col)
                adjacents_v = board.adjacent_vertical_numbers(row, col)
                
                if not board.out_of_bounds(row, col - 2):
                    if board.get_number(row, col - 2) == adjacents_h[0] == 0:
                        res += [(row, col, 1)]
                        
                    elif board.get_number(row, col - 2) == adjacents_h[0] == 1: 
                        res += [(row, col, 0)]
                
                if not board.out_of_bounds(row, col + 2):
                    if board.get_number(row, col + 2) == adjacents_h[1] == 0:
                        res += [(row, col, 1)]
                        
                    elif board.get_number(row, col + 2) == adjacents_h[1] == 1: 
                        res += [(row, col, 0)]
                
                if not board.out_of_bounds(row + 2, col): 
                    if board.get_number(row + 2, col) == adjacents_v[0] == 0:
                        res += [(row, col, 1)]
                        
                    elif board.get_number(row + 2, col) == adjacents_v[0] == 1: 
                        res += [(row, col, 0)]
                
                if not board.out_of_bounds(row - 2, col):     
                    if board.get_number(row - 2, col) == adjacents_v[1] == 0:
                        res += [(row, col, 1)]
                        
                    elif board.get_number(row - 2, col) == adjacents_v[1] == 1: 
                        res += [(row, col, 0)]

            return res
        
        if avail_pos:
            for rule in (fill_cols, fill_rows, trios, pairs):
                certain = rule()
                if certain:
                    board.certains+=1
                    return [certain[0]]

            return [(avail_pos[0][0], avail_pos[0][1], 0), (avail_pos[0][0], avail_pos[0][1], 1)]
            
        else:
            return []
        
    
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
        board = Board(state.board.board, self.board.n)
        
        if len(board.get_avail_pos()) != 0:
            return False
        
        
        def different_columns_lines():
            return len(np.unique(board.get_rows(),axis=0)) == len(board.get_rows()) and \
                len(np.unique(board.get_columns(),axis=0)) == len(board.get_columns()) 
                
        def equal_number_1_0():
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
                        return False

                    if np.count_nonzero(columns[i] == 1) != board.n / 2 or np.count_nonzero(columns[i] == 0) != board.n / 2:
                        return False
                return True
            
        def different_adj_numbers():
            
            for i in range(board.n):
                for j in range(board.n):
                    if len(set(board.adjacent_horizontal_numbers(i,j))) == 1 and board.get_number(i,j) == board.adjacent_horizontal_numbers(i,j)[0] or len(set(board.adjacent_vertical_numbers(i,j))) == 1 and board.get_number(i,j) == board.adjacent_vertical_numbers(i,j)[0]:
                        return False

            return True     
            
    
        return different_columns_lines() and equal_number_1_0() and different_adj_numbers()
    
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return 99999999999-node.state.board.certains


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
 
    compare_searchers([problem,],header=['Searchers','Results'],searchers=[breadth_first_tree_search,
                                                  depth_first_tree_search,
                                                  greedy_search,
                                                  astar_search])

    # goal_node = depth_first_tree_search(problem)
    # print(goal_node.state.board, end = "")
    
