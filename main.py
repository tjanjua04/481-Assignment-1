from queue import Queue

class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
    
    def goal_test(self, state):
        return state == self.goal

class MissCannibalsVariant(Problem):
    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        initial = (N1, N2, True)
        self.N1 = N1
        self.N2 = N2
        super().__init__(initial, goal)
    
    def actions(self, state):
        m, c, onLeft = state
        actions = []
        possible_moves = ['M', 'C', 'MM', 'MC', 'CC', 'MMC']
        
        for move in possible_moves:
            missionaries_to_move = move.count('M')
            cannibals_to_move = move.count('C')
            
            if onLeft:
                new_m, new_c = m - missionaries_to_move, c - cannibals_to_move
            else:
                new_m, new_c = m + missionaries_to_move, c + cannibals_to_move
            
            if self.is_valid_state(new_m, new_c):
                actions.append(move)
        
        return actions
    
    def result(self, state, action):
        m, c, onLeft = state
        missionaries_to_move = action.count('M')
        cannibals_to_move = action.count('C')
        
        if onLeft:
            new_m, new_c = m - missionaries_to_move, c - cannibals_to_move
        else:
            new_m, new_c = m + missionaries_to_move, c + cannibals_to_move
        
        return (new_m, new_c, not onLeft)
    
    def is_valid_state(self, m, c):
        if m < 0 or c < 0 or m > self.N1 or c > self.N2:
            return False
        if (m > 0 and m < c) or (self.N1 - m > 0 and (self.N1 - m < self.N2 - c)):
            return False
        return True

def depth_first_graph_search(problem):
    stack = [(problem.initial, [])]
    explored = set()
    
    while stack:
        state, path = stack.pop()
        if problem.goal_test(state):
            return path
        if state not in explored:
            explored.add(state)
            for action in problem.actions(state):
                stack.append((problem.result(state, action), path + [action]))
    return None

def breadth_first_graph_search(problem):
    queue = Queue()
    queue.put((problem.initial, []))
    explored = set()
    
    while not queue.empty():
        state, path = queue.get()
        if problem.goal_test(state):
            return path
        if state not in explored:
            explored.add(state)
            for action in problem.actions(state):
                queue.put((problem.result(state, action), path + [action]))
    return None

if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)
    
    path = depth_first_graph_search(mc)
    print(path)
    
    path = breadth_first_graph_search(mc)
    print(path)
