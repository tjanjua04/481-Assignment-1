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
        allowed_moves = ['M', 'C', 'MM', 'MC', 'CC', 'MMC']
        moves = []
        for move in allowed_moves:
            missionaries = move.count('M')
            cannibals = move.count('C')
            if onLeft:
                if missionaries > m or cannibals > c:
                    continue
                new_m = m - missionaries
                new_c = c - cannibals
            else:
                if missionaries > (self.N1 - m) or cannibals > (self.N2 - c):
                    continue
                new_m = m + missionaries
                new_c = c + cannibals
            if self.is_valid_state(new_m, new_c):
                moves.append(move)
        return moves
    
    def result(self, state, action):
        m, c, onLeft = state
        missionaries = action.count('M')
        cannibals = action.count('C')
        if onLeft:
            new_m = m - missionaries
            new_c = c - cannibals
        else:
            new_m = m + missionaries
            new_c = c + cannibals
        return (new_m, new_c, not onLeft)
    
    def is_valid_state(self, m, c):
        if m < 0 or c < 0 or m > self.N1 or c > self.N2:
            return False
        if m > 0 and m < c:
            return False
        if (self.N1 - m) > 0 and (self.N1 - m) < (self.N2 - c):
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
                new_state = problem.result(state, action)
                if new_state not in explored:
                    stack.append((new_state, path + [action]))
    return []

def breadth_first_graph_search(problem):
    q = Queue()
    q.put((problem.initial, []))
    explored = set()
    while not q.empty():
        state, path = q.get()
        if problem.goal_test(state):
            return path
        if state not in explored:
            explored.add(state)
            for action in problem.actions(state):
                new_state = problem.result(state, action)
                if new_state not in explored:
                    q.put((new_state, path + [action]))
    return []

if __name__ == '__main__':
    # Test result function
    print("Test result((4,2,True), 'CC') =", MissCannibalsVariant(4,4).result((4,2,True), 'CC'))
    print("Test result((4,2,True), 'C') =", MissCannibalsVariant(4,4).result((4,2,True), 'C'))
    print("Test result((4,2,True), 'MM') =", MissCannibalsVariant(4,4).result((4,2,True), 'MM'))
    print("Test result((1,1,False), 'MMM') =", MissCannibalsVariant(4,4).result((1,1,False), 'MMM'))
    print("Test result((1,1,False), 'MC') =", MissCannibalsVariant(4,4).result((1,1,False), 'MC'))
    
    # Test valid actions
    print("Valid actions from (3,3,True) with N1=3, N2=3:", MissCannibalsVariant(3,3).actions((3,3,True)))
    print("Valid actions from (2,2,False) with N1=4, N2=4:", MissCannibalsVariant(4,4).actions((2,2,False)))
    
    # Solve puzzles
    for (N1, N2) in [(4,4), (3,3), (3,2), (3,1)]:
        print(f"Solving for N1={N1}, N2={N2}")
        mc = MissCannibalsVariant(N1, N2)
        path = breadth_first_graph_search(mc)
        print(path if path else "No solution found")
