from search import *

class MissCannibalsVariant(Problem):
    """ The problem of Missionaries and Cannibals. 
    N1 and N2 are the total number of missionaries and cannibals starting from the left bank.
    A state is represented as a 3-tuple, two numbers and a boolean:
    state[0] is the number of missionaries on the left bank (note: the number on the right is N1 - m)
    state[1] is the number of cannibals on the left bank (note: the number on the right is N2 - c)
    state[2] is True if the boat is at the left bank, False if at the right bank """
    
    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        initial = (N1, N2, True)
        self.N1 = N1
        self.N2 = N2
        super().__init__(initial, goal)
    
    def actions(self, state):
        m, c, onLeft = state
        moves = []
        for i in range(1, 4):  # boat capacity 1 to 3
            for m_count in range(i + 1):
                c_count = i - m_count
                if onLeft:
                    if m_count > m or c_count > c:
                        continue
                    new_m = m - m_count
                    new_c = c - c_count
                else:
                    if m_count > (self.N1 - m) or c_count > (self.N2 - c):
                        continue
                    new_m = m + m_count
                    new_c = c + c_count
                if self.is_valid_state(new_m, new_c):
                    moves.append('M' * m_count + 'C' * c_count)
        return moves
    
    def result(self, state, action):
        m, c, onLeft = state
        missionaries = action.count('M')
        cannibals = action.count('C')
        if onLeft:
            return (m - missionaries, c - cannibals, False)
        else:
            return (m + missionaries, c + cannibals, True)
    
    def is_valid_state(self, m, c):
        if m < 0 or c < 0 or m > self.N1 or c > self.N2:
            return False
        if m > 0 and m < c:
            return False
        if (self.N1 - m) > 0 and (self.N1 - m) < (self.N2 - c):
            return False
        return True

if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    path = depth_first_graph_search(mc).solution()
    print(path)
    path = breadth_first_graph_search(mc).solution()
    print(path)
