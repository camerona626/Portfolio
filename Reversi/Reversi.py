#Cameron Anderson
#105907054
#Final Project

#Game adapted from github.com/Alex-Addy/Reversi/blob/master/Reversi.py

import heapq

black = u'\u25CF'
white = u'\u25CB'
b_size = 8
depth = 4

#Othellus
pos_score = [[ 100, -10,  11,   6,   6,  11, -10, 100],
			 [ -10, -20,   1,   2,   2,   1, -20, -10],
			 [  10,   1,   5,   4,   4,   5,   1,  10],
			 [   6,   2,   4,   2,   2,   4,   2,   6],
			 [   6,   2,   4,   2,   2,   4,   2,   6],
			 [  10,   1,   5,   4,   4,   5,   1,  10],
			 [ -10, -20,   1,   2,   2,   1, -20, -10],
			 [ 100, -10,  11,   6,   6,  11, -10, 100]
			]

def main():
	board = [[' ' for x in range(b_size)] for y in range(b_size)]

	# setup the board
	board[int(b_size/2)-1][int(b_size/2)-1] = black
	board[int(b_size/2)][int(b_size/2)] = black
	board[int(b_size/2)-1][int(b_size/2)] = white
	board[int(b_size/2)][int(b_size/2)-1] = white

	blackturn = True
	
	print("Enter moves of the form letter, number.")
	print("For example to move to A3 you would type 'A3' then press enter.")
	print("It is case insensitive.")
	
	while True:
		poss = possibleMoves(board)
		printBoard(board)
		print(poss)
		if poss[black] == [] and poss[white] == []:
			break
		else:
			if blackturn:
				if poss[black]:
					the_move = playerMove(poss, black)
					changeBoard(the_move, board, black)
					blackturn = False
				else:
					the_move = aiMove(poss[white], board)
					changeBoard(the_move, board, white)
			else:
				if poss[white]:
					the_move = aiMove(poss[white], board)
					changeBoard(the_move, board, white)
					blackturn = True
				else:
					the_move = playerMove(poss, black)
					changeBoard(the_move, board, black)

	print(u"Gameover. {0} is the winner.".format(winner(board)))

def possibleMoves(board):

	moves = {black:[], white:[]}
	
	isopen = False
	for x in range(b_size):
		if ' ' in board[x]:
			isopen = True
			break
	#print("Open is ", isopen)
	if not isopen:
		return moves

	for x in range(b_size):
		for y in range(b_size):
			if board[x][y] == ' ':
				#print(x, ' ', y)
				if validDirs(x, y, board, black):
					moves[black].append((x,y))
				if validDirs(x, y, board, white):
					moves[white].append((x,y))
	return moves

def printBoard(board):
	print('      A   B   C   D   E   F   G   H ')
	print('    ---------------------------------')
	for x in range(b_size):
		print (x), (u'  | {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |'.format(*board[x]))
		print('    ---------------------------------')

def playerMove(poss, color):
	# the column is the letter and the row is the number
	while(True):
		if color == u'\u25CF':
			c = 'black'
		else: c = 'white'
		prompt = "{}'s move: ".format(c)
		move = raw_input(prompt)
		move = move.upper()
		col = ord(move[0])-ord('A')
		row = int(move[1])
		if(b_size >= col >= 0):
			if(0 <= row <= b_size):
				if (row, col) in poss[color]:
					return (row, col)
				else:
					print("Invalid location.")
			else:
				print("Invalid number.")
		else:
			print("Invalid letter.")

def aiMove(poss, board):

	def game_score(b):
		w = 0
		for x in range(b_size):
			for y in range(b_size):
				if(b[x][y] == white): w += pos_score[x][y]
		return w
		
	def max_agent(b, d, a, bt):
		p = possibleMoves(b)
		if (p[white] == []) or d == 0:
			return game_score(b)

		score = -(2**32)

		for move in p[white]:
			nb = map(list, b)
			changeBoard(move, nb, white)
			score = max(score, min_agent(nb, d-1, a, bt))

			#print 'max:', move, score

			if score > bt:
				return score
			a = max(a, score)

		return score

	def min_agent(b, d, a, bt):
		p = possibleMoves(b)
		if (p[black] == []) or d == 0:
			return game_score(b)

		score = 2**32

		for move in p[black]:

			nb = map(list, b)
			changeBoard(move, nb, black)
			score = min(score, max_agent(nb, d-1, a, bt))

			#print 'min:', move, score

			if score < a:
				return score
			bt = min(bt, score)

		return score

	m = poss[0]

	score = -(2**32)
	a = -(2**32)
	bt = 2**32
	for move in poss:
		nb = map(list, board)
		changeBoard(move, nb, white)
		new_score = max(score, min_agent(nb, depth, a, bt))

		#print move, new_score
		#printBoard(nb)

		if new_score > score:
			m = move
			score = new_score

		if score > bt:
			#print '\n', m, score
			return m
		a = max(a, score)

	#print '\n', m, score

	return m

def validDirs(base_x, base_y, board, color):
	# returns a tuple of the valid directions
	directions = []

	if board[base_x][base_y] != " ": return directions

	# do a check out from the x, y coordinates using dx and dy values for each direction
	# check left (-x y)
	if checkOneWay(base_x, base_y, board, color, -1, 0): directions.append((-1, 0))
	# check left-up (-x -y)
	if checkOneWay(base_x, base_y, board, color, -1, -1): directions.append((-1, -1))
	# check up (x -y)
	if checkOneWay(base_x, base_y, board, color, 0, -1): directions.append((0, -1))
	# check right-up (+x -y)
	if checkOneWay(base_x, base_y, board, color, 1, -1): directions.append((1, -1))
	# check right (+x y)
	if checkOneWay(base_x, base_y, board, color, 1, 0): directions.append((1, 0))
	# check right-down (+x +y)
	if checkOneWay(base_x, base_y, board, color, 1, 1): directions.append((1, 1))
	# check down (x +y)
	if checkOneWay(base_x, base_y, board, color, 0, 1): directions.append((0, 1))
	# check left-down (-x +y)
	if checkOneWay(base_x, base_y, board, color, -1, 1): directions.append((-1, 1))

	return directions

def checkOneWay(base_x, base_y, board, color, delta_x = 0, delta_y = 0):
	#if delta_x == 0 and delta_y == 0:
	#	return False

	#print("\t", color,"dx", delta_x,"dy", delta_y)

	temp_x = base_x + delta_x
	temp_y = base_y + delta_y

	if 0 > temp_x or temp_x >= b_size or 0 > temp_y or temp_y >= b_size: return False

	if board[temp_x][temp_y] == ' ': return False

	other = (black if white == color else white)
	foundother = False
	#print("\tMade it to loop:", other)
	while 0 <= temp_x < b_size and 0 <= temp_y < b_size:
		#print("\t\tWhere:", temp_x, temp_y, " is: ", board[temp_x][temp_y])
		if board[temp_x][temp_y] == color: return foundother
		elif board[temp_x][temp_y] == other: foundother = True
		elif board[temp_x][temp_y] == ' ': return False
		temp_x += delta_x
		temp_y += delta_y
	return False

def winner(board):
	b, w = 0, 0
	for x in range(b_size):
		for y in range(b_size):
			if(board[x][y] == white): w += 1
			elif(board[x][y] == black): b += 1

	return black if b > w else white

def changeBoard(move, b, color):
	#print("Move selected: ", move[0], move[1])
	b[move[0]][move[1]] = color
	#print("board[{}][{}]:{}".format(move[0], move[1], board[move[0]][move[1]]))
	for dx in [-1, 0, 1]:
		for dy in [-1, 0, 1]:
			if dy == 0 and dx == 0: continue
			#print("\t Loop:", dx, dy)
			if checkOneWay(move[0], move[1], b, color, dx, dy):
				#print("\t\tNow changing.")
				changeOneDir(move[0], move[1], b, color, dx, dy)

def changeOneDir(base_x, base_y, b, color, delta_x = 0, delta_y = 0):

	temp_x = base_x + delta_x
	temp_y = base_y + delta_y

	other = (black if white == color else white)

	while 0 <= temp_x < b_size and 0 <= temp_y < b_size:
		if b[temp_x][temp_y] == ' ': return
		elif b[temp_x][temp_y] == other: b[temp_x][temp_y] = color
		elif b[temp_x][temp_y] == color: return

		temp_x += delta_x
		temp_y += delta_y
	return

if __name__ == '__main__':
	main()
