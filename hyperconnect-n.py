from operator import add, sub

# n - number of connections to win
def make_new_hyperboard(k=2,size=7):
    if k == 2:
        return [["-" for col in range(size)] for row in range(size)]
    else:
        return [make_new_hyperboard(k-1,size) for hyperrow in range(size)]

def print_hyperboard(board, k, size):
    if k == 2:
        for row in board:
            print row
    else:
        for i in range(size):
            print i
            print_hyperboard(board[i], k - 1, size)

def get_hypermove(player, k, size):
    move = (-1,)
    while(invalid_hypermove(move, k, size)):
        move = input("Player " + player + ", input a comma-separated hypermove: ")
    return move

def invalid_hypermove(move, k, size):
    if len(move) != k-1:
        return True
    for dim in move:
        if dim < 0 or dim >= size:
            return True
    return False

def update_hyperboard(move, player, board, k, size):
    if k == 2:
        row = size -1
        while(row > -1 and board[row][move[0]] != "-"):
            row -= 1
        if row != -1:
            board[row][move[0]] = player
        return move + (row,)
    else:
        return move[:1] + update_hyperboard(move[1:], player, board[move[0]], k - 1, size)

def generate_directions(k):
    if k == 1:
        return [(1,), (-1,)]
    else:
        new_directions = []
        for direction in generate_directions(k - 1):
            for i in range(len(direction) + 1):
                new_directions.append(direction[:i] + (-1,) + direction[i:])
                new_directions.append(direction[:i] + (0,) + direction[i:])
                new_directions.append(direction[:i] + (1,) + direction[i:])
        return list(set(new_directions))

def index_hyperboard(board, position, k):
    if k == 2:
        return board[position[1]][position[0]]
    else:
        return index_hyperboard(board[position[0]], position[1:], k-1)

def check_for_winner(board, position, player, n, size, k, directions):
    for direction in directions:
        direction_sum = 1
        for operator in (add, sub):
            neighbour = position
            for i in range(1, n):
                neighbour = elementwise(neighbour, direction, operator)
                if max(neighbour) < size and min(neighbour) >= 0:
                    if index_hyperboard(board, neighbour, k) == player:
                        direction_sum += 1
                    else:
                        break
        if direction_sum >= n:
            return True
    return False

def elementwise(tup1, tup2, operator):
    assert len(tup1) == len(tup2)
    return tuple(operator(tup1[x], tup2[x]) for x in range(len(tup1)))

def main():
    print("\nWelcome to k-Dimensional Connect N, this is going to be really fun!?!")
    print("Warning: Scales exponentially with dimension. Proceed with caution...")
    k = 3
    size = 7
    n = size / 2 + 1
    directions = generate_directions(k)
    board = make_new_hyperboard(k,size)
    print_hyperboard(board,k,size)

    turn = 0
    players = {0: "*", 1: "#"}
    while True:
        player = players[turn]
        move = get_hypermove(player, k, size)
        position = update_hyperboard(move, player, board, k, size)
        print_hyperboard(board, k, size)
        turn = 1 - turn
        if(check_for_winner(board, position, player, n, size, k, directions)):
            print "Player " + player + " wins!"
            break

if __name__ == '__main__':
    main()
